# Generated by Django 5.0.4 on 2024-04-20 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_network", "0005_alter_user_followers"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="content",
            field=models.CharField(default="Nao Especificado", max_length=255, verbose_name="Conteúdo"),
            preserve_default=False,
        ),
    ]
