from django.urls import path
from .vk_settings import CALLBACK_URL
from .views import CallBackView
from .admin import admin_site

urlpatterns = [
    path(CALLBACK_URL, CallBackView.as_view(), name='callback_url'),
    path('vk-admin/', admin_site.urls)
]