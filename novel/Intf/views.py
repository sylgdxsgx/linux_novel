from django.shortcuts import render,redirect,get_object_or_404
# from django.http import HttpResponse,HttpResponseRedirect    #与上面的功能一样吧
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from Intf.models import Event,Guest


# Create your views here.
def index(request):
    return render(request,"Intf/index.html")

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['user'] = username
            response = redirect('/Intf/event_manage/')
            return response
        # if username == 'admin' and password == 'admin123':
        #     response = redirect('/Intf/event_manage/')
        #     # response.set_cookie('user',username,3600)
        #     request.session['user'] = username
        #     return response
        else:
            return render(request,'Intf/index.html', {'error': 'username or password error!'})
    else:
        return render(request,'Intf/index.html')

@login_required     #关上窗户
def event_manage(request):
    # username = request.COOKIES.get('user','')
    username = request.session.get('user','')
    event_list = Event.objects.all()
    return render(request,"Intf/event_manage.html",{'user':username,'events':event_list})

@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get("name","")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,"Intf/event_manage.html",{'user':username,'events':event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user','')
    # guest_list = Guest.objects.all()
    guest_list = Guest.objects.all().order_by('create_time')
    # guest_list = Guest.objects.get_queryset().order_by('create_time')
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request,"Intf/guest_manage.html",{'user':username,'guests':contacts})

@login_required
def sign_index(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    return render(request,'Intf/sign_index.html',{'event':event})

@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'Intf/sign_index.html',{'event':event,'hint':'phone error.'})

    result = Guest.objects.get(phone=phone,event_id=event_id)
    if result.sign:
        return render(request,'Intf/sign_index.html',{'event':event,'hint':'user has sign in.'})

    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign = '1')
        return render(request,'Intf/sign_index.html',{'event':event,'hint':'sign in seccess!','guest':result})

@login_required
def logout(request):
    auth.logout(request)
    response = redirect('/Intf/index')
    return response