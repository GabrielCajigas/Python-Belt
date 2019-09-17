# Generated by Django 2.0.7 on 2019-09-15 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log_in', '0002_auto_20190915_0113'),
        ('DojoBelt_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('trip_start', models.DateTimeField()),
                ('trip_end', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_planned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_trips', to='log_in.Users')),
                ('users_joined', models.ManyToManyField(related_name='joined_trips', to='log_in.Users')),
            ],
        ),
        migrations.RemoveField(
            model_name='books',
            name='user',
        ),
        migrations.DeleteModel(
            name='Books',
        ),
    ]