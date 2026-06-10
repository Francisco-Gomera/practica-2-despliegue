from django.shortcuts import render
from django.http import JsonResponse
from .models import Preference
from users_view.models import User
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from services.spotifyservices import get_spotify_token_sync, search_spotify_song
import httpx
import asyncio

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def preference_create(request, user_id, *args, **kwargs):
    try:
        # Verificar que el usuario existe
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({
                'success': False,
                'message': f'el usuario {user_id} no existe'
            }, status=404)
        data = json.loads(request.body)
        song = data.get('song') or data.get('cancion')
        artist = data.get('artist') or data.get('artista')
        if not song or not artist:
            return JsonResponse({
                'success': False,
                'message': 'los campos "song" y "artist" son obligatorios'
            }, status=400)
        Preference.create(user_id, song, artist)
        return JsonResponse({
            'success': True,
            'message': 'preferencia creada exitosamente'
        }, status=201)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'error al crear preferencia: {str(e)}'
        }, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def preference_read_by_id(request, user_id, *args, **kwargs):
    try:
        # Verificar que el usuario existe
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({
                'success': False,
                'message': f'el usuario {user_id} no existe'
            }, status=404)
        username = User.objects.get(id=user_id).name
        preferences = list(Preference.objects.filter(user_id=user_id).values())
        if not preferences:
            return JsonResponse({
                'success': False,
                'message': f'el usuario {user_id} no tiene preferencias'
            }, status=404)
        
        token = get_spotify_token_sync()
        if not token:
            raise ValueError("No se pudo obtener token de Spotify")
        
        # Buscar en Spotify de forma async usando asyncio.run()
        async def fetch_preferences():
            async with httpx.AsyncClient() as client:
                resultados_spotify = []
                for row in preferences:
                    cancion_db = row['song']
                    artista_db = row['artist']
                    resultado = await search_spotify_song(client, token, cancion_db, artista_db)
                    resultados_spotify.append(resultado)
                return resultados_spotify
        
        resultados_spotify = asyncio.run(fetch_preferences())

        return JsonResponse({
            'success': True,
            'message': f'preferencias del usuario {user_id} obtenidas',
            'usuario': username,
            'total': len(preferences),
            'data': preferences,
            'spotify_results': resultados_spotify
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'error al obtener preferencias: {str(e)}'
        }, status=400)
            
        
@csrf_exempt
@require_http_methods(["PUT"])
def preference_update(request, id, *args, **kwargs):
    try:
        preference = Preference.objects.get(id=id)
        data = json.loads(request.body)
        song = data.get('song') or data.get('cancion')
        artist = data.get('artist') or data.get('artista')
        if song:
            preference.song = song
        if artist:
            preference.artist = artist
        preference.save()
        return JsonResponse({
            'success': True,
            'message': f'preferencia {id} actualizada exitosamente'
        })
    except Preference.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': f'preferencia {id} no encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'error al actualizar preferencia: {str(e)}'
        }, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
@transaction.atomic
def preference_delete(request, id, *args, **kwargs):
    try:
        preference = Preference.objects.get(id=id)
        preference.delete()
        return JsonResponse({
            'success': True,
            'message': f'preferencia {id} eliminada exitosamente'
        })
    except Preference.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': f'preferencia {id} no encontrada'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'error al eliminar preferencia: {str(e)}'
        }, status=400)