import json
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from lxml import etree
import re

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
            response_login['data'] = {
            'sessionid': session.cookies.get('sessionid')  
        }            
            response_login['data']['group'] = int(text[text.index('第')+1:text.index('组')])
            response_login['data']['number'] = int(text[text.index('组第')+2:text.index('企业')])
            response_login['data']['rival'] = int(text[text.index('仅有')+2:text.index(' 位')])
            # 提取 'cycle' 并转换为阿拉伯数字
            cycle_str = element2[2].strip()
            chinese_to_arabic = {
                '一': 1,
                '二': 2,
                '三': 3,
                '四': 4,
                '五': 5,
                '六': 6,
                '七': 7
            }
            cycle_num = chinese_to_arabic.get(cycle_str, 0)  # 若未找到对应的中文数字，默认值为0
            response_login['data']['cycle'] = cycle_num
        else:
            response_login['status'] = 'False'
            response_login['data'] = {}
            response_login['data']['logintxt'] = smessage.text

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
        for i in range(len(response_look1),7):
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



@csrf_exempt
def commit_decision(request):

    data = json.loads(request.body)
    general_market_price = data.get('general_market_price')  # 一般市场价格（元/台）
    advertising_investment = data.get('advertising_investment')  # 广告费用投入（百万元）
    sales_staff = data.get('sales_staff')  # 销售人员人数（个）
    market_research_report = data.get('market_research_report')  # 市场和生产研究报告（Y/N）
    bid_price = data.get('bid_price')  # 附件一：投标价格（元/台）
    special_product_qty = data.get('special_product_qty')  # 附件二：特殊产品数（台）
    production_plan_qty = data.get('production_plan_qty')  # 一般市场产品计划量（台）
    production_line_investment = data.get('production_line_investment')  # 生产线投资（条）
    production_line_change = data.get('production_line_change')  # 生产线变卖（条）
    maintenance_cost = data.get('maintenance_cost')  # 维护保养费用（百万元）
    production_optimization_investment = data.get('production_optimization_investment')  # 生产合理化投资（百万元）
    production_staff_recruitment = data.get('production_staff_recruitment')  # 生产人员招收数（个）
    production_staff_resignation = data.get('production_staff_resignation')  # 生产人员辞退数（个）
    purchase_robot = data.get('purchase_robot')  # 购买机器人（个）
    raw_material_purchase_qty = data.get('raw_material_purchase_qty')  # 购买原材料量（单位）
    purchase_accessories = data.get('purchase_accessories')  # 购买附件量（单位）
    research_staff_recruitment = data.get('research_staff_recruitment')  # 科研人员招收数（个）
    research_staff_resignation = data.get('research_staff_resignation')  # 科研人员辞退数（个）
    product_improvement_cost = data.get('product_improvement_cost')  # 产品改进费用（百万元）
    social_benefits = data.get('social_benefits')  # 社会福利费用（%）
    medium_term_loan = data.get('medium_term_loan')  # 中期贷款（百万元）
    purchase_securities = data.get('purchase_securities')  # 购买有价证券（百万元）
    planned_dividend_payment = data.get('planned_dividend_payment')  # 计划支付股息（百万元）
    management_optimization_investment = data.get('management_optimization_investment')  # 管理合理化投资（百万元）

    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)
    url_update_decision_data='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/adddata/dataadd.aspx'
    response = session.get(url_update_decision_data)

    def extract_hidden_fields(soup):                   #定义提取页面中的所有隐藏字段的函数
        hidden_fields = {}
        for hidden in soup.find_all('input', type='hidden'):
            name = hidden.get('name')
            value = hidden.get('value', '')
            if name:
                hidden_fields[name] = value
        return hidden_fields
    
    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_fields = extract_hidden_fields(soup)
    data_update_decision_data={
        '__VIEWSTATE': hidden_fields.get('__VIEWSTATE', ''),
        '__VIEWSTATEGENERATOR': hidden_fields.get('__VIEWSTATEGENERATOR', ''),
        '__EVENTVALIDATION': hidden_fields.get('__EVENTVALIDATION', ''),
        'ctl00$contentplaceholderadd$prd5': general_market_price,
        'ctl00$contentplaceholderadd$wed5': advertising_investment,
        'ctl00$contentplaceholderadd$hzd5': sales_staff,
        'ctl00$contentplaceholderadd$mfd5': market_research_report,
        'ctl00$contentplaceholderadd$fed5': bid_price,
        'ctl00$contentplaceholderadd$fzd5': special_product_qty,
        'ctl00$contentplaceholderadd$rsd5': raw_material_purchase_qty,
        'ctl00$contentplaceholderadd$zbd5': purchase_accessories,
        'ctl00$contentplaceholderadd$end5': research_staff_recruitment,
        'ctl00$contentplaceholderadd$eld5': research_staff_resignation,
        'ctl00$contentplaceholderadd$vad5': product_improvement_cost,
        'ctl00$contentplaceholderadd$pnd5': production_plan_qty,
        'ctl00$contentplaceholderadd$smd5': production_line_investment,
        'ctl00$contentplaceholderadd$swd5': production_line_change,
        'ctl00$contentplaceholderadd$ikd5': maintenance_cost,
        'ctl00$contentplaceholderadd$rkd5': production_optimization_investment,
        'ctl00$contentplaceholderadd$nsd5': production_staff_recruitment,
        'ctl00$contentplaceholderadd$nld5': production_staff_resignation,
        'ctl00$contentplaceholderadd$rbd5': purchase_robot ,
        'ctl00$contentplaceholderadd$zsd5': social_benefits,
        'ctl00$contentplaceholderadd$mkd5': medium_term_loan,
        'ctl00$contentplaceholderadd$wkd5': purchase_securities,
        'ctl00$contentplaceholderadd$gdd5': planned_dividend_payment,
        'ctl00$contentplaceholderadd$vid5': management_optimization_investment,
        'ctl00$contentplaceholderadd$submit1.x':78,
        'ctl00$contentplaceholderadd$submit1.y':28,
        'ctl00$contentplaceholderadd$pb5':hidden_fields.get('ctl00$contentplaceholderadd$pb5', ''),
        'ctl00$contentplaceholderadd$zyzj55':hidden_fields.get('ctl00$contentplaceholderadd$zyzj55', ''),
        'ctl00$contentplaceholderadd$eb5':hidden_fields.get('ctl00$contentplaceholderadd$eb5', ''),
        'ctl00$contentplaceholderadd$fs5':hidden_fields.get('ctl00$contentplaceholderadd$fs5', ''),
        'ctl00$contentplaceholderadd$fz5':hidden_fields.get('ctl00$contentplaceholderadd$fz5', ''),
        'ctl00$contentplaceholderadd$zyzj5':hidden_fields.get('ctl00$contentplaceholderadd$zyzj5', ''),
        'ctl00$contentplaceholderadd$ff5': hidden_fields.get('ctl00$contentplaceholderadd$ff5', ''), 
        'ctl00$contentplaceholderadd$rz5': hidden_fields.get('ctl00$contentplaceholderadd$rz5', ''), 
        'ctl00$contentplaceholderadd$rf5': hidden_fields.get('ctl00$contentplaceholderadd$rf5', ''),
        'ctl00$contentplaceholderadd$gr5': hidden_fields.get('ctl00$contentplaceholderadd$gr5', ''), 
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    response_update_decision_data = session.post(url_update_decision_data, data_update_decision_data)


    response_submit_decision_data={}
    if "决策数据已经成功递交" in response_update_decision_data.text: 
        response_submit_decision_data['提交结果']="决策数据已经成功递交"

        #递交决策数据第一次post请求
        url_sub1 = 'http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/select.aspx'
        response_sub1 = session.get(url_sub1)
        soup_sub1= BeautifulSoup(response_sub1.text, 'html.parser')
        hidden_fields_sub1 = extract_hidden_fields(soup_sub1)
        data_sub1 = {
            '__EVENTTARGET': 'caculbt',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': hidden_fields_sub1.get('__VIEWSTATE', ''),
            '__VIEWSTATEGENERATOR': hidden_fields_sub1.get('__VIEWSTATEGENERATOR', ''),
            '__EVENTVALIDATION': hidden_fields_sub1.get('__EVENTVALIDATION', ''),
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }
        response_sub1 = session.post(url_sub1, data_sub1)

        #递交决策数据第二次post请求
        soup_sub2 = BeautifulSoup(response_sub1.text, 'html.parser')
        hidden_fields_sub2 = extract_hidden_fields(soup_sub2)
        data_sub2 = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': hidden_fields_sub2.get('__VIEWSTATE', ''),
            '__VIEWSTATEGENERATOR': hidden_fields_sub2.get('__VIEWSTATEGENERATOR', ''),
            '__EVENTVALIDATION': hidden_fields_sub2.get('__EVENTVALIDATION', ''),
            'ImageButton3.x': 46,
            'ImageButton3.y': 24,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }
        url_sub2 = 'http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/select.aspx'
        response_sub2 = session.post(url_sub2, data_sub2)


        #递交决策数据第三次post请求
        soup_sub3 = BeautifulSoup(response_sub2.text, 'html.parser')
        hidden_fields_sub3 = extract_hidden_fields(soup_sub3)
        url_sub3='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/select.aspx'
        data_sub3 = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': hidden_fields_sub3.get('__VIEWSTATE', ''),
            '__VIEWSTATEGENERATOR': hidden_fields_sub3.get('__VIEWSTATEGENERATOR', ''),
            '__EVENTVALIDATION': hidden_fields_sub3.get('__EVENTVALIDATION', ''),
            'ImageButton3.x': 46,
            'ImageButton3.y': 24,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
        }
        response_submit3 = session.post(url_sub3, data_sub3)


    else:
        soup = BeautifulSoup(response_update_decision_data.text, 'html.parser')
        response_submit_decision_data['提交结果']=soup.select_one("#contentplaceholderadd_Label8").text 
    return JsonResponse(response_submit_decision_data)       


@csrf_exempt
def historical_decision(request):
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)
    #爬取目标网站
    url='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/adddata/dataadd.aspx'

    def extract_hidden_fields(soup,type):                   #定义提取页面中的所有隐藏字段的函数
        hidden_fields = {}
        for hidden in soup.find_all('input', type=type):
            name = hidden.get('name')
            value = hidden.get('value', '')
            if name:
                hidden_fields[name] = value
        return hidden_fields

    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_fields1 = extract_hidden_fields(soup,'hidden')
    hidden_fields2 = extract_hidden_fields(soup,'text')

    #mfd5的定位方式不同，所以单独处理
    mfd5 = soup.find('select', id='contentplaceholderadd_mfd5')
    mfd5_option = mfd5.find('option', selected=True)
    smfd5_value = mfd5_option.get('value')
    # 构造提交数据
    data = {
        '__VIEWSTATE': hidden_fields1.get('__VIEWSTATE', ''),
        '__VIEWSTATEGENERATOR': hidden_fields1.get('__VIEWSTATEGENERATOR', ''),
        '__EVENTVALIDATION': hidden_fields1.get('__EVENTVALIDATION', ''),
        'ctl00$contentplaceholderadd$prd5': hidden_fields2.get('ctl00$contentplaceholderadd$prd5', ''), 
        'ctl00$contentplaceholderadd$wed5': hidden_fields2.get('ctl00$contentplaceholderadd$wed5', ''),     
        'ctl00$contentplaceholderadd$hzd5': hidden_fields2.get('ctl00$contentplaceholderadd$hzd5', ''),  
        'ctl00$contentplaceholderadd$mfd5': smfd5_value,   
        'ctl00$contentplaceholderadd$fed5': hidden_fields2.get('ctl00$contentplaceholderadd$fed5', ''),   
        'ctl00$contentplaceholderadd$fzd5': hidden_fields2.get('ctl00$contentplaceholderadd$fzd5', ''),
        'ctl00$contentplaceholderadd$rsd5': hidden_fields2.get('ctl00$contentplaceholderadd$rsd5', ''), 
        'ctl00$contentplaceholderadd$zbd5': hidden_fields2.get('ctl00$contentplaceholderadd$end5', ''),  
        'ctl00$contentplaceholderadd$end5': hidden_fields2.get('ctl00$contentplaceholderadd$end5', ''),  
        'ctl00$contentplaceholderadd$eld5': hidden_fields2.get('ctl00$contentplaceholderadd$eld5', ''),    
        'ctl00$contentplaceholderadd$vad5': hidden_fields2.get('ctl00$contentplaceholderadd$vad5', ''),
        'ctl00$contentplaceholderadd$pnd5': hidden_fields2.get('ctl00$contentplaceholderadd$pnd5', ''), 
        'ctl00$contentplaceholderadd$smd5': hidden_fields2.get('ctl00$contentplaceholderadd$smd5', ''),    
        'ctl00$contentplaceholderadd$swd5': hidden_fields2.get('ctl00$contentplaceholderadd$swd5', ''),   
        'ctl00$contentplaceholderadd$ikd5': hidden_fields2.get('ctl00$contentplaceholderadd$ikd5', ''),  
        'ctl00$contentplaceholderadd$rkd5': hidden_fields2.get('ctl00$contentplaceholderadd$rkd5', ''),    
        'ctl00$contentplaceholderadd$nsd5': hidden_fields2.get('ctl00$contentplaceholderadd$nsd5', ''),    
        'ctl00$contentplaceholderadd$nld5': hidden_fields2.get('ctl00$contentplaceholderadd$nld5', ''),    
        'ctl00$contentplaceholderadd$rbd5': hidden_fields2.get('ctl00$contentplaceholderadd$rbd5', ''),   
        'ctl00$contentplaceholderadd$zsd5': hidden_fields2.get('ctl00$contentplaceholderadd$zsd5', ''),  
        'ctl00$contentplaceholderadd$mkd5': hidden_fields2.get('ctl00$contentplaceholderadd$mkd5', ''),    
        'ctl00$contentplaceholderadd$wkd5': hidden_fields2.get('ctl00$contentplaceholderadd$wkd5', ''),    
        'ctl00$contentplaceholderadd$gdd5': hidden_fields2.get('ctl00$contentplaceholderadd$gdd5', ''),  
        'ctl00$contentplaceholderadd$vid5': hidden_fields2.get('ctl00$contentplaceholderadd$vid5', ''),   
        'ctl00$contentplaceholderadd$history.x':59,
        'ctl00$contentplaceholderadd$history.y': 25,
        'ctl00$contentplaceholderadd$pb5':hidden_fields1.get('ctl00$contentplaceholderadd$pb5', ''),
        'ctl00$contentplaceholderadd$zyzj55':hidden_fields1.get('ctl00$contentplaceholderadd$zyzj55', ''),
        'ctl00$contentplaceholderadd$eb5':hidden_fields1.get('ctl00$contentplaceholderadd$eb5', ''),
        'ctl00$contentplaceholderadd$fs5':hidden_fields1.get('ctl00$contentplaceholderadd$fs5', ''),
        'ctl00$contentplaceholderadd$fz5':hidden_fields1.get('ctl00$contentplaceholderadd$fz5', ''),
        'ctl00$contentplaceholderadd$zyzj5':hidden_fields1.get('ctl00$contentplaceholderadd$zyzj5', ''),
        'ctl00$contentplaceholderadd$ff5': hidden_fields1.get('ctl00$contentplaceholderadd$ff5', ''), 
        'ctl00$contentplaceholderadd$rz5': hidden_fields1.get('ctl00$contentplaceholderadd$rz5', ''), 
        'ctl00$contentplaceholderadd$rf5': hidden_fields1.get('ctl00$contentplaceholderadd$rf5', ''),
        'ctl00$contentplaceholderadd$gr5': hidden_fields1.get('ctl00$contentplaceholderadd$gr5', ''), 
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    response=session.post(url,data,headers=headers)
    # 解析HTML内容
    tree=etree.HTML(response.text)
    # 使用XPath定位元素

    element1 = tree.xpath('//a[@class="light"]/text()')
    element2 = tree.xpath('//input[starts-with(@id, "contentplaceholderadd_")]/@value')
    element3 = tree.xpath('//option[@selected="selected"]/@value')
    element2 =element2[0:23]
    element1.insert(0, '一般市场价格')
    element2.insert(3, element3[0])
    element4 = tree.xpath('//span[@style="font-size: 36px"]/text()')
    element4 = [text.replace('\xa0 ', '') for text in element4]


    response_historical_decision={}
    response_historical_decision[element4[0]]={}
    for i,j in zip(element1,element2):
        response_historical_decision[element4[0]][i]=j


    for i in range(0,7):
        url='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/adddata/historydataadd.aspx'
        soup = BeautifulSoup(response.text, 'html.parser')
        hidden_fields1 = extract_hidden_fields(soup,'hidden')
        hidden_fields2 = extract_hidden_fields(soup,'text')
        #mfd5的定位方式不同，所以单独处理
        mfd5 = soup.find('select', id='contentplaceholderadd_mfd5')
        mfd5_option = mfd5.find('option', selected=True)
        mfd5_value = mfd5_option.get('value')
        data = {
                '__VIEWSTATE': hidden_fields1.get('__VIEWSTATE', ''),
                '__VIEWSTATEGENERATOR': hidden_fields1.get('__VIEWSTATEGENERATOR', ''),
                '__EVENTVALIDATION': hidden_fields1.get('__EVENTVALIDATION', ''),
                'ctl00$contentplaceholderadd$prd5': hidden_fields2.get('ctl00$contentplaceholderadd$prd5', ''),
                'ctl00$contentplaceholderadd$wed5': hidden_fields2.get('ctl00$contentplaceholderadd$wed5', ''),
                'ctl00$contentplaceholderadd$hzd5': hidden_fields2.get('ctl00$contentplaceholderadd$hzd5', ''),
                'ctl00$contentplaceholderadd$mfd5': mfd5_value,
                'ctl00$contentplaceholderadd$fed5': hidden_fields2.get('ctl00$contentplaceholderadd$fed5', ''),
                'ctl00$contentplaceholderadd$fzd5': hidden_fields2.get('ctl00$contentplaceholderadd$fzd5', ''),
                'ctl00$contentplaceholderadd$rsd5': hidden_fields2.get('ctl00$contentplaceholderadd$rsd5', ''),
                'ctl00$contentplaceholderadd$zbd5': hidden_fields2.get('ctl00$contentplaceholderadd$zbd5', ''),
                'ctl00$contentplaceholderadd$end5': hidden_fields2.get('ctl00$contentplaceholderadd$end5', ''),
                'ctl00$contentplaceholderadd$eld5': hidden_fields2.get('ctl00$contentplaceholderadd$eld5', ''),
                'ctl00$contentplaceholderadd$vad5': hidden_fields2.get('ctl00$contentplaceholderadd$vad5', ''),
                'ctl00$contentplaceholderadd$pnd5': hidden_fields2.get('ctl00$contentplaceholderadd$pnd5', ''),
                'ctl00$contentplaceholderadd$smd5': hidden_fields2.get('ctl00$contentplaceholderadd$smd5', ''),
                'ctl00$contentplaceholderadd$swd5': hidden_fields2.get('ctl00$contentplaceholderadd$swd5', ''),
                'ctl00$contentplaceholderadd$ikd5': hidden_fields2.get('ctl00$contentplaceholderadd$ikd5', ''),
                'ctl00$contentplaceholderadd$rkd5': hidden_fields2.get('ctl00$contentplaceholderadd$rkd5', ''),
                'ctl00$contentplaceholderadd$nsd5': hidden_fields2.get('ctl00$contentplaceholderadd$nsd5', ''),
                'ctl00$contentplaceholderadd$nld5': hidden_fields2.get('ctl00$contentplaceholderadd$nld5', ''),
                'ctl00$contentplaceholderadd$rbd5': hidden_fields2.get('ctl00$contentplaceholderadd$rbd5', ''),
                'ctl00$contentplaceholderadd$zsd5': hidden_fields2.get('ctl00$contentplaceholderadd$zsd5', ''),
                'ctl00$contentplaceholderadd$mkd5': hidden_fields2.get('ctl00$contentplaceholderadd$mkd5', ''),
                'ctl00$contentplaceholderadd$wkd5': hidden_fields2.get('ctl00$contentplaceholderadd$wkd5', ''),
                'ctl00$contentplaceholderadd$gdd5': hidden_fields2.get('ctl00$contentplaceholderadd$gdd5', ''),
                'ctl00$contentplaceholderadd$vid5': hidden_fields2.get('ctl00$contentplaceholderadd$vid5', ''),
                'ctl00$contentplaceholderadd$ober': '上一周期',
            }
        response=session.post(url,data,headers=headers)

        # 解析HTML内容
        tree=etree.HTML(response.text)
        # 使用XPath定位元素

        element1 = tree.xpath('//a[@class="light"]/text()')
        element2 = tree.xpath('//input[starts-with(@id, "contentplaceholderadd_")]/@value')
        element3 = tree.xpath('//option[@selected="selected"]/@value')
        element2 =element2[0:23]
        element1.insert(0, '一般市场价格')
        element2.insert(3, element3[0])
        element4 = tree.xpath('//span[@style="font-size: 36px"]/text()')
        element4 = [text.replace('\xa0 ', '') for text in element4]
        response_historical_decision[element4[0]]={}
        for i,j in zip(element1,element2):
            response_historical_decision[element4[0]][i]=j
        if len(element4[0])>14:
            break

    # 将字典项转换为列表并倒序
    reversed_items = list(response_historical_decision.items())[::-1]

    # 将倒序后的列表转换回字典
    response_historical_decision = dict(reversed_items)

    if len(response_historical_decision)<7:
        for i in range(len(response_historical_decision),7):
            response_historical_decision['查看第'+str(i+1)+'周期决策数据']='无'

    return JsonResponse(response_historical_decision)


@csrf_exempt
def compete_outcome(request):
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)
    #爬取目标网站
    url='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/result/result.aspx?type=1'
    response=session.get(url=url)


    # 解析HTML内容
    tree=etree.HTML(response.text)

    # 使用XPath定位元素
    element1 = tree.xpath('//font[@style="font-size:17px"]/text()')
    cleaned_element1 = [text.replace('\xa0', '') for text in element1]
    element2 = tree.xpath('//font[@style="font-size: 24px;"]/text()')
    cleaned_element2 = [text.replace('\xa0', '') for text in element2]
    cleaned_element1 = cleaned_element1[2:-1]



    # 初始化空字典用于存储结果
    compete_outcome = {}
    compete_outcome['标题'] = cleaned_element2[0]
    # 按步长4遍历列表（标签、单位、值1、值2）
    for i in range(0, len(cleaned_element1), 4):
        # 提取标签和值
        label = cleaned_element1[i]         # 标签
        value1 = cleaned_element1[i+2]      # 企业1的值
        value2 = cleaned_element1[i+3]      # 企业2的值
        
        # 将标签作为键，两个值作为列表存储在字典中
        compete_outcome[label] = [value1, value2]
    return JsonResponse(compete_outcome)  




@csrf_exempt
def enterreporting(request):
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)
    response_enterreporting={} 
    report_data = [
        ['market', "http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/market.aspx?type=", '市场生产数据报告'],
        ['cost_ctype', "http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/cost/ctype.aspx?type=", '产品成本类型核算报告'],
        ['cost_cdept','http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/cost/cdept.aspx?type=', '成本发生部门核算报告'],
        ['cost_ccell','http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/cost/ccell.aspx?type=','成本承担单元核算报告'],
        ['profitlost_prolost','http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/profitlost/prolost.aspx?type=','利润和亏损核算报告'],
        ['profitlost_ptax','http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/profitlost/ptax.aspx?type=','税后利润核算报告'],
        ['profitlost_pdis','http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/profitlost/pdis.aspx?type=','利润分配核算报告'],
        ['financer','http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/financer.aspx?type=','财务报告'],
        ['assetdebt','http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/assetdebt.aspx?type=','资产负债表'],
        ['research','http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/report/research.aspx?type=','各企业市场营销及生产研究报告']
    ]
    for dictl,urll,text in report_data:
        dictl={}
        dict_data=dictl
        url=urll+'1'
        response=session.get(url=url)
        # 解析HTML内容
        tree=etree.HTML(response.text)
        # 使用XPath定位元素
        # 例如，定位一个包含特定文本的元素
        element1 = tree.xpath('//font[@style="font-size:16px"]/text()')
        element2 = tree.xpath('//font[@style="POSITION:relative;top:20px;Z-INDEX:4;font-size: 24px;font-family:隶书;"]/text()')
        element3 = tree.xpath('//font[@style="position:relative;top:15px;Z-INDEX:4;line-height:15px; width:500px;height: 50px;font-size: 40px;font-family:隶书;"]/text()')
        # 删除字段中的 \xa0
        cleaned_element1 = [text.replace('\xa0', '') for text in element1]
        cleaned_element2 = [text.replace('\xa0', '') for text in element2]
        cleaned_element3 = [text.replace('\xa0', '') for text in element3]
        cleaned_element1 = [item.strip() for item in cleaned_element1 if re.search(r'\d', item)]
        if  cleaned_element3:  
            dict_data[cleaned_element3[0]+cleaned_element2[0]]=cleaned_element1
            n=cleaned_element2[0][2]
        else:
            if text=='各企业市场营销及生产研究报告':
                dict_data['各企业市场营销及生产研究报告（第'+n+'周期）']='本周期没有订购市场和生产研究报告！'

        for i in range(int(n)-1,0,-1):
            #爬取目标网站
            url=urll+'3&hcycleno='+str(i)
            response=session.get(url=url)

            # 解析HTML内容
            tree=etree.HTML(response.text)
            # 使用XPath定位元素
            # 例如，定位一个包含特定文本的元素
            element1 = tree.xpath('//font[@style="font-size:16px"]/text()')
            element2 = tree.xpath('//font[@style="POSITION:relative;top:20px;Z-INDEX:4;font-size: 24px;font-family:隶书;"]/text()')
            element3 = tree.xpath('//font[@style="position:relative;top:15px;Z-INDEX:4;line-height:15px; width:500px;height: 50px;font-size: 40px;font-family:隶书;"]/text()')
            # 删除字段中的 \xa0
            cleaned_element1 = [text.replace('\xa0', '') for text in element1]
            cleaned_element2 = [text.replace('\xa0', '') for text in element2]
            cleaned_element3 = [text.replace('\xa0', '') for text in element3]
            cleaned_element1 = [item.strip() for item in cleaned_element1 if re.search(r'\d', item)]
            if cleaned_element3:
                if text=='各企业市场营销及生产研究报告':
                    cleaned_element2[0]=cleaned_element2[0][0]+cleaned_element2[0][6:]
                    dict_data[cleaned_element3[0]+cleaned_element2[0]]=cleaned_element1
                    a=cleaned_element3[0]
                    b=int(cleaned_element2[0][-4])-1
                    c=cleaned_element2[0]
                else:
                    dict_data[cleaned_element3[0]+cleaned_element2[0]]=cleaned_element1
            else:
                if text=='各企业市场营销及生产研究报告':
                    c = c[:len(c) - 4] + str(b) + c[len(c) - 3:]
                    dict_data[a+c]='本周期没有订购市场和生产研究报告！'
        # 将字典项转换为列表并倒序
        reversed_items = list(dict_data.items())[::-1]
        # 将倒序后的列表转换回字典
        dict_data= dict(reversed_items)
            
        if len(dict_data)<7:
            for i in range(len(dict_data),7):
                dict_data[text+'（第'+str(i+1)+'周期）']='无'
        response_enterreporting[text]=dict_data
    return JsonResponse(response_enterreporting)  
