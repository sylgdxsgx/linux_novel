from django.db import models

# Create your models here.

class Event(models.Model):
	'''发布会表'''
	name = models.CharField('发布会标题',max_length=100)
	limit = models.IntegerField('参加人数')
	status = models.BooleanField('状态')
	address = models.CharField('地址',max_length=200)
	start_time = models.DateTimeField('发布会时间')
	create_time = models.DateTimeField('创建时间',auto_now=True)

	def __str__(self):
		return self.name

class Guest(models.Model):
	'''嘉宾表'''
	event = models.ForeignKey(Event,on_delete=models.deletion.CASCADE)
	realname = models.CharField('姓名',max_length=64)
	phone = models.CharField('手机号',max_length=16)
	email = models.EmailField('邮箱')
	sign = models.BooleanField('签到时间')
	create_time = models.DateTimeField('创建时间',auto_now=True)

	class Meta:
		unique_together = ("event","phone")

	def __str__(self):
		return self.realname
