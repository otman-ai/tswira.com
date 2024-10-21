from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from app.admin import custom_admin_site  # Import the custom admin site
from django.conf.urls.static import static

urlpatterns = []
if settings.DEBUG:
    urlpatterns = [
        path("admin/", admin.site.urls) ,
        path('admin-related/', custom_admin_site.urls),  # Use the custom admin site
        path("api/", include("app.urls")),

    ]
else:

    urlpatterns = [
        path("api/", include("app.urls")),
    ]