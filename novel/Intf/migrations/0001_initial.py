# Generated by Django 2.0.5 on 2018-09-10 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='发布会标题')),
                ('limit', models.IntegerField(verbose_name='参加人数')),
                ('status', models.BooleanField(verbose_name='状态')),
                ('address', models.CharField(max_length=200, verbose_name='地址')),
                ('start_time', models.DateTimeField(verbose_name='发布会时间')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realname', models.CharField(max_length=64, verbose_name='姓名')),
                ('phone', models.CharField(max_length=16, verbose_name='手机号')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('sign', models.BooleanField(verbose_name='签到时间')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Intf.Event')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='guest',
            unique_together={('event', 'phone')},
        ),
    ]
