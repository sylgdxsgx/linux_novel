from django.contrib import admin

# Register your models here.

#导入app02模块
from app02 import models

#注册咱们创建的类,通过他来访问
admin.site.register(models.UserInfo)
admin.site.register(models.Project)
admin.site.register(models.Modular)
admin.site.register(models.Point)
admin.site.register(models.Machine)
admin.site.register(models.UserSave)
admin.site.register(models.TestConfig)
admin.site.register(models.TestInfo)
admin.site.register(models.TestInfo_Detail)
admin.site.register(models.TestList)