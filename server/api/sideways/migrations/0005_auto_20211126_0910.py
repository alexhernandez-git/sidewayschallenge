# Generated by Django 3.0.3 on 2021-11-26 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sideways', '0004_auto_20211126_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sideway',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sideways.Place'),
        ),
    ]
