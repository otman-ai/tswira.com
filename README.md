# Tswira.com 

tswira.com is image generator tool that can generate up to 100 of images of anyone in different styles

## Video Demo

![Tswira Demo](demo/demo.mp4)

## Project stucture

* client-side: this is the front-end built using react jsx and tailwind css
* photomaker-side: built using gradio , you can deploy it on hugging face (like I did) this is the side that generate the images and send them back to the backend to update its status
* server-side: built using django reset framework 