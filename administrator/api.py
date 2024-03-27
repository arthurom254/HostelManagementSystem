from django.http import JsonResponse
from .models import UserRegistration, Registration
from django.contrib.auth.models import User
import hashlib
from django.contrib.auth.hashers import check_password
def check_email(request):
    if request.method == 'POST' and 'emailid' in request.POST:
        email = request.POST['emailid']
        if UserRegistration.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists! Try using a new one.', 'color': 'red'})
        else:
            return JsonResponse({'message': 'Email available for registration!!', 'color': 'green'})
    return JsonResponse({}, status=400)

def check_password(request):
    if request.method== 'POST':
    # if request.method == 'POST' and 'oldpassword' in request.POST:

        print(request)
        password = request.POST.get('oldpassword')
        if password:
            print("OK")
            return JsonResponse({'message': 'Password matched.', 'color': 'green'})
        else:
            return JsonResponse({'message': 'Password does not match!', 'color': 'red'})
    return JsonResponse({}, status=400)

def check_room(request):
    if request.method == 'POST' and 'roomno' in request.POST:
        room_no = request.POST['roomno']
        if Registration.objects.filter(roomno=room_no).exists():
            return JsonResponse({'message': 'Seats are already full.', 'color': 'red'})
        else:
            return JsonResponse({'message': 'All seats are available', 'color': 'green'})
    return JsonResponse({}, status=400)
