from django.urls import path
from .views import (
    googleLogin, create_generated_photo, GeneratedPhotosView,
    webhook,billing, checkout,get_user_images,user_features_subscription_view,
    UpdateJobStatusPhotoView, JobStatusPhotoView, upload_image
)

urlpatterns = [
    path("auth", googleLogin, name="googleLogin"),
    path("create", create_generated_photo, name="create_photos"),
    path("get_photos", GeneratedPhotosView.as_view(), name="get_photos"),
    path("webhook", webhook, name="webhook"),
    path("billing", billing, name="billing"),
    path("checkout", checkout, name="checkout"),
    path("update-photojob-status", UpdateJobStatusPhotoView, name="update_faceless_job_status"),
    path("photojob-status/", JobStatusPhotoView.as_view(), name="get_faceless_job_status"),
    path("upload_image", upload_image, name="upload_images"),
    path("get_user_images", get_user_images, name="get_user_images"),
    path("get_user", user_features_subscription_view, name="user_features_subscription_view"),
]
