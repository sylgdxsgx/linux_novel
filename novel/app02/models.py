from django.db import models

# Create your models here.

#这个类是用来生成数据库表的,这个类必须集成models.Model
#同步数据库
#python manage.py createsuperuser
#python manage.py makemigrations
#python manage.py migrate
class UserInfo(models.Model):
    '保存用户名和密码'
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
class Project(models.Model):
    '一个项目表，保存项目名、路径、'
    #ID会自动创建
    name = models.CharField('项目名称',max_length=32)
    svn = models.CharField('SVN路径',max_length=128)

class Modular(models.Model):
    '''保存已经记录的（可执行的）各项目的模块,显示在Content中
        可能出现同名，所有先找项目、再找模块'''
    name = models.CharField('模块名称',max_length=32)
    svn = models.CharField('SVN路径',max_length=128)
    main = models.CharField('主文件',max_length=128)
    project = models.ForeignKey(Project,verbose_name='所属项目',on_delete=models.deletion.CASCADE)

class Point(models.Model):
    '''保存已经记录的（可执行的）各项目的功能点,显示在Content中
        可能出现同名，所有先找项目、再找模块、再找功能点'''
    name = models.CharField('功能点',max_length=32)
    svn = models.CharField('SVN路径',max_length=128)
    main = models.CharField('主文件',max_length=128)
    modular = models.ForeignKey(Modular,verbose_name='所属模块',on_delete=models.deletion.CASCADE)

class Machine(models.Model):
    name = models.CharField('机器名称',max_length=32)
    ip = models.GenericIPAddressField('ip地址')
    password = models.CharField('Password',max_length=32) #先用做密码吧

class UserSave(models.Model):
    '''保存用户保存的数据'''
    name = models.CharField('用户名',max_length=32)
    test_case = models.TextField('测试项')
    machine_case = models.TextField('机器')

class TestConfig(models.Model):
    '''测试配置的保存'''
    test_root_dir = models.CharField('测试目录',max_length=128)
    current_stamp = models.IntegerField('当前时间戳')

class TestList(models.Model):
    '''测试列表，每次测试的所有数据都在这里'''
    time_stamp = models.IntegerField('时间戳')
    test_list = models.CharField('测试集合',max_length=4096)
    register_hub = models.CharField('Hub节点',max_length=128)

class TestInfo(models.Model):
    '''测试主列表'''
    time_stamp = models.IntegerField('时间戳')
    test_list = models.CharField('测试集合',max_length=1024)
    machine_list = models.CharField('执行机合集',max_length=1024)
    status = models.IntegerField('状态')

class TestInfo_Detail(models.Model):
    '''测试详情表'''
    time_stamp = models.IntegerField('时间戳')
    test_case = models.CharField('测试项',max_length=10)
    machine = models.ForeignKey(Machine,verbose_name='执行机',on_delete=models.deletion.CASCADE)
    status = models.IntegerField('状态')
