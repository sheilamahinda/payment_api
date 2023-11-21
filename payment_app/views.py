# views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def paytm_payment_verification(request):
    if request.method == 'POST':
        # Your Paytm merchant key
        merchant_key = 'your_merchant_key'

        # Get the POST data from the Paytm server
        data = {k: request.POST[k] for k in request.POST.keys()}

        # Verify the checksum
        checksum = data.pop('CHECKSUMHASH')
        is_checksum_valid = verify_checksum(data, merchant_key, checksum)

        if is_checksum_valid:
            # Check if the payment status is success
            if data['STATUS'] == 'TXN_SUCCESS':
                # Perform any additional verification or processing as needed
                # You can update your database, send confirmation emails, etc.

                # Return a success response
                return JsonResponse({'status': 'success', 'message': 'Payment successfully verified'})

            else:
                # Handle other payment statuses (e.g., TXN_FAILURE, PENDING)
                return JsonResponse({'status': 'failure', 'message': 'Payment verification failed'})

        else:
            # Checksum verification failed
            return JsonResponse({'status': 'failure', 'message': 'Checksum verification failed'})

    else:
        # Invalid HTTP method
        return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})

def verify_checksum(data, merchant_key, checksum):
    import hashlib
    import hmac

    # Create a string by concatenating all the POST parameters
    message = '|'.join(data[key] for key in sorted(data.keys()))

    # Append the merchant key to the message
    message += '|' + merchant_key

    # Calculate the checksum using SHA256 and encode in base64
    generated_checksum = hmac.new(merchant_key.encode(), message.encode(), hashlib.sha256).hexdigest()

    # Compare the generated checksum with the received checksum
    return generated_checksum == checksum
from django.shortcuts import render

# Create your views here.
