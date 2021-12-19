# Generated by Django 3.2 on 2021-12-19 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentpost', to='core.post', verbose_name='Share Post'),
        ),
    ]
