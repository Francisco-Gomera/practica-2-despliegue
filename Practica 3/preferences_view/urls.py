from django.urls import path
from .views import preference_create, preference_update, preference_delete, preference_read_by_id

urlpatterns = [
    path('crear/<int:user_id>/', preference_create, name='preference-create'),
    path('leer/<int:user_id>/', preference_read_by_id, name='preference-read-by-id'),
    path('actualizar/<int:id>/', preference_update, name='preference-update'),
    path('eliminar/<int:id>/', preference_delete, name='preference-delete'),
]