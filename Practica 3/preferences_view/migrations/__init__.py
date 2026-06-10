from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('cancion', models.CharField(max_length=100)),
                ('artista', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'preferencias',
            },
        ),
    ]
