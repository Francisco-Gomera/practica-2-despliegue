from django.db import models

class Preference(models.Model):
    user = models.ForeignKey('users_view.User', on_delete=models.CASCADE, db_column='user_id')
    song = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

    class Meta:
        db_table = 'preferencias'

    @classmethod
    def create(cls, user_id, song, artist):
        if not song or not artist:
            raise ValueError("La canción y el artista son obligatorios")
        # validate user exists
        from users_view.models import User
        if not User.objects.filter(id=user_id).exists():
            raise ValueError("El usuario no existe")
        cls.objects.create(user_id=user_id, song=song, artist=artist)
        