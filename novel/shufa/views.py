from django.shortcuts import render,redirect,get_object_or_404

from shufa import func

# Create your views here.

def index(request):
	return render(request,"shufa/index.html")

def raky(request):
	zi = request.GET.get('zi')
	zitype = request.GET.get('zitype','楷书')	#默认为楷书
	flag = request.GET.get('flag','0')		#默认为0
	# print(zi)
	dic = {}
	dic['zi_all'] = zi
	dic['zi'] = zi[0] if zi else zi
	dic['zitype'] = zitype
	if zi:
		rlt = func.getdata(zi[0],zitype)
		# print(rlt)
		dic['url'] = rlt
		# print(rlt)
		if flag == '0':
			return render(request,"shufa/raky.html",dic)
		else:
			return render(request,"shufa/zi_show.html",dic)
	else:
		return render(request,"shufa/index.html")

def database(request):
	# func.delect_data()
	return render(request,"shufa/index.html")