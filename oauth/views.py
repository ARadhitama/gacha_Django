from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt
import json
from oauth.models import UserProfile

@csrf_exempt
def login_account(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
    except Exception as e:
        return JsonResponse({'message': str(e)})

    user_check = authenticate(request, username=username, password=password)

    if user_check is not None:
        payload = { 'username': user_check.username, 't_open_id': user_check.t_open_id}
        jwt_token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

        return JsonResponse({'token': jwt_token.decode('utf-8')}, status=200)
    else:
        return JsonResponse({'message': "invalid username/password"}, status=401)

@csrf_exempt
def check_account(request):
    try:
        jwt_token = request.headers.get('authorization', None)
    except Exception as e:
        return JsonResponse({'message': str(e)})

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return JsonResponse({'message': "Invalid Token"}, status=401)
    else:
        return JsonResponse({'message': "Not Authorized"}, status=401)
    return JsonResponse(payload, status=200)

@csrf_exempt
def create_new_user(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        diamonds = data['diamonds']
        t_open_id = data['t_open_id']
        UserProfile.objects.create_user(username, password, diamonds, t_open_id)
    except Exception as e:
        return JsonResponse({'message': str(e)})

    return JsonResponse({'message': "User Created"})