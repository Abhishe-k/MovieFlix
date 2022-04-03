# Generated by Django 4.0.2 on 2022-04-02 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0014_order_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('A', 'Approved'), ('P', 'Pending')], default='P', max_length=2),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.PositiveIntegerField(default=0)),
                ('username', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('movie_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]