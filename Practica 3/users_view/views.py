from django.shortcuts import render
from django.http import JsonResponse
from .models import User
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST"])
def user_create(request, *args, **kwargs):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        User.create(name)
        body = {
            'message': 'usuario creado'
        }
        return JsonResponse(body)
    except Exception as e:
        body = {
            'message': f'error al crear usuario: {str(e)}'
        }
        return JsonResponse(body, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def user_read(request, *args, **kwargs):
    try:
        users = list(User.objects.values())
        body = {
            'data': users
        }
        return JsonResponse(body)
    except Exception as e:
        body = {
            'message': f'error al obtener usuarios: {str(e)}'
        }
        return JsonResponse(body, status=400)
    
@csrf_exempt
@require_http_methods(["GET"])
def user_read_by_id(request, id, *args, **kwargs):
    try:
        users = list(User.objects.values().filter(id=id))   
        body = {
            'data': users
        }
        return JsonResponse(body)
    except Exception as e:
        body = {
            'message': f'error al obtener usuarios: {str(e)}'
        }
        return JsonResponse(body, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def user_update(request, id, *args, **kwargs):
    try:
        data = json.loads(request.body)
        new_name = data.get('name')
        User.update(new_name, id)
        body = {
            'message': 'usuario actualizado'
        }
        return JsonResponse(body)
    except Exception as e:
        body = {
            'message': f'error al actualizar usuario: {str(e)}'
        }
        return JsonResponse(body, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def user_delete(request, id, *args, **kwargs):
    try:
        user = User.objects.get(id=id)
        user.delete()
        body = {
            'message': 'usuario eliminado'
        }
        return JsonResponse(body)
    except Exception as e:
        body = {
            'message': f'error al eliminar usuario: {str(e)}'
        }
        return JsonResponse(body, status=400)   