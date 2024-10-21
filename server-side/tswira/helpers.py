from .models import *
from django.conf import settings
from gradio_client import Client
import itertools
from django.db.models import Q
from django.conf import settings
import requests
import stripe
from stripe import Customer
import uuid
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_PRIVATE_KEY

def handle_user_created(user):
    FeaturesT.objects.create(user=user).save()
    subscription = SubscriptionT.objects.create(user=user)
    subscription.save()

    print("Saved.")
    customer = Customer.create(name=user, email=user.email)
    profile = UserProfileT.objects.create(user=user, stripe_customer=customer.id)
    profile.save()
    print("Customer created")





hf_token = settings.HF_TOKEN
photo_clients = []
plus_photo_clients = []

print("Loading Photomaker servers...")
for server in settings.HF_SERVER_PHOTO:
    try:
        photo_clients.append(Client(server, hf_token=hf_token, upload_files=False))
    except:
        print("Could not load the server ", server)
print("Successfully loaded free  servers.")

print("Loading plus Photomaker servers...")
for server in settings.HF_SERVER_PHOTO_PLUS:
    try:
        plus_photo_clients.append(Client(server, hf_token=hf_token, upload_files=False))
    except:
        print("Could not load the server ", server)
print("Successfully loaded plus Photomaker  servers.")

photo_server_cycle = itertools.cycle(photo_clients)
plus_photo_server_cycle = itertools.cycle(plus_photo_clients)

def generate_photos(metadata):
    print("Hf token: ", hf_token)
    print("Recieved metadata : ", metadata)
    if metadata["is_free"]:
        print("Free user use slow server")
        client = next(plus_photo_server_cycle)
    else:
        print("Plus user use fast one")
        client = next(photo_server_cycle)
    result = client.submit(
            prompt=metadata["prompt"],
            num_steps=50,
            style_name=metadata["style_name"],
            input_images=metadata["input_images"],
            num_outputs=metadata["num_outputs"],
            guidance_scale=5,
            negative_prompt="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
            style_strength_ratio=20,
            job_id=metadata["job_id"],
            user_token=metadata["user_token"],
            api_name="/generate_image"
    )
    return True


def generate_unique_filename(ext=".mp4"):
    """Generate unique file name
    Paramtres :
        ext (string) : the extention of the file
    Return:
        key (string): the full file name with unique name
    """
    key = str(uuid.uuid4()) + ext
    return key


def update_credits( user, added):
    features = FeaturesT.objects.get(user=user)
    prev_tokens = features.tokens
    tokens = prev_tokens + added
    FeaturesT.objects.filter(user=user).update(tokens=tokens)


def get_product(session_id):
    line_items = stripe.checkout.Session.list_line_items(session_id)        
    price_id = line_items['data'][-1]['price']['id']
    print(f"Checkout session completed for {price_id}")
    product_details = None
    price  = stripe.Price.retrieve(price_id)
    print("Price details ", price)
    product_id = price.product
    product = stripe.Product.retrieve(product_id)
    return product

def handle_payment_finished(data_object):
    session_id = data_object["id"]
    product = get_product(session_id)
    token_granted = product["metadata"]["token_granted"]
    images_granted = product["metadata"]["images_granted"]
    plan = None
    if product:
        plan = product["name"]
    print("Plan: ", plan)
    customer_id = data_object.get("customer")
    print("Customer id: ", customer_id)
    if customer_id:
       user = get_user_by_customer(customer_id)
       restore_membership(user, plan.lower(), token_granted, images_granted, data_object.get("id"))
       return JsonResponse({"status": "success"})

def handle_customer_deleted(data):
    customer_id = data.get("id")
    user = get_user_by_customer(customer_id)

    try:
        if user:
            user.delete()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "No customer found"})
    except Exception as e:
        return JsonResponse({"status": "Error", "error":str(e)}, status=500)  
    
def handle_payment_failed(invoice):
    customer = invoice["customer"]
    transaction_id = invoice["id"]
    description = f"Payment for invoice {invoice['number']} failed"

def handle_subscription_delete(data_object):
    customer_id = data_object.get("customer")
    print("Deleting the customer info ", customer_id)
    user = None
    try:
        if customer_id:
            user = get_user_by_customer(customer_id)
        if user:
            restore_membership(user, "free", 1, None)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "No customer found"})
    except Exception as e:
        return JsonResponse({"status": "Error", "error":str(e)}, status=404)

def get_user_by_customer(id):
    profile = UserProfileT.objects.filter(stripe_customer=id).first()
    user = None
    if profile:
      user = profile.user
    return user

def restore_membership(user, plan, token_granted, images_granted, stripe_subscription_id):
    """Resotre the membership according to the plan"""
    print("Plan :", plan)
    
    print("The credits granted", token_granted)
    subscription_data = {
        "status": "active",
        "plan": plan,
        "stripe_subscription_id": stripe_subscription_id,
    }
    SubscriptionT.objects.filter(user=user).update(**subscription_data)
    features = {"token_limits":int(token_granted), 
                "images":0,
                "images_limits":images_granted,
                "tokens":0,
        }    
    print("Updating the features for the user")
    FeaturesT.objects.filter(user=user).update(**features)
    print("Features created successfully")
