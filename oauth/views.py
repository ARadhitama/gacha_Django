from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt
import json

@csrf_exempt
def login_account(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user_check = authenticate(request, username=username, password=password)

    if user_check is not None:
        payload = { 'username': user_check.username, 't_open_id': user_check.t_open_id,}
        jwt_token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

        return JsonResponse({'token': jwt_token.decode('utf-8')}, status=200)
    else:
        return JsonResponse({'message': "invalid username/password"}, status=401)

def check_account(request):
    if 'access_token' in request.header:
        token = request.headers['access_token']
        data = jwt.decode(token, setting.JWT_SECRET, settings.JWT_ALGORITHM)
        data_username = data['username']
        user_data = User.objects.filter(username=username)[0]

        username = user_data['username']
        t_open_id = user_data['t_open_id']

        return JsonResponse({'username': username, 't_open_id': t_open_id}, status=200)
    else:
        return JsonResponse({'message': "Invalid Token"}, status=401)