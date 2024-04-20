# Generated by Django 5.0.4 on 2024-04-19 19:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_network", "0002_comment_created_at_post_updated_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="posts",
        ),
        migrations.AddField(
            model_name="post",
            name="users",
            field=models.ForeignKey(
                default=None, on_delete=django.db.models.deletion.CASCADE, to="social_network.user"
            ),
            preserve_default=False,
        ),
    ]