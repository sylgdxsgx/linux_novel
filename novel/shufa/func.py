
import requests
import os
# from urllib.parse import quote,unquote,urlencode
from bs4 import BeautifulSoup
from shufa.models import hanzi,zidetail


def delect_data():
    hanzi.objects.all().delete()
    zidetail.objects.all().delete()

def getdata(zi,zitype='楷书'):
    '''判断是否已经存储在本地'''
    #先查询本地和网络是否有
    rlt = hanzi.objects.filter(zi=zi)
    zi_type = get_first_letter(zitype)[0]
    if rlt:
        # print(rlt)
        rlt_zi = rlt[0]
        if int(eval('rlt_zi.%s'%zi_type)) == 0:
            #字已载入，但该字体没有
            reqdata(zi,zitype)

    else:
        #该字尚未载入
        reqdata(zi,zitype)

    #读取
    zi_path = []
    rlt = zidetail.objects.filter(zi=zi,zitype=zitype)
    for z in rlt:
        dic = {}
        dic['author'] = z.author
        dic['url'] = z.path if z.path else z.url
        zi_path.append(dic)

    return zi_path


def reqdata(zi,zitype='楷书',name=None):
    url = "https://shufa.supfree.net/raky.asp"
    param = {'zi':zi.encode('gb2312')}
    # param = urlencode(param)
    # print(param)
    r = requests.get(url,params=param)

    # print(r.url)

    result = r.content
    result = result.decode('gbk')
    soup = BeautifulSoup(result,'html.parser')
    body = soup.body
    entry = body.find_all('div',class_='entry')[0]
    divs = entry.find_all('div',class_='cdiv')
    if not divs:
        #没有结果，返回
        return False

    for div in divs:
        if div.span !=None:
            span = div.span.string
            # print(span)
            span = span.split('  ')[-1]
            zitype_temp = span[:2]
            if zitype != zitype_temp:
                continue
        else:
            zitype_temp = 'other'
        # print(zi_type)
        for li in div.find_all('li'):
            if name:
                if name in li.a.img['alt']:
                    alt = li.a.img['alt'].split(' - ')
                    url = li.a.img['src']
                    zitype,author,no = alt[1],alt[0],os.path.splitext(os.path.basename(url))[0]
                    #写入数据库
                    write_data(zi=zi,zitype=zitype,author=author,no=no,url=url,status=0)
            else:
                alt = li.a.img['alt'].split(' - ')
                url = li.a.img['src']
                zitype,author,no = alt[1],alt[0],os.path.splitext(os.path.basename(url))[0]
                #写入数据库
                write_data(zi=zi,zitype=zitype,author=author,no=no,url=url,status=0)
        else:
            #else最终都会执行
            zi_type = get_first_letter(zitype_temp)
            # print(zi_type)
            if zi_type != 'other':
                result = hanzi.objects.filter(zi=zi)
                
                # print(result.zi,result.x,result.c,result.k,result.l,result.z,result.g,result.o,result.count)
                #判断该字是否已载入，没有则创建
                if result:
                    result = result[0]
                    if zi_type[0] == 'x':
                        result.x = 1    #1表示已经有url了，2表示已经有path了
                    if zi_type[0] == 'c':
                        result.c = 1
                    if zi_type[0] == 'k':
                        result.k = 1
                    if zi_type[0] == 'l':
                        result.l = 1
                    if zi_type[0] == 'z':
                        result.z = 1
                    if zi_type[0] == 'g':
                        result.g = 1
                    if zi_type[0] == 'o':
                        result.o = 1
                    result.save()
                else:
                    if zi_type[0] == 'x':
                        hanzi.objects.create(zi=zi,x=1,c=0,k=0,l=0,z=0,g=0,o=0,count=0)
                    if zi_type[0] == 'c':
                        hanzi.objects.create(zi=zi,x=0,c=1,k=0,l=0,z=0,g=0,o=0,count=0)
                    if zi_type[0] == 'k':
                        hanzi.objects.create(zi=zi,x=0,c=0,k=1,l=0,z=0,g=0,o=0,count=0)
                    if zi_type[0] == 'l':
                        hanzi.objects.create(zi=zi,x=0,c=0,k=0,l=1,z=0,g=0,o=0,count=0)
                    if zi_type[0] == 'z':
                        hanzi.objects.create(zi=zi,x=0,c=0,k=0,l=0,z=1,g=0,o=0,count=0)
                    if zi_type[0] == 'g':
                        hanzi.objects.create(zi=zi,x=0,c=0,k=0,l=0,z=0,g=1,o=0,count=0)
                    if zi_type[0] == 'o':
                        hanzi.objects.create(zi=zi,x=0,c=0,k=0,l=0,z=0,g=0,o=1,count=0)
    return True
        
def write_data(zi,zitype,author,no=None,path=None,url=None,binaryfile=None,status=None):
    rlt = zidetail.objects.filter(zi=zi,zitype=zitype,author=author,no=no)
    if not rlt:
        zidetail.objects.create(zi=zi,zitype=zitype,author=author,no=no,url=url,status=0)
    else:
        print('已存在')


def downloadfile(file,url):
    r = requests.get(url)
    file = file.split(' - ')
    filename = file[1]+'-'+file[2]+'-'+file[0]+'-'+os.path.basename(url)
    print(filename)
    with open('d:/shufa/'+filename,'wb') as code:
        code.write(r.content)
        
def multi_get_letter(str_input):
    '''获取多个汉字首字母'''
    if isinstance(str_input, str):
        unicode_str = str_input
    else:
        try:
            unicode_str = str_input.decode('utf8')
        except:
            try:
                unicode_str = str_input.decode('gbk')
            except:
                print ('unknown coding')
                return
      
    return_list = []
    for one_unicode in unicode_str:
        return_list.append(single_get_first(one_unicode))
    return return_list
  
def single_get_first(unicode1):
    '''获取单个汉字首字母'''
    str1 = unicode1.encode('gbk')
    try:        
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''
  
def get_first_letter(str_input):
    '''获取多个汉字首字母'''
    a = multi_get_letter(str_input)
    b = ''
    for i in a:
        if type(i).__name__ =='bytes':
            i = i.decode()
        c = str(i)
        b= b+c
    return b

if __name__=="__main__":
    reqdata('来','行书','')
    

