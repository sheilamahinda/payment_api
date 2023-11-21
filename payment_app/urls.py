# urls.py

from django.urls import path
from .views import paytm_payment_verification

urlpatterns = [
    path('paytm-verification/', paytm_payment_verification, name='paytm_payment_verification'),
    # Add other URL patterns as needed
]

