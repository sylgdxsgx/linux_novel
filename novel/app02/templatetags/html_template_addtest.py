from django import template
from django.utils.safestring import mark_safe
from django.template.base import Node,TemplateSyntaxError

register = template.Library()


@register.simple_tag
def my_modularstyle(projectid,modularid,name,test,list):
    dic = dict(zip(["projectid","modularid","name","action"],[[str(projectid)],[str(modularid)],[name],[test]]))
    if dic in list:
        result = 'style="border-style: solid; border-width: 1px; border-color: blue;"'
    else:
        result = ''
    return mark_safe(result)

@register.simple_tag
def my_pointstyle(projectid,modularid,name,test,list):
    dic = dict(zip(["projectid","modularid","name","action"],[[str(projectid)],[str(modularid)],[name],[test]]))
    if dic in list:
        result = 'style="border-style: solid; border-width: 1px; border-color: blue;"'
    else:
        result = ''
    return mark_safe(result)

@register.simple_tag
def my_test(pid,list):
    result=''
    for test in list:
        projectid = test['projectid'][0]
        modularid = test['modularid'][0]
        name = test['name'][0]
        action = test['action'][0]
        src=''
        if action=="add_modulartest":
            src="/static/img/mode22.png"
        elif action=="add_pointtest":
            src="/static/img/mode11.jpg"
        result = result+ '''<div style="float: left; padding: 10px; width: 80px; height: 85px;">
		    <form action="/app02/project'''+pid+'''/" method="post" style="height:100%;">
			    <input name="projectid" value="'''+projectid+'''" type="hidden">
			    <input name="modularid" value="'''+modularid+'''" type="hidden">
			    <input name="name" value="'''+name+'''" hidden>
			    <input name="test_list" value="'''+str(list)+'''" hidden>
			    <button name="action" value="'''+action+'''" >
				    <img src="'''+src+'''">
				    <div style="height: 20px;">'''+name+'''</div>
			    </button>
		    </form>
	    </div>'''+'\n'
    return mark_safe(result)

