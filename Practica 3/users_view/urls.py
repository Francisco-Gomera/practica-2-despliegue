from django.urls import path
from .views import user_create, user_update, user_delete, user_read, user_read_by_id

urlpatterns = [
    path('crear/', user_create, name='user-create'),
    path('leer/', user_read, name='user-read'),
    path('leer/<int:id>/', user_read_by_id, name='user-read-by-id'),
    path('actualizar/<int:id>/', user_update, name='user-update'),
    path('eliminar/<int:id>/', user_delete, name='user-delete'),
]