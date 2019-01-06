# Generated by Django 2.0.3 on 2018-03-13 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.IntegerField(verbose_name='时间戳')),
                ('test_list', models.CharField(max_length=4096, verbose_name='测试集合')),
                ('register_hub', models.CharField(max_length=128, verbose_name='Hub节点')),
            ],
        ),
    ]
