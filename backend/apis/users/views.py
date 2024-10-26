import json
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from lxml import etree


@csrf_exempt  # 禁用 CSRF 验证，适用于开发环境
def register(request):
    from .models import User
    if request.method == 'POST':
        # 获取前端发送的用户注册信息

        data=json.loads(request.body)

        classid= data.get('classid')
        studentid= data.get('studentid')
        name= data.get('name')
        teamname= data.get('teamname')
        pwd= data.get('pwd')
        phone= data.get('phone')



        session=requests.Session()
        response_register={}
        url_register1='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/default.aspx?vdir=2&vdxmc=%e5%86%b3%e7%ad%96%e6%94%af%e6%8c%81%e7%b3%bb%e7%bb%9f%e5%af%bc%e8%ae%ba&vrjslogin=True'
        data_register1={
            '__EVENTTARGET':'', 
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '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',
            '__VIEWSTATEGENERATOR': 'A3C0820E',
            '__EVENTVALIDATION': '/wEdAAQzAciB/QDW6zkymZaSNIWsHZ4wi8ny7Ddjn7Rp4o1bKeH0Iu/9fZc467JXyMTUE04rU8x5SglfzmEU2KqYFKCXUPtFZlhnqU6SzCMo4bcRBiEMcQ00d/JzNIc16qX0s38=',
            'stuid':'' ,
            'mima': '',
            'ueser': '注册',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }

        response1=session.post(url=url_register1,data=data_register1)


        url_register2='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/use/reg.aspx'
        data_register2={
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUKMTk3OTc1ODE0M2RkOq5HnWF3CwUF3/6MTeJ8KaJDyAukzzz7iwXJh+AQ0Q8=',
            '__VIEWSTATEGENERATOR': 'A1B8A72B',
            '__EVENTVALIDATION': '/wEdAAnnjSdDfwIDrciwYcRtgns4yeS6Quj9IO0OUa7RlabC7oiGpBojjKW+kZ9HnEKOH8vfgBFNPpDgBU7XwLWjc/5wt1gMyoo6rwGWs+lip0/f7nMSsyduhzsT/f3nm0F9rdN0cGHhZ/l61QhuVoEqzzBfo/c0wzpF4mGkADUW7iUvA8VPz8p2oEzmd5kzBEgRc79WR957p/uNC3nhY8nb2xPyLAJjjVfIWN1Bba+kLqXmRg==',
            'classtxt': classid,
            'numberTxt': studentid,
            'nameTxt': name,
            'usersnameTXT': teamname,
            'pwdTxt': pwd,
            'phoneTxt': phone,
            'ok': '确认注册',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }

        response2=session.post(url=url_register2,data=data_register2)
        # 解析返回的页面
        soup = BeautifulSoup(response2.text, 'html.parser')
        # 返回注册提示：如注册成功，学号已存在等
        smessage = soup.find('span', {'id': 'Label7'})
        if smessage.text[:4] == '注册成功':
            parts = smessage.text.split('第')
            response_register['status'] = 'True'
            response_register['data']={}
            response_register['data']['group'] = parts[1].split('组')[0]
            response_register['data']['number'] = parts[2].split('企业')[0]
                    # 创建用户对象并保存到数据库
            new_user = User(
                user_class=classid,   # 对应模型中的字段
                studentid=studentid,
                name=name,
                teamname=teamname,
                pwd=pwd,
                phone=phone,
                group=response_register['data']['group'],
                number=response_register['data']['number']
            )
            new_user.save()  # 保存到数据库中
        else:
            response_register['status'] = 'False'
            response_register['data']={}
            response_register['data']['registertxt'] = smessage.text
        # 返回注册结果给前端
        return JsonResponse(response_register)
    else:
        return HttpResponse('.....')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 获取前端发送的登录信息

        data=json.loads(request.body)

        username = data.get('username')
        password = data.get('password')

        session=requests.Session()

        url_login1='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/default.aspx?vdir=2&vdxmc=%e5%86%b3%e7%ad%96%e6%94%af%e6%8c%81%e7%b3%bb%e7%bb%9f%e5%af%bc%e8%ae%ba&vrjslogin=True'
        data_login1={
            '__EVENTTARGET':'', 
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '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',
            '__VIEWSTATEGENERATOR':'A3C0820E',
            '__EVENTVALIDATION': '/wEdAAQzAciB/QDW6zkymZaSNIWsHZ4wi8ny7Ddjn7Rp4o1bKeH0Iu/9fZc467JXyMTUE04rU8x5SglfzmEU2KqYFKCXUPtFZlhnqU6SzCMo4bcRBiEMcQ00d/JzNIc16qX0s38=',
            'stuid':username,
            'mima':password,
            'login': '登录',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }

        response1=session.post(url=url_login1,data=data_login1)
        # 解析返回的页面
        soup = BeautifulSoup(response1.text, 'html.parser')

        smessage = soup.find('span', {'id': 'Label4'})

        response_login={}
        # 返回登录结果给前端
        if smessage is None:
            # 登录成功，保存会话信息到 Django 的 session 中
            request.session['session_cookies'] = session.cookies.get_dict()
            response_login['status'] = 'True'
            response_login['data'] = {}
            #爬取目标网站
            url_login2='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/select.aspx'
            response2=session.get(url=url_login2)

            # 解析HTML内容
            tree=etree.HTML(response2.text)
            # 使用XPath定位元素
            element2= tree.xpath('//font[@color="#ff0000"]/text()')
            # 提取第一个字符串
            text = element2[0]
            # 使用字符串切片方法提取数字
            response_login['data']['group'] = int(text[text.index('第')+1:text.index('组')])
            response_login['data']['number'] = int(text[text.index('组第')+2:text.index('企业')])
            response_login['data']['rival'] = int(text[text.index('仅有')+2:text.index(' 位')])
            response_login['data']['cycle'] = element2[1]
        else:
            response_login['status'] = 'False'
            response_login['data'] = {}
            response_login['data']['logintxt'] = smessage.text
        response_login['data'] = {
        'sessionid': session.cookies.get('sessionid')  
    }
        response = JsonResponse(response_login)
        response.set_cookie('sessionid', response_login['data']['sessionid'], httponly=True, secure=True) 
        return response


    else:
        return HttpResponse('.....')

@csrf_exempt
def look1(request):
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)
    response_look1={}

    #爬取目标网站
    url_look1='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/mtrend/mtrend.aspx'
    response1=session.get(url=url_look1)
    # 解析HTML内容
    tree=etree.HTML(response1.text)

    # 使用XPath定位元素
    # 例如，定位一个包含特定文本的元素
    element1 = tree.xpath('//font[translate(@color, "F", "f")="#ffffff" and @style="font-size:18px"]/text()')
    element2 = tree.xpath('//font[@color="#000000" and @style="font-size:18px"]/text()')
    element3 = tree.xpath('//font[@class="title"]/text()')
    # 删除字段中的 \xa0
    cleaned_element1 = [text.replace('\xa0', '') for text in element1]
    cleaned_element2 = [text.replace('\xa0', '') for text in element2]
    cleaned_element3 = [text.replace('\xa0', '') for text in element3]
    cleaned_element1 = [element.lstrip('·') for element in cleaned_element1]
    response_looknow={}
    response_looknow['标题']=cleaned_element3[0]
    for i,j in zip(cleaned_element1,cleaned_element2):
        response_looknow[i]=j
    response_look1[response_looknow['标题']]=response_looknow

    while len(response_looknow['标题'])<16:
        url_look1_switchover='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/mtrend/mtrend.aspx'
        data_look1_switchover={
            '__VIEWSTATE': '/wEPDwUKMTk0OTkyNTkwOQ9kFgJmD2QWAgIDD2QWAgIBD2QWBAIEDxYCHgdWaXNpYmxlaBYCAgEPZBYEAgEPDxYCHgRUZXh0BTXnrKwgMSDlkajmnJ/miqXlkYrlt7LmmK/lj6/nnIvnmoTmnIDml6nmiqXlkYrvvIw8YnIvPmRkAgMPDxYCHwFlZGQCCA8WAh8AaBYCAgEPZBYCAgEPDxYCHwEFNiA8YnIvPuesrCA3IOWRqOacn+aKpeWRiuW3suaYr+WPr+eci+eahOacgOWQjuaKpeWRiu+8gWRkZBmTd+AeDzUNQa2vzCRT56lsSWQmVcW0na2NEIfHf9Tc',
            '__VIEWSTATEGENERATOR': '94DCD150',
            '__EVENTVALIDATION': '/wEdAAaI5UnofgfVCsO/QLIHFqLpufKS5sa+yJvJjw+5JY9vLwktJF0MZ56SB8vS/XZ5neQ6okqFUwKhyoUSfg2h7Mgo1dNSXck49YdW1B5T4adaDrk4TCrBr5sOTl9xSqNj9zDQiHzVrlf2wb7y+XRSWNi82if6HN5I9VzZLdku/7Y22A==',
            'ctl00$contentplaceholder1$ober': '上一周期',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }
        response1=session.post(url=url_look1_switchover,data=data_look1_switchover)
        # 解析HTML内容
        tree=etree.HTML(response1.text)
        # 使用XPath定位元素
        # 例如，定位一个包含特定文本的元素
        element1 = tree.xpath('//font[translate(@color, "F", "f")="#ffffff" and @style="font-size:18px"]/text()')
        element2 = tree.xpath('//font[@color="#000000" and @style="font-size:18px"]/text()')
        element3 = tree.xpath('//font[@class="title"]/text()')
        # 删除字段中的 \xa0
        cleaned_element1 = [text.replace('\xa0', '') for text in element1]
        cleaned_element2 = [text.replace('\xa0', '') for text in element2]
        cleaned_element3 = [text.replace('\xa0', '') for text in element3]
        cleaned_element1 = [element.lstrip('·') for element in cleaned_element1]
        response_looknow={}
        response_looknow['标题']=cleaned_element3[0]
        for i,j in zip(cleaned_element1,cleaned_element2):
            response_looknow[i]=j
        response_look1[response_looknow['标题']]=response_looknow
    # 将字典项转换为列表并倒序
    reversed_items = list(response_look1.items())[::-1]

    # 将倒序后的列表转换回字典
    response_look1 = dict(reversed_items)
    if len(response_look1)<7:
        for i in range(len(response_look1),8-len(response_look1)):
            response_look1['第'+str(i+1)+'周期市场形势报告']='无'
    return JsonResponse(response_look1)



@csrf_exempt
def lookhistory(request):
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)

    url_lookhistory='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/mtrend/mtrend.aspx'
    data_lookhistory={
        '__VIEWSTATE': '/wEPDwUKMTk0OTkyNTkwOWRkcH+X8uLl91V+Wwn59cMAChdkvb49cBtIUw1ctC5d2vI=',
        '__VIEWSTATEGENERATOR': '94DCD150',
        '__EVENTVALIDATION': '/wEdAAas194nENGdrO9KNXirw1X2ufKS5sa+yJvJjw+5JY9vLwktJF0MZ56SB8vS/XZ5neQ6okqFUwKhyoUSfg2h7Mgo1dNSXck49YdW1B5T4adaDrk4TCrBr5sOTl9xSqNj9zArqoVeHawAFMgtV364YEwGDV0dgpUkABn/BNQJlgqepA==',
        'ctl00$contentplaceholder1$back': '历史平均',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }

    response1=session.post(url=url_lookhistory,data=data_lookhistory)
    # 解析返回的页面
    soup = BeautifulSoup(response1.text, 'html.parser')

    # 解析HTML内容
    tree=etree.HTML(response1.text)

    # 使用XPath定位元素
    # 例如，定位一个包含特定文本的元素
    element2 = tree.xpath('//font[@color="#000000" and @style="font-size: 16px"]/text()')
    element3 = tree.xpath('//font[@class="title"]/text()')
    # 删除字段中的 \xa0

    cleaned_element2 = [text.replace('\xa0', '') for text in element2]
    cleaned_element3 = [text.replace('\xa0', '') for text in element3]
    data_list=cleaned_element2

    response_lookhistory={}
    response_lookhistory['标题']=cleaned_element3[0]


    # Extracting order quantities and unit prices
    response_lookhistory['订购批量_批量范围'] = data_list[0:12:3]
    response_lookhistory['订购批量_原材料单价（元）'] = data_list[1:12:3]
    response_lookhistory['订购批量_附件单价（元）'] = data_list[2:12:3]

    # Extracting department salaries
    response_lookhistory['部门'] = data_list[12:22:2]
    response_lookhistory['年薪（万元）'] = data_list[13:22:2]

    # Extracting fund types and amounts
    response_lookhistory['资金类型'] = data_list[22::2]
    response_lookhistory['数额（万元）'] = data_list[23::2]
    return JsonResponse(response_lookhistory)

