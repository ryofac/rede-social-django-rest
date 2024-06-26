# Generated by Django 5.0.4 on 2024-04-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_network", "0010_alter_user_password"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="name",
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="Email do Usuário"),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=30, verbose_name="Nome"),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=30, verbose_name="Sobrenome"),
        ),
    ]
