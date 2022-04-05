# Generated by Django 4.0.1 on 2022-04-04 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0016_usertoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='userlikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('likes', models.BooleanField(default=False)),
                ('movie', models.CharField(max_length=100)),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
            ],
        ),
    ]