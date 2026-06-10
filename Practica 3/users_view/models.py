from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'usuarios'
        
    @classmethod
    def create(cls, name):
        if not name:
            raise ValueError("El nombre es obligatorio")
        cls.objects.create(name=name)

    @classmethod
    def update(cls, new_name, id):
        if not new_name:
            raise ValueError("El nuevo nombre es obligatorio")
        user = cls.objects.get(id=id)
        user.name = new_name
        user.save()