# Generated by Django 3.1.7 on 2021-04-04 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20210329_0949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forumlike',
            old_name='posts',
            new_name='post',
        ),
        migrations.AlterField(
            model_name='forumcategory',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.forumcategory'),
        ),
        migrations.AlterField(
            model_name='forumcomment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='forumcomment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.forumcomment'),
        ),
        migrations.AlterField(
            model_name='forumpost',
            name='file',
            field=models.FileField(blank=True, upload_to='files'),
        ),
        migrations.AlterField(
            model_name='forumpost',
            name='tags',
            field=models.ManyToManyField(blank=True, to='forum.ForumTag'),
        ),
    ]