from django.urls import path, include
from . import views

urlpatterns = [
    path('register_ticket', view=views.register_ticket),
    path('camera_triggered', view=views.camera_triggered),
]
