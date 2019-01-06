# Generated by Django 2.0 on 2018-01-19 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='机器名称')),
                ('ip', models.GenericIPAddressField(verbose_name='ip地址')),
                ('password', models.CharField(max_length=32, verbose_name='Password')),
            ],
        ),
        migrations.CreateModel(
            name='Modular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='模块名称')),
                ('svn', models.CharField(max_length=128, verbose_name='SVN路径')),
                ('main', models.CharField(max_length=128, verbose_name='主文件')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='功能点')),
                ('svn', models.CharField(max_length=128, verbose_name='SVN路径')),
                ('main', models.CharField(max_length=128, verbose_name='主文件')),
                ('modular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app02.Modular', verbose_name='所属模块')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='项目名称')),
                ('svn', models.CharField(max_length=128, verbose_name='SVN路径')),
            ],
        ),
        migrations.CreateModel(
            name='TestConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_root_dir', models.CharField(max_length=128, verbose_name='测试目录')),
                ('current_stamp', models.IntegerField(verbose_name='当前时间戳')),
            ],
        ),
        migrations.CreateModel(
            name='TestInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.IntegerField(verbose_name='时间戳')),
                ('test_list', models.CharField(max_length=1024, verbose_name='测试集合')),
                ('machine_list', models.CharField(max_length=1024, verbose_name='执行机合集')),
                ('status', models.IntegerField(verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='TestInfo_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.IntegerField(verbose_name='时间戳')),
                ('test_case', models.CharField(max_length=10, verbose_name='测试项')),
                ('status', models.IntegerField(verbose_name='状态')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app02.Machine', verbose_name='执行机')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserSave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='用户名')),
                ('test_case', models.TextField(verbose_name='测试项')),
                ('machine_case', models.TextField(verbose_name='机器')),
            ],
        ),
        migrations.AddField(
            model_name='modular',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app02.Project', verbose_name='所属项目'),
        ),
    ]
