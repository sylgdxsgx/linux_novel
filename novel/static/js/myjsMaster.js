$(document).ready(function(){
	$("#block1 li").click(function(){	//项目菜单
		var id = $(this).attr("id");
		if(id != "menu_addproject"){
			pid = id; 		//保存当前项目id
			var url = "/app02/index/?pid="+id;
			var content = document.getElementById("content"); 
			$("#content").load(url);//?PID=XX没用
			//window.history.pushState({content:content.load},0,'http://'+host+url);	//会在请求成功后修改页面的URL
		}else{				//添加项目按钮
			var url = "/app02/addproject";
			var content = document.getElementById("content"); 
			$("#content").load(url);
			$(window).scrollTop(0);		//回滚到页面顶部
			//window.history.pushState({content:content.load},0,'http://'+host+url);
		}
		if(typeof($("#block3 input").attr("set"))!="undefined"){//判断是否有属性set=ok
			$("#block3 input").removeAttr('set');
		};
	});
	$("#set").click(function(){		//设置按钮
		var url = "/app02/addmachine";
		var content = document.getElementById("content");
		$("#content").load(url);
		//window.history.pushState({content:content.load},0,'http://'+host+url);
		$("#block1").css("display",'none');//隐藏菜单栏
		$("#block3").css("display","none");//隐藏测试项栏
		$("#block4").css("display","none");//隐藏前进、后退键
		$(window).scrollTop(0);		//回滚到页面顶部
	});
	$("#forward").click(function(){		//下一步按钮
		if(typeof($(this).attr("set"))=="undefined"){//判断是否有属性set=ok,第一次点击
			$(this).attr('set','ok');	//设置test为ok
			var url = "/app02/machine?username="+username;
			$("#content").load(url,function(){		//隐藏菜单，显示上一步
				$("#block1").css("display",'none');
				$("#backward").parent().css("display",'block');
				var temp_backward_top = 218-$(window).scrollTop();
				if(temp_backward_top<=0){
					temp_backward_top=0;
				};
				$("#backward").parent().css("top",temp_backward_top+30+"px");
			});
		}else{//第二次点击，提交数据了
			$(this).removeAttr('set');
			send();
		};
		$(window).scrollTop(0);		//回滚到页面顶部
		//alert($(document).scrollTop());
		//window.history.pushState({content:content.load},0,'http://'+host+url);
		//window.location.href="/app02/machine.html?username="+username;
	});

	$("#backward").click(function(){		//上一步按钮
		if(typeof($("#forward").attr("set"))=="undefined"){//被点击过一次
			;
		}else{//被点击过2次
			$("#forward").removeAttr('set');
		};
		$("#content").html("");
		$("#block1").css("display",'block');
		$("#backward").parent().css("display",'none');
		$(window).scrollTop(0);		//回滚到页面顶部
	});
	
	$(window).resize(function(){//当浏览器大小变化时
		var temp_top = $(window).height()-70;
		$(".pub_fo").css("top",temp_top+"px");	//设置底部高度
		$("#forward").parent().css("top",temp_top - 130 +"px");
		$("#forward").parent().css("left",$("#block2").offset().left +1230);	//设置前进按钮位置
	});
	$(window).scroll(function(){//当滚动条变化时
		var temp_menu_top = 218-$(window).scrollTop();
		if(temp_menu_top<=0){
			temp_menu_top=0;
		};
		$(".left_navber_wrap").css("top",temp_menu_top+30+"px");//设置菜单高度
	
		var temp_backward_top = 218-$(window).scrollTop();
		if(temp_backward_top<=0){
			temp_backward_top=0;
		};
		$("#backward").parent().css("top",temp_backward_top+30+"px");//设置后退按钮高度
	});
	var temp_menu_top = 218-$(window).scrollTop();
	if(temp_menu_top<=0){
		temp_menu_top=0;
	};
	$(".left_navber_wrap").css("top",temp_menu_top+30+"px");//设置菜单高度
	var temp_top = $(window).height()-70;
	$(".pub_fo").css("top",temp_top+"px");					//设置底部高度
	$("#forward").parent().css("top",temp_top - 130 +"px");	//首次打开时，设置前进按钮高度
	$("#forward").parent().css("left",$("#block2").offset().left +1230);	//设置前进按钮位置
	$("#backward").parent().css('display','none');			//首次打开时，设置返回按钮为隐藏
});

//$('textarea').each(function(){
//	$(this).setAttribute('style','height:'+($(this).scrollHeight)+'px;overflow-y:hidden;');
//}).on('input',function(){
//	$(this).style.height='auto';
//	$(this).style.height=($(this).scrollHeight)+'px';
//});

$(function(){
	$(window).scroll(function(){
		var point = getObjWhl("machinepopup");
		$("#machinepopup").css({position:"absolute", top:point.y, left:"25%"});
	});
});

function send(){
	var url = "/app02/monitor";
	var temp_data = {};
	var temp_value = [];
	var temp_tt = [];	//保存测试项和浏览器
	$.each(dictcase_checked,function(i,items){
		if(items != ''){
			temp_value = [];
			$.each(items,function(n,value){
				temp_tt = [];
				temp_tt.push($(value).find('button').attr('id'));//保存测试项
				temp_tt.push('chrome');//保存浏览器
				temp_value.push(temp_tt);
			});
			temp_data[i] = temp_value;
		}
	});
	var data_dict = JSON.stringify(temp_data);//将字典转换成字符串
	$(".main").load(url,{'data':data_dict});
	//$.getJSON();
};

function back(){
	$("#content").html("");
	$("#block3").css("display","block");//显示测试项栏
	$("#block4").css("display","block");//显示前进、后退键
	if($("#backward").parent().css("display")=='none'){
		$("#block1").css("display",'block');
	}else{
		var url = "/app02/machine?username="+username;
		$("#content").load(url);
	};
};

function checkclick(obj){//按钮点击事件
	var clas = $(obj).attr('class'); 
	var id = $(obj).attr('id');
	var test_attr = $(obj).attr('test');
	var start_string = id.substring(0,1);
	if(start_string != 'c'){//如果点击的是模块和功能点
		if($(obj).parent().parent().attr('id') == "pop-table"){//如果是在弹窗中点击
			var cid = $(obj).parent().parent().attr('test');		//弹窗所属项
			var temp_value = [];
			if(clas == "unchecked")
			{
				$(obj).attr('class','checked');
				var temp_clone = $(obj).parent().clone();
				testcase_list.push(temp_clone);//保存到当前执行机s数组中
				if(typeof(dictcase_checked[cid])!="undefined"){
					temp_value = dictcase_checked[cid];
				}else{
					temp_value = [];
				}
				temp_value.push(temp_clone);//追加一个对象
				dictcase_checked[cid] = temp_value;	//保存起来
				//dictcase_checked.push($(obj).attr('id'));		//将该id保存起来
				//$(machine_test_obj).append($(obj).parent().clone());	//添加测试项
				//$(obj).parent().css({float:"left"});  //已经有了的
			}else{
				$(obj).attr('class','unchecked');
				testcase_list.splice($.inArray($(obj).parent(),testcase_list),1);
				temp_value = dictcase_checked[cid];
				temp_value.splice($.inArray($(obj).parent(),temp_value),1);	//从value中删除
				dictcase_checked[cid] = temp_value;	//更新字典
				//dictcase_checked.splice($.inArray($(obj).attr('id'),dictcase_checked),1);
				//var a = "#pop-table [test="+test_attr+"]";
				//$(a).parent().remove();		//删除测试项
			}
		}else if($(obj).parent().parent().attr('id') == "selected-test"){	//如果是在selected-test中点击
			test_list.splice($.inArray(id,test_list),1);	//从数组中删除
			$(obj).parent().remove();	//删除测试项
			var tempid = "#"+id;
			if($(tempid).length){		//如果该元素存在
				$(tempid).attr("class","unchecked");	//将table中改变样式
			}
			//document.getElementById(id).setAttribute("class","unchecked");//将table中改变样式
		}else{										//如果是在table中点击
			if(typeof($(obj).attr("test"))=="undefined"){					//如果没有test属性（在项目详情页点击）
				if(clas == "unchecked")
				{
					test_list.push(id);		//添加到数组中
					$(obj).attr('class','checked');//修改样式
					$("#selected-test").append($(obj).parent().clone());	//添加测试项
					$("#selected-test div").css({float:"left"});			//统一修改样式（重复了）
					var a = "#selected-test #"+id;
					$(a).attr('test',id);	//添加一个属性
				}else{
					test_list.splice($.inArray(id,test_list),1);	//从数组中删除
					$(obj).attr('class','unchecked');
					var a = "[test="+id+"]";
					$(a).parent().remove();		//删除测试项
				}
			}else{
				var cid = $(obj).parent().parent().prev().find('button').attr('id');	//获取机器cid
				var temp_value = dictcase_checked[cid];		//获取该机器下所有的测试
				temp_value.splice($.inArray($(obj).parent(),temp_value),1)//删除该测试项
				dictcase_checked[cid] = temp_value;//更新字典
				$(obj).parent().remove();		//删除该项
				var tempid = "#selected-test #"+id;
				$(tempid).attr('class','checked');
				$(tempid).attr('disabled',false);
			}
		}
	}else{//点击的是执行机
		if(clas == "unchecked")
		{
			machine_list_new.push(id);
			$(obj).attr('class','checked');
		}else{
			machine_list_new.splice($.inArray(id,machine_list_new),1);	//从数组中删除
			$(obj).attr('class','unchecked');
		}
	};
};

function addmodular(obj){
	var url = "/app02/addpoint?Type=modular&pid="+pid;
	$("#content").load(url);
	var content = document.getElementById('content');
	$(window).scrollTop(0);		//回滚到页面顶部
	//window.history.pushState({content:content.load},0,'http://'+host+url);
}; 

function addpoint(obj){
	var mid = $(obj).attr('id');
	var url = "/app02/addpoint?Type=point&mid="+mid;
	$("#content").load(url);
	var content = document.getElementById('content');
	$(window).scrollTop(0);		//回滚到页面顶部
	//window.history.pushState({content:content.load},0,'http://'+host+url);
};

function modify_project(obj){
	var temp_id = $(obj).attr('id').split("_")[0];
	if($(obj).attr('value')=='修改'){	//如果是修改，则enabled输入框
		$(obj).attr('value','保存');
		$("#"+temp_id+"_name").attr('disabled',false);
		$("#"+temp_id+"_svn").attr('disabled',false);
	}else{
		//因为有返回HTML文件，故而，不用设置各标签
		var url = '/app02/addproject';
		var name = $("#"+temp_id+"_name").val();
		var svn= $("#"+temp_id+"_svn").val();
		$("#content").load(url,{'id':temp_id,'name':name,'svn':svn,'action':'modify'});
	};
};

function modify_point(obj){
	var temp_id = $(obj).attr('id').split("_")[0];	//获取选项id
	if($(obj).attr('value')=='修改'){	//如果是修改，则enabled输入框
		$(obj).attr('value','保存');
		$("#"+temp_id+"_name").attr('disabled',false);
		$("#"+temp_id+"_svn").attr('disabled',false);
		$("#"+temp_id+"_main").attr('disabled',false);
	}else{
		//因为有返回HTML文件，故而，不用设置各标签
		var url = '/app02/addpoint';
		var name = $("#"+temp_id+"_name").val();
		var svn= $("#"+temp_id+"_svn").val();
		var main=$("#"+temp_id+"_main").val();
		var Type = $("#addpoint_btn").attr('name');
		var mid = $("#addpoint_btn").attr('modeid');
		var id = temp_id.substring(1);	//从1开始的字符串，选项id去除m
		$("#content").load(url,{'name':name,'svn':svn,'main':main,'action':'modify','Type':Type,'pid':pid,'mid':mid,'id':id});
	};
};

function modify_machine(obj){
	var temp_id = $(obj).attr('id').split("_")[0];	//先获取机器id
	if($(obj).attr('value')=='修改'){	//如果是修改，则enabled输入框
		$(obj).attr('value','保存');
		$("#"+temp_id+"_name").attr('disabled',false);
		$("#"+temp_id+"_ip").attr('disabled',false);
		$("#"+temp_id+"_pwd").attr('disabled',false);
	}else{
		//因为有返回HTML文件，故而，不用设置各标签
		var url = '/app02/addmachine';
		var name = $("#"+temp_id+"_name").val();
		var ip= $("#"+temp_id+"_ip").val();
		var password = $("#"+temp_id+"_pwd").val();
		$("#content").load(url,{'cid':temp_id,'name':name,'ip':ip,'password':password,'action':'modify'});
	};
};

function getObjWhl(obj){    
  var point={};    
  var st=$(document).scrollTop();//滚动条距顶部的距离    
  var sl= $(document).scrollLeft();//滚动条距左边的距离    
  var ch=$(window).height();//屏幕的高度    
  var cw=$(window).width();//屏幕的宽度    
	
  var objH=$("#"+obj).height();//浮动对象的高度    
  var objW=$("#"+obj).width();//浮动对象的宽度    

  var objT=Number(st)+(Number(ch)-Number(objH))/2;    
  var objL=Number(sl)+(Number(cw)-Number(objW))/2;    
  point.x = objL ;    
  point.y = objT;      
  return point;    
};

function filtermachine(){
	/*弹窗-执行机,会发送请求*/
	
	$("#machinepopup").show();
	$("#fade").css("height",$(document).height()+"px");//设置fade高度
	$("#fade").show();
	$("#pop-table").html('');
	$("#pop-table").load('/app02/machine?action=getmachinelist',function(responseTxt,statusTxt,xhr){
		$("#pop-table button").each(function(i,domi){//设置显示样式
			var cid = $(this).attr('id');
			if($.inArray(cid,machine_list) != -1){
				$(this).attr('class','checked');
			}
		});
	});//回调函数为空
	//$("#machinepopup [btn='ok']").attr('id','selectedmachinelist');
	$("#btnok").attr('onclick','selectedmachinelist()');
	//$("#btnok").click(function(){
	//	selectedmachinelist();
	//	});
};

function selectedmachinelist(){
	/*确定-执行机*/
	var temp_id = [];//保存将要删除的测试项id
	$("#machinepopup").hide();
	$("#fade").hide();
	var list = JSON.stringify(machine_list_new);
	$("#content").load('/app02/machine',{'name':username,'action':'selected_machine_list','machine_list':list});
	
	$.each(machine_list,function(i,items){		//如果有机器被去掉了，则该机器的测试项要释放出来
		if($.inArray(items,machine_list_new) == -1){
			if(typeof(dictcase_checked[items]) != "undefined"){//如果要被干掉的项不为undefined
				if(dictcase_checked[items] != ""){//同时列表又不为空
					$.each(dictcase_checked[items],function(n,value){//则读取出该项下的列表的每个值
						temp_id.push($(value).find('button').attr('id'));
					});
				}
				delete dictcase_checked[items];		//将该执行机的测试项从字典中删除
			}
		};
	});
	$("#selected-test div").each(function(i,domi){//更新selected-test数据
		if($.inArray($(this).find("button").attr('id'),temp_id) != -1){
			$(this).find('button').attr('class','checked');
			$(this).find('button').attr('disabled',false);
		}
	});
	machine_list = [];	//先清空
	$.each(machine_list_new,function(n,value){//再更新列表
		machine_list.push(value);
	});
};	

function addmachinetest(obj){
	/*弹窗-测试项,不会发送请求*/
	var cid = $(obj).attr('id');//先获取机器id号
	var temp_id1 = [];			//保存该机器下已选的测试项
	var temp_id2 = [];			//保存其它机器下已选的测试
	var temp_height_popup = $("#machinepopup").outerHeight();
	var temp_height_mac_up = ($(window).height()-temp_height_popup)/2+"px";
	testcase_list = [];			//每次都清空
	$("#pop-table").html('');	//先清空数据
	$("#pop-table").attr('test',cid);//表示此次弹窗属于cid的
	$.each(dictcase_checked,function(name,value){		//将testid_checked中的数据整理出来
		if(name == cid){
			$.each(dictcase_checked[name],function(n,value){
				temp_id1.push(value.children().eq(0).attr('id'));
			})
		}else{
			$.each(dictcase_checked[name],function(n,value){
				temp_id2.push(value.children().eq(0).attr('id'));
			})
		}
	}); 
	$("#selected-test div").each(function(i,domi){		//筛选数据
		if($.inArray($(this).children().eq(0).attr('id'),temp_id2) == -1){//不在temp_id2中则添加
			var temp_obj = $(this).clone();
			if($.inArray($(this).children().eq(0).attr('id'),temp_id1) == -1){//又不在temp_id1中
				$(temp_obj).children().eq(0).attr('class','unchecked');
				$(temp_obj).children().eq(0).attr('disabled',false);
			}else{
				$(temp_obj).children().eq(0).attr('class','checked');
				$(temp_obj).children().eq(0).attr('disabled',false);
				testcase_list.push(temp_obj);		//保存已经添加了的测试项
			}
			$("#pop-table").append($(temp_obj));	//添加到pop-table中
		}
	});
	$(obj).parent().attr('id','flagId');//为父标签传递ID，在点击确定之后将其删除
	$("#btnok").attr('onclick','selectedmachinetest("flagId")');//传递ID
	//$("#btnok").click(function(){
	//	selectedmachinetest($(obj).parent());
	//	});
	//$("#machinepopup").css("top",temp_height_mac_up);
	var point = getObjWhl("machinepopup");
	$("#machinepopup").css({position:"absolute", top:point.y, left:"25%"});
	$("#machinepopup").show();
	$("#fade").css("height",$(document).height()+"px");//设置fade高度
	$("#fade").show();
};

function selectedmachinetest(id){
	/*确定-测试项*/
	//debugger
	var temp_id = [];
	$("#machinepopup").hide();
	$("#fade").hide();
	$("#flagId").siblings(".buttondiv").remove();	//先清空数据
	$("#flagId").before(testcase_list);		//添加测试项
	$("#flagId").attr('id','');				//清空id
	$.each(dictcase_checked,function(name,value){		//将testid_checked中的数据整理出来
		$.each(dictcase_checked[name],function(n,value){
			temp_id.push(value.children().eq(0).attr('id'));
		})
	}); 
	$("#selected-test div").each(function(i,domi){	//置灰selected-test测试项
		if($.inArray($(this).children().eq(0).attr('id'),temp_id) != -1){
			$(this).children().eq(0).attr('disabled',true);	//不可点击
			$(this).children().eq(0).attr('class','checked_ok'); //置灰
			//再将项目table中的也设置成disabled
		}else{
			$(this).children().eq(0).attr('disabled',false);
			$(this).children().eq(0).attr('class','checked');
			}
		});
	//list = JSON.stringify(machine_list)
	//$("#content").load('#',{name:username,action:'selected_machine_list',machine_list:list});
};