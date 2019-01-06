from django.db import models

# Create your models here.

class zidetail(models.Model):
	'''保存汉字'''
	zi = models.CharField('字',max_length=10)
	zitype = models.CharField('字体',max_length=10)
	author = models.CharField('作者',max_length=10)
	no = models.CharField('编号(非必填)',max_length=10)
	path = models.FilePathField('文件路径')
	url = models.URLField('网络地址')
	binaryfile = models.BinaryField('二进制文件(先不用它)')
	status = models.BooleanField('下载状态')

	def __str__(self):
		return self.zi

class hanzi(models.Model):
	'''汉字列表'''
	zi = models.CharField('字',max_length=10)
	x = models.CharField('行书',max_length=1024)
	c = models.CharField('草书',max_length=1024)
	k = models.CharField('楷书',max_length=1024)
	l = models.CharField('隶书',max_length=1024)
	z = models.CharField('篆书',max_length=1024)
	g = models.CharField('钢笔',max_length=1024)
	o = models.CharField('其它',max_length=1024)
	count = models.IntegerField('更新次数')

	def __str__(self):
		return self.zi
