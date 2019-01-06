import os,socket,time,queue
import svn.remote
import subprocess
import paramiko
import threading
from app02 import models
from configparser import ConfigParser

localhost = '172.16.3.220'
svn_name = 'admin'
svn_pwd = 'testisli123'
svn_path = '/home/mpr/svn_copy/Test_Au/IsliTest'
svn_server_path = 'svn://172.16.3.220/project_1/Test_Au/IsliTest'
q_checknode = queue.Queue()
selenium_file = 'selenium-server-standalone-3.8.1.jar'

def StartTest(test_dict):
    """ Grid框架,开始测试
        0、更新svn
        1、启动Hub
        2、ping IP,启动node
        3、新进程执行测试
    """
    
    #更新svn
    update_from_svn(svn_path)   #svn 副本目录
	
    stamp = int(round(time.time()*1000))    #时间戳,毫秒级
    #启动Hub
    port = StartHub(localhost)
    #写入数据库
    if port:    #当port存在时,写入数据库
        registerHub = "http://%s:%s/grid/register/"%(localhost,port)
        add_dict = {'time_stamp':stamp,'test_list':test_dict,'register_hub':registerHub}
        models.TestList.objects.create(**add_dict)  #写入数据库
    else:
        print("启动Hub失败")
        return False

    test_list = []      #[{'http://172.16.7.34:5555/wd/hub':[('/home/mpr/est1s.py','firefox')]}]
    hub = registerHub
    hub_port = hub.split('/')[2].split(':')[1]
    #启动node
    #可以使用多线程来进行，方法见<技能提升篇--多线程.jpg>
    threads = []
    for item in test_dict.items():
        t = threading.Thread(target=CheckNode,args=(item,hub,))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()        #显然，所有节点都成功启动（或者等待10s启动失败）后，才进行测试
    while not q_checknode.empty():
        test_list.append(q_checknode.get()) #把node节点写入测试数据中
    #将测试数据写入文件test_list.list
    if not test_list:   #为空时
        print('\n没有测试数据(节点未启动或者测试模块为空)')
        return
    conf = ConfigParser()
    conf_file = '/opt/proj/script/test_list.list'
    conf.read(conf_file)
    conf.add_section(str(stamp))
    conf.set(str(stamp),'value',str(test_list))
    conf.write(open(conf_file,'w'))
    #启动测试
    print('启动子进程，开始测试，[ python manage.py %s  ]'%stamp)
    result = subprocess.call('python %s/manage.py %s'%(svn_path,stamp),shell=True)
    print('子进程测试结束！ result=%s'%result)

def CheckNode(idict,hub):
    ip,data = idict
    port = StartNode(ip,5555,hub)   #返回将要启动的端口
    #判断端口是否成功启动
    if port:    #node成功启动
        for i in range(10):  #20s钟的等待
            if IsPortInUse(ip,port):
                print('尝试连接远程 http://%s:%s 成功'%(ip,port))
                node = 'http://{ip}:{port}/wd/hub'.format(ip=ip,port=port)
                temp_dict = {}
                temp_dict[node] = data
                q_checknode.put(temp_dict)  #将结果存入队列中
                break
            print('尝试连接远程 http://%s:%s 失败'%(ip,port))
            time.sleep(2)
        else:
            print('远程node连接失败: http://%s:%s'%(ip,port))
    
def go2(testdict):
    """
    分析测试数据,筛选出有效数据，并写入数据库:time_stamp,save_dict,register_hub
    返回测试字典：save_dict={'172.16.7.34':[('../../test1.py', 'chrome'), ('./test2.py', 'firefox'),],}
    """
    stamp = int(round(time.time()*1000))    #时间戳,毫秒级
    save_dict = {}
    for key,item in testdict.items():
        #判断机器是否存在
        try:
            machine = models.Machine.objects.get(id=key[1:])
        except:     #不存在时
            print('>>>>>>>执行机:',key,'>>>>>>>>>不存在！')
            continue
        #判断IP是否填写
        if not machine.ip:  #如果没有填写ip地址,则读取下一条
            print('>>>>>>>执行机:',key,'>>>>>>>>>IP地址为空！')
            continue
        #如果IP写好了
        save_list = [] #保存临时元组
        for value in item:
            # 先判断数据是否正确
            #判断是否为2个数据（含有浏览器数据）
            if len(value)!=2:
                continue
            if value[0][0] == 'm':     #是模块
                mode = models.Modular.objects.get(id=value[0][1:])
                proj_svn = mode.project.svn
            elif value[0][0] == 'p':     #是功能点
                mode = models.Point.objects.get(id=value[0][1:])
                proj_svn = mode.modular.project.svn
            else:
                print('>>>>>>>执行机:{}({}) --测试项{} >>>>>>>>>测试数据异常！'.format(machine.name,machine.ip,value))
                continue
            # 再判断svn文件和主文件是否写好
            if not mode.svn:
                print('>>>>>>>执行机:{}({}) --测试项{} >>>>>>>>>未配置svn！'.format(machine.name,machine.ip,mode.name))
                continue
            test_svn = proj_svn.strip('/')+'/'+mode.svn.strip('/')
            test_svn = test_svn.replace('\\','/').replace('//','/').replace('\n','')
            #以上都没问题则保存到数组中
            save_list.append(tuple([test_svn,value[1]]))
        if save_list:
            save_dict[machine.ip] = save_list  #如果该执行机有测试数据，则保存到字典中。
    return save_dict

def StartHub(ip,port=4444):
    """启动hub,返回port"""
    print('启动hub...')
    for i in range(int(port),4500):
        if not IsPortInUse(ip,i):
            port = i
            #这里将输出保存到日志文件，如果日志文件很大了会怎样呢？--先不处理
            ret = subprocess.Popen("/usr/bin/java -jar /opt/proj/script/selenium-server-standalone-3.8.1.jar -role hub"
                           " -port %s >>/opt/proj/script/novel_uwsgi.log 2>&1 &"%port,shell=True)
            break
        else:
            #判断该端口是否是selenium在运行
            ret = os.popen("lsof -i:%s"%i)
            str_list = ret.readlines()
            pid = 0
            for l in str_list[1:]:
                ret_list = l.split()
                pid = ret_list[1]   #获取到了pid
            ret = os.popen("ps -ef | grep %s | grep -v grep"%pid)
            if 'selenium-server-standalone' in ret.read():
                port = i
                break
    else:
        print("Try again!")
        return False
    print('启动hub完毕')
    return port

def StartNode(ip,port,hub):
    '''从5555到5600，自动设定端口，启动node,返回port或者False'''
    print('>>>准备设定Node：%s'%ip)
    data_mode = r'''%1(start /min cmd.exe /c %0 :&exit)
set PROJECT_HOME={path}
cd /d %PROJECT_HOME%
java -jar selenium-server-standalone-3.8.1.jar -role node -port {port} -hub {hub}'''
    data_node = r'\%1(start /min cmd.exe /c \%0 :&exit);set PROJECT_HOME={path};cd /d \%PROJECT_HOME\%;java -jar selenium-server-standalone-3.8.1.jar -role node -port {port} -hub {hub}'
    #先ping
    result = PingIP(ip) 
    if not result:  #如果没有ping通
        return False
    temp_dict = {}
    for i in range(int(port),5600):
        if not IsPortInUse(ip,i):
            port = i
            print('>>>Node %s 预计启用端口：%s'%(ip,port))
            break
    else:
        print('>>>Node{}没有获得可用的端口'.format(ip))
        return False
    dest_path = models.TestConfig.objects.get(id=1).test_root_dir.replace('\\','/')  #windows支持路径为斜杠符号
    stamp = str(round(time.time()*1000))    #时间戳,毫秒级
    file_data = data_mode.format(path=dest_path,port=port,hub=hub)
    file_data_node = data_node.format(path=dest_path,port=port,hub=hub)
    sec_file = '/opt/proj/script/%s.bat'%stamp  #要发送的bat文件
    with open(sec_file,'w') as f:
        f.truncate()    #清空文件
        f.write(file_data)  #写文件
    print('>>>设定Node完毕，发送节点配置到节点机器：%s,并启动...\n'%ip)
    result = send_file(ip,dest_path,sec_file)   #发送文件并启动node
    #result = send_file(ip,dest_path,file_data_node)	#发送启动代码并启动node
    if not result:
        print('>>>启动node：%s失败(发送文件时出错了)'%ip)
        return False
    #node = 'http://{ip}:{port}/wd/hub'.format(ip=ip,port=port)
    os.remove(sec_file) #删除该bat文件
    print('>>>启动node：%s结果：待确认'%ip)
    return port


def IsPortInUse(ip,port):
    """判断主机和远程端口是否被占用"""
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        #利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
        #该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
        s.shutdown(2)
        print('>>>Node %s:%s 已占用'%(ip,port))
        return True
    except:
        print('>>>Node %s:%s 未被占用'%(ip,port))
        return False

def PingIP(ip):
    """ping 远程IP"""
    if os.system('ping -c 1 -w 1 %s'%ip):
        print('>>>IP地址：{} 没有ping通！'.format(ip))
        return False
    else:
        print('>>>IP地址：{} 已ping通！'.format(ip))
        return True

def KillProcess(port):
    """杀掉主机进程，不能杀远程机器进程"""
    ret = os.popen("lsof -i:%s"%port)
    str_list = ret.readlines()
    for l in str_list[1:]:  #从第二行读取
        ret_list = l.split()
        if str(port) in ret_list[8]:
            pid = ret_list[1]
            print('杀掉进程：%s'%pid)
            os.system("kill -9 %s"%pid)
            return True
    return False


def send_file(ip,path,file):
    '''将file发送到ip的指定目录,并且运行file文件（bat文件）'''
    SEND_CMD = r"""
                expect -c "
                set timeout 5;
                spawn scp {d} {src} {user}@{ip}:{dest}{rename};
                expect {{
                    *assword {{send {pwd}\r;}}
                    yes/no {{send yes\r; exp_continue;}}
                }}
                expect eof"
                """
    MD_CMD = r"""
                expect -c "
                set timeout 5;
                spawn ssh {user}@{ip};
                expect {{
                    *assword {{send {pwd}\r;}}
                    yes/no {{send yes\r; exp_continue;}}
                }}
                expect *>*
                send \"MD {dest}\r\";
                send \"exit\r\"
                expect *>*
                "
                """
    TASK_CMD = r"""
                expect -c "
                set timeout 5;
                spawn ssh {user}@{ip};
                expect {{
                    *assword {{send {pwd}\r;}}
                    yes/no {{send yes\r; exp_continue;}}
                }}
                expect *>*
                send \"{cmd1}\r\";
                expect *任务*
                send \"{cmd2}\r\";
                expect *task*
                send \"exit\r\"
                expect *>*
                "
                """
    print('>>>发送文件...')
    #获取执行机信息
    machine = models.Machine.objects.get(ip=ip)
    user = machine.name
    pwd = machine.password
    #先在执行机创建文件夹,路径不要有空格
    scp_cmd = MD_CMD.format(user=user,ip=ip,pwd=pwd,dest=path.replace('/','\\'))
    sub = subprocess.call(scp_cmd,shell=True,stdout=subprocess.PIPE)    #去掉stdout可以查看输出

    #判断selenium-server-standalone-3.8.1.jar是否存在于远程机器上
    selenium_remote_file = '%s/%s'%(path,selenium_file)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,22,user,pwd)
    sftp = client.open_sftp()
    try:
        sftp.stat(selenium_remote_file)
        print('>>>Node %s: 文件 %s 存在'%(ip,selenium_remote_file))
    except IOError:
        #文件不存在
        #发送文件selenium-server-standalone-3.8.1.jar
        selenium_server_file = '/opt/proj/script/%s'%selenium_file
        if not os.path.exists(selenium_server_file):    #如果文件不存在
            print('服务器文件：%s 不存在！'%selenium_server_file)
            return False
        scp_cmd = SEND_CMD.format(d='',user=user,ip=ip,pwd=pwd,src=selenium_server_file,dest=path,rename = '')
        sub = subprocess.Popen(scp_cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        output,err=sub.communicate()  #阻塞
        status = sub.returncode
        print('>>>Node {}：发送文件 {} 状态： status= {} err= {}\n'.format(ip,selenium_server_file,status,err))
        if status !=0 or (status==0 and err):
            print('>>>send "{}" Error\n'.format(selenium_server_file))
            return False  #若是发送文件出错，则直接终止发送

    #发送文件node.bat
    
    scp_cmd = SEND_CMD.format(d='',user=user,ip=ip,pwd=pwd,src=file,dest=path,rename='/node.bat')
    sub = subprocess.Popen(scp_cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    output,err=sub.communicate()  #阻塞
    status = sub.returncode
    print('>>>Node {}：发送文件 {} 状态： status= {} err= {}\n'.format(ip,file,status,err))
    if status !=0 or (status==0 and err):
        print('>>>send "{}" Error\n'.format(file))
        return False  #若是发送文件出错，则直接终止发送
    print('>>>发送文件成功\n')
    #执行任务文件
    print('>>>启动子线程，建立计算机事件，启动Node:%s 配置文件...'%ip)
    task_name = 'task'+str(round(time.time()))    #任务名称
    cmd1 = r"SCHTASKS /Create /SC onstart /TN {task_name} /TR {path} /F".format(task_name=task_name,path=path+'/node.bat')
    #cmd1 = 'SCHTASKS /Create /SC onstart /TN {task_name} /TR \"{path}\" /F'.format(task_name=task_name,path=file)
    cmd2 = "SCHTASKS /run /I /TN {task_name} ".format(task_name=task_name)
    scp_cmd = TASK_CMD.format(user=user,ip=ip,pwd=pwd,dest=path,cmd1=cmd1,cmd2=cmd2)
    sub = subprocess.Popen(scp_cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    #print('scp_cmd=',scp_cmd)
    #sub = subprocess.call(scp_cmd,shell=True)

    rlt = False
    while True:
        line = sub.stdout.readline()
        # print('>>>%s'%line)
        if not line:
            print('>>>子线程结束,执行结果：%s'%rlt)
            break
        #检查是否成功
        if '成功: 尝试运行' in line.strip().decode("utf-8"):
            rlt = True
            print('>>>Node {}：执行文件 {} 成功\n'.format(ip,path+'/node.bat'))
        #打印输出到console
        # print('Subprogram output:> {} <'.format(line.strip().decode("utf-8")))
        print('>>>Node {}：执行文件 {} 检查中(未成功)...\n'.format(ip,path+'/node.bat'))
    sub.wait()
    return True

def update_from_svn(target_path):
    print('更新svn...')
    r = svn.remote.RemoteClient(svn_server_path,username=svn_name,password=svn_pwd)
    r.checkout(target_path)     # 包括了 checkout 及 update, 很不错
    print('更新svn完毕')
    

    

##+++++++++++++++++未使用的函数+++++++++++++++++++++++++++++
def readLog(file):
    '''返回最后5行(列表)'''
    with open(file,'r') as f:
        size = f.seek(0,2)
        if size <3000:  #如果是小文件
            lines = f.readlines()
        else:
            off = -500
            while True:
                f.seek(off, 2)  #从文件末尾向前off个字符
                lines = f.readlines()
                if len(lines) >= 5: #判断是否最少有5行
                    break
                off *=2
    return lines
    
def go(testdict):
    """
    分析测试数据,筛选出有效数据，并写入数据库
    传入数据testdict:{'c1':['m1','p3'],}
    写入数据库：TestConfig:写入时间戳
                TestInfo：时间戳、传入数据testdict（字典）、执行机集合(数组['c1','c4',])、状态
                TestInfo_Detail：时间戳、测试项(m1)、执行机(对象)、状态
    """
    test_list = []  #临时保存
    stamp = int(round(time.time()*1000))    #时间戳,毫秒级
    models.TestConfig.objects.filter(id=1).update(current_stamp=stamp)  #保存当前时间戳,每次启动测试都更新这里
    models.TestInfo.objects.create(time_stamp=stamp,test_list=testdict,status=0)   #新建测试,临时保存，非正式测试数据
    for key,item in testdict.items():
        #判断机器是否存在
        try:
            machine = models.Machine.objects.get(id=key[1:])
        except:     #不存在时
            print('>>>>>>>执行机:',key,'>>>>>>>>>不存在！')
            continue
        #判断IP是否填写
        if not machine.ip:  #如果没有填写ip地址,则读取下一条
            print('>>>>>>>执行机:',key,'>>>>>>>>>IP地址为空！')
            continue
        #如果IP写好了
        for value in item:
            # 先判断数据是否正确
            if value[0] == 'm':     #是模块
                mode = models.Modular.objects.get(id=value[1:])
                proj_svn = mode.project.svn
            elif value[0] == 'p':     #是功能点
                mode = models.Point.objects.get(id=value[1:])
                proj_svn = mode.modular.project.svn
            else:
                print('>>>>>>>执行机:{}({}) --测试项{} >>>>>>>>>测试数据异常！'.format(machine.name,machine.ip,value))
                continue
            # 再判断svn文件和主文件是否写好
            if not (mode.svn and mode.main):
                print('>>>>>>>执行机:{}({}) --测试项{} >>>>>>>>>未配置svn！'.format(machine.name,machine.ip,mode.name))
                continue

            #如果都写了（可能写的不对），则写到sjk中，以便以后发送
            models.TestInfo_Detail.objects.create(time_stamp=stamp,test_case=value,machine=machine,status=0)   #新建测试
        else:
            test_list.append(key)       #保存该机器
    else:
        try:
            testinfo = models.TestInfo.objects.get(time_stamp=stamp)    #并且获取出来
        except:
            pass
        else:
            testinfo.machine_list=test_list #保存本次测试的执行机，数组
            testinfo.save()
            '''
            with open(file_name,'w') as f:
                #第一行：ip name password dest mainfile
                line_data = machine.ip+" "+machine.name+" "+machine.password+" "+"d:/TEST_CASE"+" "+mode.main
                f.write(line_data)
                #第二行开始为要发送的svn文件：src_file
                for svni in mode.svn.split("\n"):
                    f.write('\n')     #先换行
                    line_data = proj_svn+svni
                    f.write(line_data)
            test_list.append(file_name) #添加list文件
            '''
    #写入了数据库后，返回时间戳
    return stamp

def send(stamp):
    '''发送文件'''
    #根据时间戳和machine找到记录，故而暂不支持
    test_error = [] #保存出错的文件:[m1.list,p2.list]
    testinfo_list = models.TestInfo_Detail.objects.filter(time_stamp=stamp).order_by('machine')
    for test in testinfo_list:
        result = send_file(test)
        if not result:
            test_error.append(test.test_case)   #记录错误
    print('test_error=',test_error)

def send_file1(obj):
    SEND_CMD = r"""
                expect -c "
                set timeout 5;
                spawn scp {d} {src} {user}@{host}:{dest};
                expect {{
                    *assword {{send {pwd}\r;}}
                    yes/no {{send yes\r; exp_continue;}}
                }}
                expect eof"
                """
    DIR_CMD = r"""
                expect -c "
                set timeout 5;
                spawn ssh {user}@{ip};
                expect {{
                    *assword {{send {pwd}\r;}}
                    yes/no {{send yes\r; exp_continue;}}
                }}
                expect *>*
                send \"MD {dest}\r\";
                send \"exit\r\"
                expect *>*
                "
                """
    START_CMD = r"""
                expect -c "
                set timeout 5;
				set addr "{dest}";
                spawn ssh {user}@{ip};
                expect {{
                    *assword {{send {pwd}\r;}}
                    yes/no {{send yes\r; exp_continue;}}
                }}
                expect *>*
                send \"{dest_p}\r\";
				send \"\$addr\r\";
                send \"python {file}\r\";
                expect *>*
                "
                """
    print('\n\n----------- test case: {} -----------'.format(obj.test_case))
    user = obj.machine.name
    ip = obj.machine.ip
    pwd = obj.machine.password
    dest = models.TestConfig.objects.get(id=1).test_root_dir.replace('\\','/')  #统一改为这种样式
    #先在执行机创建文件夹,路径不要有空格
    scp_cmd = DIR_CMD.format(user=user,ip=ip,pwd=pwd,dest=dest.replace('/','\\'))
    sub = subprocess.call(scp_cmd,shell=True,stdout=subprocess.PIPE)    #去掉stdout可以查看输出
    #源文件处理
    test_case = obj.test_case
    if test_case[0]=='m':
        test_case = models.Modular.objects.get(id=test_case[1:])
        proj_svn = test_case.project.svn
    else:
        test_case = models.Point.objects.get(id=test_case[1:])
        proj_svn = test_case.modular.project.svn
    svn = test_case.svn.split("\n")
    print(svn)
    mainfile = test_case.main
    for svni in svn:
        if not svni:    #如果为空
            continue
        temp_svn = proj_svn+svni
        if not os.path.exists(temp_svn):    #当源文件（源文件夹）不存在时
            print('>>>{} -- Not exists !'.format(temp_svn))
            continue
        if os.path.isfile(temp_svn):    #当是文件时
            scp_cmd = SEND_CMD.format(d='',user=user,host=ip,pwd=pwd,src=temp_svn,dest=dest)
        else:   #当时文件夹时
            scp_cmd = SEND_CMD.format(d='-r',user=user,host=ip,pwd=pwd,src=temp_svn,dest=dest)
        #发送数据
        sub = subprocess.Popen(scp_cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        output,err=sub.communicate()  #阻塞
        status = sub.returncode
        print('>>>send "{}" status= {} err= {}\n'.format(temp_svn,status,err))
        if status !=0 and not err:
            obj.status = -1 #发送出错,status=-1
            obj.save()
            return False  #若是发送文件出错，则直接终止发送
    else:
        #发送完，执行测试文件
        obj.status = 1      #成功发送，status=1
        obj.save()
        dest_p = dest.split(':')[0]+':'
        file_py = os.path.basename(mainfile)   #获取文件名
        if mainfile in svn:
            pass        #dest不动
        else:
            dest = dest+'/'+os.path.dirname(mainfile)
        print('dest=',dest)
        dest = dest.split(':/')[-1]  #去掉盘符
        dest=dest.replace('/','\\\\\\')
        print('dest=',dest)
        scp_cmd = START_CMD.format(user=user,ip=ip,pwd=pwd,dest_p=dest_p,dest=dest,file=file_py)
        print(scp_cmd)
        #sub = subprocess.call(scp_cmd,shell=True)
        subprocess.call('expect /opt/proj/script/start_test_cmd {} {} {} {} {} {}'.format(ip,user,pwd,dest_p,dest,file_py),shell=True)
        return mainfile


'''
def select_machine(request):
    dic = {}
    dic['action'] = 'select_machine'
    dic['proj_list'] = models.Project.objects.all()
    dic['machine_list'] = models.Machine.objects.all()

    return render(request,'index.html',dic)
'''
