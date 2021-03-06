# Generated by Django 3.1.7 on 2021-04-11 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20210410_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumlike',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.forumcomment'),
        ),
        migrations.AlterField(
            model_name='forumlike',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.forumpost'),
        ),
    ]
