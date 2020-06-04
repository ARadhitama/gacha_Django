from django.shortcuts import render
import random
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt
import json
from oauth.models import UserProfile
from api.models import itemList, itemSpinHistory

@csrf_exempt
def use_diamond(id, amount):
    user=UserProfile.objects.get(t_open_id=id)
    user.diamonds = user.diamonds-amount
    user.save()

@csrf_exempt
def spin_gacha(request):

    jwt_token = request.headers.get('authorization', None)

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return JsonResponse({'message': "Invalid Token"}, status=401)
    else:
        return JsonResponse({'message': "Not Authorized"}, status=401)
    
    Gacha_itemlist = []
    Gacha_chance = []

    for item in itemList.objects.all():
        Gacha_itemlist.append({'item_id': item.item_id, 'item_name': item.item_name})
        Gacha_chance.append(item.chance)

    data = json.loads(request.body)
    spin_type = data['spin_type']
    owned_diamonds = UserProfile.objects.values_list('diamonds', flat=True).get(t_open_id=payload['t_open_id'])

    print(owned_diamonds)

    if (spin_type==1):
        roll_cost = 10
    else:
        roll_cost = 90

    if 'spin_type' in data:
        print("1")
        if (spin_type==1) or (spin_type==10):
            if (owned_diamonds>=roll_cost):

                use_diamond(payload['t_open_id'], roll_cost)

                item_roll = random.choices(Gacha_itemlist, Gacha_chance, k=spin_type)


                for item in item_roll:
                    itemSpinHistory.objects.create(item_id=item['item_id'], item_name=item['item_name'], spin_type=spin_type, t_open_id=payload['t_open_id'])

            else:
                JsonResponse({'message': "Not enough diamond"}, status-403)
        else:
            JsonResponse({'message': "Invalid spin type"}, status=503)
    else:
        JsonResponse({'message': "Invalid request body"}, status=403)

    return JsonResponse({'result': item_roll}, status=200)

def spin_history(request):

    jwt_token = request.headers.get('authorization', None)

    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return JsonResponse({'message': "Invalid Token"}, status=401)
    else:
        return JsonResponse({'message': "Not Authorized"}, status=401)

    gacha_history = []
    item = itemSpinHistory.objects.filter(t_open_id=payload['t_open_id']).order_by('-created_at')
    for gacha_item in item:
        gacha_history.append({'item_id': gacha_item.item_id, 'item_name': gacha_item.item_name, 'created_at': gacha_item.created_at, 'spin_type': gacha_item.spin_type})
    
    return JsonResponse({'result': gacha_history}, status=200)

