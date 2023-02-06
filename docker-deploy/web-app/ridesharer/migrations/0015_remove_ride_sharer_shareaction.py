# Generated by Django 4.1.5 on 2023-02-05 22:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ridesharer', '0014_alter_ride_driver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='sharer',
        ),
        migrations.CreateModel(
            name='ShareAction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sharer_num', models.PositiveIntegerField(default=1)),
                ('shared_ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharing_actions', to=settings.AUTH_USER_MODEL)),
                ('sharer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_actions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]