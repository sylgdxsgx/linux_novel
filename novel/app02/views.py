import sys
import time
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django.shortcuts import redirect
# from django.views.decorators.cache import cache_page
from django.core.cache import cache
import json,threading
#如果想使用数据库,需要先导入(需要在开头导入)
from app02 import models
from app02 import func
#分别是：取消当前函数防跨站请求伪造功能、强制使用当前函数防跨站请求伪造功能。即便settings中设置了(没设置)全局中间件。
from django.views.decorators.csrf import csrf_exempt,csrf_protect 
from .forms import UserForm
# from django.contrib.auth import authenticate,login,logout	#登入和退出
# from django.contrib.auth.decorators import login_required	#验证用户是否登入
# from django.contrib import auth 


def tologin(request):
    return redirect('/app02/login')

@csrf_exempt
def regist(request):
    dic = {}
    '''
    dic = {}
    dic['userform'] = UserForm()
    if request.method == 'POST':
	    userform = UserForm(request.POST)
	    if userform.is_valid():
		    username = userform.cleaned_data['username']
		    password = userform.cleaned_data['password']
			
		    user = models.UserInfo.objects.filter(username__exact=username)
		    if user:
			    dic['message'] = '该用户已经存在'
		    else:
			    models.UserInfo.objects.create(username=username,password=password)
			    dic['message'] = '注册成功！'
		    return render_to_response('regist.html',dic)
    return render_to_response('regist.html',dic)
    '''
    if request.method == 'POST':
	    username = request.POST.get('username')
	    password = request.POST.get('password')
		
	    user = models.UserInfo.objects.filter(username__exact=username)
		
	    dic['status'] = 0
	    if user:
		    dic['msg'] = '该用户已经存在，请重新注册。'
	    else:
		    models.UserInfo.objects.create(username=username,password=password)
		    dic['msg'] = '注册成功，现在去登入吧。'
	    return HttpResponse(json.dumps(dic))
	
@csrf_exempt
def reset_password(request):
    dic = {}
    if request.method == 'POST':
	    username = request.POST.get('username')
	    password = request.POST.get('password')
		
	    user = models.UserInfo.objects.filter(username__exact=username)
		
	    dic['status'] = 0
	    if not user:
		    dic['msg'] = '该用户不存在，请重新输入。'
	    else:
		    user = models.UserInfo.objects.get(username=username)
		    user.password = password
		    user.save()
		    dic['msg'] = '修改成功，现在去登入吧。'
	    return HttpResponse(json.dumps(dic))
		
@csrf_exempt
def login(request):
    if request.method == 'POST':		#当提交表单时
		
	    userform = UserForm(request.POST)	#form 表单
		
	    if userform.is_valid():	#如果数据合法
		    username = userform.cleaned_data['username']
		    password = userform.cleaned_data['password']
		    
		    user = models.UserInfo.objects.filter(username__exact=username,password__exact=password)
			
		    if user:
			    response = redirect('/app02/index')
			    #response.set_cookie('username',username,path='/',3600)
			    response.set_signed_cookie('username',username,path='/')
			    return response
			
		    else:	
			    return render_to_response('login.html',{'err_message':'用户名或密码错误，请重新登入','userform':userform})
    else:	#正常访问时
        userform = UserForm()
    return render(request,'login.html',{'userform':userform})

def logout(request):
    response = redirect('/app02/login')
    response.delete_cookie('username')
    return response

def index(request):
    username = request.COOKIES.get('username')
    if not username:
	    return redirect('/app02/login')
    dic = {}
    try:
        #导航菜单
        pid = request.GET['pid']
        # dic['proj_list'] = models.Project.objects.all()
        dic['mode_list'] = models.Modular.objects.filter(project_id=pid)
        dic['point_list'] = models.Point.objects.filter(modular__project_id=pid)
        return render(request,'include/select_project.html',dic)
    except:
        #登入成功
	    username = request.COOKIES.get('username','')
	    try:
		    obj = models.UserSave.objects.get(name=username)
		    temp_list = obj.test_case
		    temp_list = eval(temp_list)
	    except:
		    temp_list = None
	    dic['test_list'] = json.dumps(temp_list)       #发送数组
	    dic['proj_list'] = models.Project.objects.all()
	    dic['proj_info'] = ["看到此页，是因为您尚未选择项目，或者您需要添加新的项目",]
        # return render(request,'index.html',dic)
	    return render_to_response('index.html',dic)

@csrf_exempt
def addproject(request):
    dic = {}
    if request.method == "POST":
        name = request.POST['name']
        svn = request.POST['svn']
        action = request.POST['action']
        if name=="" or svn=="":
            dic['status'] = '不能为空'
        else:
            if action=='add':   #添加项目
                try:
                    models.Project.objects.get(name=name)
                except Exception as e:
                    print(e,'创建新项目')
                    models.Project.objects.create(name=name,svn=svn)
                    pid = models.Project.objects.get(name=name).id
                    dic['new_id'] = pid #仅仅是在添加项目时，更新菜单用到
                    dic['new_name'] = name #仅仅是在添加项目时，更新菜单用到
                else:
                    dic['status'] = '项目名已存在'
            elif action=='modify':      #修改操作，先判断项目id是否正确
                try:
                    project = models.Project.objects.get(id=request.POST['id'])
                except:
                    pass
                else:
                    project.name=name
                    project.svn=svn
                    project.save()
            else:       #禁用操作
                pass
    else:
        #点击菜单添加项目
        pass
    dic['proj_list'] = models.Project.objects.all()
    return render(request,'include/addproject.html',dic)

@csrf_exempt
def addpoint(request):
    dic = {}
    if request.method == "POST":
        action = request.POST['action']
        name = request.POST['name']
        svn = request.POST['svn']
        main = request.POST['main']
        Type = request.POST['Type']
        pid = request.POST['pid']
        mid = request.POST['mid']
        print(request.POST)
        print(svn)
        if action=='add':        #添加模块或者功能点
            if Type == "modular":      #添加模块
                if name=="" or svn =="" or main=="":
                    dic['status'] = '不能为空'
                else:
                    try:
                        models.Modular.objects.filter(project_id=pid).get(name=name)
                    except:
                        project = models.Project.objects.get(id=pid)
                        add_dict = {'name':name,'svn':svn,'main':main,'project':project}
                        models.Modular.objects.create(**add_dict)
                    else:
                        dic['status'] = '模块名已存在'
                dic['mode_list'] = models.Modular.objects.filter(project_id=pid)
            elif Type == "point":     #添加功能点
                if name=="" or svn=="" or main=="":
                    dic['status'] = '不能为空'
                else:
                    try:
                        models.Point.objects.filter(modular_id=mid).get(name=name)
                    except:
                        modular = models.Modular.objects.get(id=mid)
                        add_dict = {'name':name,'svn':svn,'main':main,'modular':modular}
                        models.Point.objects.create(**add_dict)
                    else:
                        dic['status'] = '功能点已存在'
                dic['point_list'] =models.Point.objects.filter(modular_id=mid)
        elif action=='modify':  #修改模块或者功能点
            if Type== "modular":      #修改模块
                try:
                    mode = models.Modular.objects.get(id=request.POST['id'])
                except:
                    pass
                else:
                    mode.name=name
                    mode.svn=svn
                    mode.main=main
                    mode.save()
                # proj_project = models.Modular.objects.get(id=id[1:]).project
                dic['mode_list'] = models.Modular.objects.filter(project_id=pid)
            elif Type == "point":     #修改功能点
                try:
                    point = models.Point.objects.get(id=request.POST['id'])
                except:
                    pass
                else:
                    point.name=name
                    point.svn=svn
                    point.main=main
                    point.save()
                # mode_project = models.Point.objects.get(id=id[1:]).modular
                dic['point_list'] =models.Point.objects.filter(modular_id=mid)
        else:       #禁用模块或者功能点
            pass
        dic['Type'] = Type
        dic['pid'] = pid
        dic['mid'] = mid
    else:
        #请求跳转到模块/功能点添加页
        Type = request.GET['Type']
        if Type=="modular":
            pid = request.GET['pid']
            dic['mode_list'] = models.Modular.objects.filter(project_id=pid)
            dic['Type'] = Type
            dic['pid'] = pid
        elif Type == "point":
            mid = request.GET['mid']
            dic['point_list'] =models.Point.objects.filter(modular__id=mid)        #因为modular_id是唯一的
            dic['Type'] = Type
            dic['mid'] = mid
    return render(request,'include/addpoint.html',dic)

@csrf_exempt
def machine(request):
    dic = {}
    if request.method == "POST":
        #点击弹窗的确定
        action = request.POST['action']
        print(action)
        if action == 'selected_machine_list':
            name = request.POST['name']
            machine_list = request.POST['machine_list']
            machine_list = eval(machine_list)
            temp_list = []
            for id in machine_list:
                temp_list.append(id[1:])
            try:
                models.UserSave.objects.get(name=name)      #如果存在则更新
                # models.UserSave.objects.get(name=name).update(machine_case=str(temp_list))
                obj = models.UserSave.objects.get(name=name)
                obj.machine_case = str(temp_list)
                obj.save()
            except:
                models.UserSave.objects.create(name=name,machine_case=str(temp_list))
            dic['save_machine_list'] = models.Machine.objects.filter(id__in=temp_list)
            dic['save_machine_arr'] = 'None'  #懒得写了，传None字符吧
            return render(request,'include/select_machine.html',dic)
    else:
        try:
            # 弹出执行机弹窗
            action = request.GET['action']
        except:
            #跳转到执行机页
            try:
                username = request.GET['username']
                obj = models.UserSave.objects.get(name=username)
                temp_list = obj.machine_case
                temp_list = eval(temp_list)
            except:
                temp_list = []
            dic['save_machine_list'] = models.Machine.objects.filter(id__in=temp_list)    #发送数据库
            temp_arr = []
            for arr in temp_list:
                temp_arr.append('c'+arr)
            dic['save_machine_arr'] = json.dumps(temp_arr)       #发送数组
            return render(request,'include/select_machine.html',dic)
        else:
            #弹出执行机弹窗
            dic['machine_list'] = models.Machine.objects.all()
            return render(request, 'include/popup.html', dic)
@csrf_exempt
def addmachine(request):
    dic = {}
    if request.method == "POST":
        name = request.POST['name']
        ip = request.POST['ip']
        password = request.POST['password']
        action = request.POST['action']
        if name=="" or ip=="":
            dic['status'] = '不能为空'
        else:
            if action=='add':       #添加机器
                try:
                    models.Machine.objects.get(name=name)
                except Exception as e:
                    print(e,'添加机器')
                    models.Machine.objects.create(name=name,ip=ip,password=password)
                else:
                    dic['status'] = '机器名已存在'
            elif action=='modify':      #修改操作,先判断机器id是否正确
                try:
                    machine = models.Machine.objects.get(id=request.POST['cid'][1:])
                except:
                    pass
                else:
                    machine.name=name
                    machine.ip=ip
                    machine.password=password
                    machine.save()
            else:       #禁用操作
                pass
    else:
        #点击设置，添加机器
        pass
    dic['machine_list'] = models.Machine.objects.all()
    return render(request,'include/addmachine.html',dic)

@csrf_exempt
def monitor(request):
    '''获取test数据，写入数据库，启动线程来发送到各个执行机'''
    data = request.POST['data']
    data = eval(data)

    '''
    result = go(data)   #写入数据库，返回时间戳

    #启动线程（发送文件）
    thread = threading.Thread(target=send,args=(result,),name=result)
    threads.clear()
    threads.append(thread)
    for tr in threads:
        tr.start()
    '''
    result = func.go2(data)  #(使用Grid框架),写入数据库，返回测试数据
    if result:
        #启动线程
        thread = threading.Thread(target=func.StartTest,args=(result,))
        thread.start()
    else:
        print("无测试项")
    return render(request,'include/monitor.html')