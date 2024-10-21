import gradio as gr
import replicate
import urllib.parse

import requests
from aws_utils import *

BACKEND_URL = os.getenv("BACKEND_URL")

def download_image(image_url, image_path):
    response = requests.get(image_url, stream=True)

    with open(image_path ,"wb") as file:
      for chunk in response.iter_content(chunk_size=1024):
          if chunk:
              file.write(chunk)
    print(f"Image downloaded successfully to {image_path}.")
    return True
    
def get_url_by_name(musics, name):
    for music in musics:
        if music["name"] == name:
            return music["url"]
    return None  # Return None if the name is not found
    
def update_job_status(data, user_token):
    if user_token and "job_id" in data :
        print("Updating the job status")
        print("Job status: ", data["status"])
        print("User token ", user_token)
        api_url = BACKEND_URL + 'update-photojob-status'

        headers = {
            'Authorization':f'Token {user_token}',
            'Content-Type':'application/json',
        }
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            print("Successfully updated the job status to ", data["status"])
            return True
        else :
            print("Failed to update the job status: ", response)
            return None
    else:
        return None

# Function to generate images using Replicate API
def generate_image(prompt, num_steps, style_name, input_images, num_outputs, guidance_scale, negative_prompt, style_strength_ratio, job_id, user_token):
    s3_client = Initialize_s3()
    urls = input_images.split(',')
    input_prompt = {
            "prompt": prompt,
            "num_steps": num_steps,
            "style_name": style_name,
            "num_outputs": 1,
            "guidance_scale": guidance_scale,
            "negative_prompt": negative_prompt,
            "style_strength_ratio": style_strength_ratio
    }

    for l in range(len(urls)):
        if l == 0:
            input_prompt["input_image"] = urls[0]
        else:
            input_prompt[f"input_image{l+1}"] = urls[l]
    print(input_prompt)
    for i in range(num_outputs):
        # Convert uploaded files into URLs or paths (assume files are URLs for simplicity)        
        # Assign images to the respective inputs (using up to 4 images)
        # Assuming input_images is a list of uploaded file paths
        # Call the Replicate model with the given parameters
        try:
            outputs = replicate.run(
                "tencentarc/photomaker:ddfc2b08d209f9fa8c1eca692712918bd449f695dabb4a958da31802a9570fe4",
                input=input_prompt
            )
            # outputs = ["https://replicate.delivery/pbxt/KFkSv1oX0v3e7GnOrmzULGqCA8222pC6FI2EKcfuCZWxvHN3/newton_0.jpg", 
            #            "https://replicate.delivery/pbxt/KFkSv1oX0v3e7GnOrmzULGqCA8222pC6FI2EKcfuCZWxvHN3/newton_0.jpg", 
            #            "https://replicate.delivery/pbxt/KFkSv1oX0v3e7GnOrmzULGqCA8222pC6FI2EKcfuCZWxvHN3/newton_0.jpg"]
            print('Outputs: ', outputs)
            out = outputs[0]
        except:
            outputs = replicate.run(
                "tencentarc/photomaker:ddfc2b08d209f9fa8c1eca692712918bd449f695dabb4a958da31802a9570fe4",
                input=input_prompt
            )
            # outputs = ["https://replicate.delivery/pbxt/KFkSv1oX0v3e7GnOrmzULGqCA8222pC6FI2EKcfuCZWxvHN3/newton_0.jpg", 
            #            "https://replicate.delivery/pbxt/KFkSv1oX0v3e7GnOrmzULGqCA8222pC6FI2EKcfuCZWxvHN3/newton_0.jpg", 
            #            "https://replicate.delivery/pbxt/KFkSv1oX0v3e7GnOrmzULGqCA8222pC6FI2EKcfuCZWxvHN3/newton_0.jpg"]
            print('Outputs: ', outputs)
            out = outputs[0]
        file_path = job_id + "." + out.split(".")[-1]
        key_ath = job_id +f"/image_{i}" + "." + out.split(".")[-1]
        
        print("File path:", file_path)
        download_image(out, file_path)
        image_link = upload_to_s3(s3_client, file_path, key_ath, "https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com",
                                  "uploadedvideosyoutube", "generated/")
        print("Image link: ", image_link)
        update_job_status(data={"status":"finish","job_id":job_id, "image":image_link, "key":i},user_token=user_token)
        os.remove(file_path)
    # Return all generated images as a list (for the gallery)
    
    return outputs if outputs else ["Error in generating images"]

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Replicate Image Generator")

    with gr.Row():
        prompt = gr.Textbox(label="Prompt", value="A photo of a scientist img receiving the Nobel Prize")
        job_id = gr.Textbox(label="Job id")
        user_token = gr.Textbox(label="User token")
        
        style_name = gr.Dropdown(label="Style Name", value="Photographic (Default)", choices=["Photographic (Default)", "Cinematic", "Disney Charactor", "Digital Art", "Fantasy art", "Neonpunk", "Enhance", "Lowpoly", "Comic book", "Line art"])
    
    with gr.Row():
        num_steps = gr.Number(label="Num Steps", value=50)
        num_outputs = gr.Number(label="Num Outputs", value=1)
    
    with gr.Row():
        files = gr.Textbox(
        label="Enter image URLs (comma-separated)",
        value="https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/WhatsApp+Image+2024-09-20+at+19.10.30+(2).jpeg,https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/WhatsApp+Image+2024-09-20+at+19.10.30.jpeg,https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/WhatsApp+Image+2024-09-20+at+19.10.30+(1).jpeg,https://uploadedvideosyoutube.s3.eu-north-1.amazonaws.com/WhatsApp+Image+2024-09-20+at+19.10.30+(1).jpeg",
        )

    with gr.Row():
        guidance_scale = gr.Number(label="Guidance Scale", value=5)
        style_strength_ratio = gr.Number(label="Style Strength Ratio", value=20)
    
    negative_prompt = gr.Textbox(label="Negative Prompt", value="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry")

    output_gallery = gr.Gallery(label="Generated Images")

    submit_button = gr.Button("Generate Image")
    
    submit_button.click(generate_image, 
                        inputs=[prompt, num_steps, style_name, files, num_outputs, guidance_scale, negative_prompt, style_strength_ratio, job_id, user_token], 
                        outputs=output_gallery)

if __name__ == "__main__":
    demo.launch()
