# Generated by Django 3.1.5 on 2021-03-03 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTimeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('basetimemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='forum.basetimemodel')),
                ('title', models.CharField(max_length=30)),
                ('file', models.FileField(upload_to='files')),
            ],
            bases=('forum.basetimemodel',),
        ),
    ]
