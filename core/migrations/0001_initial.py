# Generated by Django 5.2.2 on 2025-06-29 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subreddit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='subreddit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subreddit'),
        ),
    ]
