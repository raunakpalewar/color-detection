from django.urls import path
from .views import ColorAPIView

urlpatterns = [
    path('color-info/',ColorAPIView.as_view(),name='color-info'),
]
