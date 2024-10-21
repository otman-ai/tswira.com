from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.http import  HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt

from firebase_admin import auth

from django.contrib.auth.tokens import default_token_generator
import asyncio
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import json
import requests
from .models import *
from .helpers import *
from .serializer import *

@csrf_exempt
@api_view(["POST"])
def googleLogin(request):
    data = json.loads(request.body)
    print("Loaded data from Google SignIn: ", data)
    token = data["token"]
    try:
        decoded_token = auth.verify_id_token(token)
        print("Decoed token: ", decoded_token)
        uid = decoded_token["uid"]
        print("UID: ", uid)
        email = str(decoded_token["email"]).lower()
        print("Email: ", email)
        username = str(decoded_token["name"]) # Use name for username replace(" ", "_") 
        print("Username: ", username)
        user, created = User.objects.get_or_create(email=email, 
                                                    is_active=True, 
                                                    username=username)

        print("Customer created")
        if created :
            user_count = User.objects.count()
            if user_count >= 500:
                user.delete()
                if WaitListT.objects.filter(email=email).exist:
                    return Response({"message":"You are already in the waitlist"}, status=400)
                WaitListT.objects.create(email=email, source="google_signup")
                return Response({"message":"We no longer accept more users, you have been added you to the waitlist. Once we accept more we will let you know"}, 
                                status=400)
            handle_user_created(user)
            gg_profile = GoogleProfileT.objects.create(user=user, uid=uid, profile=decoded_token["picture"])
            gg_profile.save()
        else:
            print("User already logged in")
            gg_profile = GoogleProfileT.objects.get(user=user)

        token , _ = Token.objects.get_or_create(user=user)   
        return  Response({'token': token.key})
    except Exception as e:
        print("Error while loggin with google: ", str(e))
        return Response({"message":"Error while loggin"}, status=400)

def get_user_token(request):
    user_token = request.data.get("user_token")
    auth_header = request.headers.get("Authorization", "")
    user_token= auth_header.split(" ")[-1]
    return user_token

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_features_subscription_view(request):
    subscription = SubscriptionT.objects.get(user=request.user)
    feature = FeaturesT.objects.get(user=request.user)
    response = requests.post(
    "https://api.stripe.com/v1/customer_sessions",
    auth=(settings.STRIPE_PRIVATE_KEY, ''),
    data={
        "customer": UserProfileT.objects.get(user=request.user).stripe_customer,
        "components[pricing_table][enabled]": "true"
    }
)
    print(response.json())
    client_secret = response.json()["client_secret"]
    response_data = {
        'user': request.user.username,
	'email':request.user.email,
        'client_secret':client_secret,
        'profile': GoogleProfileT.objects.get(user=request.user).profile,
        'subscription': {
            'plan': subscription.plan,
            'status': subscription.status,
        },
        'feature': {
            'tokens': feature.tokens,
            'token_limits': feature.token_limits,
            'images': feature.images,
            'images_limits': feature.images_limits,
        }
    }

    return JsonResponse(response_data, status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_generated_photo(request):
    user = request.user
    payload = request.data
    num_outputs = payload["num_outputs"]
    imgs = payload["selectedImages"]
    payload["user"] = user.pk
    serializer = GeneratedPhotoSerialize(data=payload)

    if not imgs:
        return Response({"message": "images is required"}, status=400)
    if not payload["prompt"]:
        return Response({"message": "Prompt can't be blank"}, status=status.HTTP_400_BAD_REQUEST)
    if not payload["style_name"]:
        return Response({"message": "Style name can't be blank"}, status=status.HTTP_400_BAD_REQUEST)
    if not payload["prompt"]:
        return Response({"message": "Prompt can't be blank"}, status=status.HTTP_400_BAD_REQUEST)

    if num_outputs == 0 or not num_outputs or not isinstance(num_outputs, int):
        return Response({"message": "Number of outputs is not valid"}, status=status.HTTP_400_BAD_REQUEST)

    subscription = SubscriptionT.objects.get(user=user)
    features = get_object_or_404(FeaturesT, user=user)
    if features.tokens + num_outputs  > features.token_limits:
        return Response({"message": "Insufficient tokens."}, status=400)

    input_images = []
    if len(imgs) > 4:
        imgs = imgs[:4]
    for image in imgs:  # Limit to the first 4 images
        user_image =  UserImageT.objects.filter(user=user, image=image)
        if UserImageT.objects.filter(user=user, image=image).exists():
            input_images.append(UserImageT.objects.get(user=user, image=image).image.url)
        else:
            return JsonResponse({"message": f"Input image {image} does not exist."}, status=400)
    input_images = ",".join(input_images)
    print(input_images)
    # Create GeneratedPhoto instance
    job_id = generate_unique_filename(ext="")
    for i in range(num_outputs):
        generated_photo = GeneratedPhotoT.objects.create(
            user=user,
            status="pending",
            prompt=payload["prompt"],
            style_name=payload["style_name"],
            num_outputs=payload["num_outputs"],
            input_images=input_images,
            user_token=get_user_token(request),
            is_free=subscription.plan.lower() == "free",
            job_id=job_id,
            key=i
        )
        generated_photo.save()

    # Call the generate_photos function
    try:
        result = generate_photos({
            "user_token": generated_photo.user_token,
            "job_id": job_id,
            "prompt": "img " + generated_photo.prompt,
            "style_name": generated_photo.style_name,
            "input_images": generated_photo.input_images,
            "num_outputs": generated_photo.num_outputs,
            "is_free": generated_photo.is_free,
        })
        update_credits(user, generated_photo.num_outputs)
        return Response({"message": "success", "job_id": generated_photo.job_id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        GeneratedPhotoT.objects.filter(user=user, job_id=job_id).update(status="error")
        return JsonResponse({"message": str(e)}, status=500)
    
@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_image(request):
    user = request.user
    if FeaturesT.objects.get(user=user).images + 1 >FeaturesT.objects.get(user=user).images_limits:
        return Response({"message":"Can't upload more images"}, status=400)
    # Check if an image is provided in the request
    if 'image' not in request.FILES:
        return Response({"error": "Image file is required."}, status=400)

    image = request.FILES['image']

    # Check file type
    if not image.name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return Response({"error": "File type not supported. Please upload an image."}, status=400)

    # Check file size (e.g., limit to 5MB)
    max_size = 10 * 1024 * 1024  # 5 MB
    if image.size > max_size:
        return Response({"error": "File size exceeds the limit of 10MB."}, status=400)

    # Create a UserImage instance and save the uploaded image
    user_image = UserImageT(user=request.user, image=image)
    user_image.save()
    FeaturesT.objects.filter(user=user).update(images=FeaturesT.objects.get(user=user).images + 1)
    return Response({"message": "Image uploaded successfully."}, status=201)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_images(request):
    # Fetch all images uploaded by the authenticated user
    user_images = UserImageT.objects.filter(user=request.user)

    # Prepare the response data
    images_data = [
        {
            "id": user_image.id,
	    "image":user_image.image.name,
            "image_url": user_image.image.url,  # URL of the uploaded image
            "uploaded_at": user_image.created_at,  # Assuming you have a created_at field
        }
        for user_image in user_images
    ]

    return Response({"images": images_data}, status=200)

@csrf_exempt
@api_view(["POST"])
def webhook(request):
    webhook_secret = settings.WEBHOOK_SECRET_TSWIRA
    payload = request.body
    
    event = None

    try:
      sig_header = request.META['HTTP_STRIPE_SIGNATURE']
      event = stripe.Webhook.construct_event(
      payload, sig_header, webhook_secret
      )
    except ValueError as e:
    # Invalid payload
      print('Error parsing payload: {}'.format(str(e)))
      return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
      print('Error verifying webhook signature: {}'.format(str(e)))
      return HttpResponse(status=400)
    except Exception as e:
    # Invalid signature
      print('Error verifying webhook signature: {}'.format(str(e)))
      return HttpResponse(status=400)
    event_type = event['type']
    data_object = event['data']['object']

    if event_type == "checkout.session.completed":
        print("checkout.session.completed")
        handle_payment_finished(data_object)
    elif event_type == "invoice.payment.failed":
        handle_payment_failed(data_object)
    elif event_type == "customer.deleted":
        handle_customer_deleted(data_object)
    elif event_type == "customer.subscription.deleted":
        handle_subscription_delete(data_object)

    return JsonResponse({"status": "success"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def billing(request):
    user = request.user
    profile = UserProfileT.objects.get(user=user)
    
    if not profile.stripe_customer:
        return Response({"status": "Customer id not found"}, status=404)
    
    billing_portal_session = stripe.billing_portal.Session.create(
        customer=profile.stripe_customer,
        return_url=settings.FRONT_END_URL,
    )
    
    
    return Response({"message":"success", "url":billing_portal_session.url}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def checkout(request):
    subscription = SubscriptionT.objects.get(user=request.user)
    print("Current Plan: ", subscription.plan)
    profile = UserProfileT.objects.get(user=request.user)
    if subscription.plan == "free":
        try:
            prices = stripe.Price.list(
                lookup_keys=[request.data["lookup_key"]], expand=["data.product"]
            )
            print("Prices: ", prices)
            selected_plan_name = (
                prices.get("data", [{}])[0].get("product", {}).get("name")
            )
            print("Selected plan :", selected_plan_name)
            checkout_session = stripe.checkout.Session.create(
                customer=profile.stripe_customer,
                line_items=[
                    {
                        "price": prices.data[0].id,
                        "quantity": 1,
                    },
                ],
                mode="subscription",
                allow_promotion_codes=True, 
                success_url=settings.FRONT_END_URL
                + "workspace?tab=home?success=true&session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.FRONT_END_URL + "workspace?tab=home",
            )
            print("Url: ", checkout_session.url)
            return Response({"url": checkout_session.url}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse(
                {"status": "error", "details": "Customer not found"}, status=400
            )
    return Response(settings.FRONT_END_URL + "workspace", status=200)

class JobStatusPhotoView(generics.ListCreateAPIView):
    serializer_class = GeneratedPhotoSerialize
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Fetching all fields for the specific user and job_id
        job_id = self.request.query_params.get('job_id')  # Get job_id from query parameters
        return GeneratedPhotoT.objects.filter(user=self.request.user, job_id=job_id)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def UpdateJobStatusPhotoView(request):
    user = request.user
    data = request.data
    print("Data: ", data)
    if  "status" not in data and "job_id" not in data and "image" not in data and "key" not in data:
        return Response({"message":"One or more field required"}, status=400)
    generate_photo = GeneratedPhotoT.objects.filter(user=user, job_id=data["job_id"], key=data["key"])
    if not generate_photos:
        return Response({"message":"Job id deos not exists"}, status=400)
    
    generate_photo.update(**data)
    return Response({'message':"success"}, status=200)

class GeneratedPhotosView(generics.ListCreateAPIView):
    serializer_class = GeneratedPhotoSerialize
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Customizing the queryset to only include specific columns
        return GeneratedPhotoT.objects.filter(user=self.request.user)