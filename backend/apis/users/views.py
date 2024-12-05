import json
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from lxml import etree
import re
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db import transaction

# 辅助函数：提取隐藏字段
def extract_hidden_fields(soup, type='hidden'):
    """提取页面中的所有隐藏字段"""
    hidden_fields = {}
    for hidden in soup.find_all('input', type=type):
        name = hidden.get('name')
        value = hidden.get('value', '')
        if name:
            hidden_fields[name] = value
    return hidden_fields



@csrf_exempt  # 禁用 CSRF 验证，适用于开发环境
def register(request):
    from .models import User,Round,Cycle
    if request.method == 'POST':
        # 获取前端发送的用户注册信息

        data=json.loads(request.body)

        classid= data.get('classid')
        studentid= data.get('studentid')
        name= data.get('name')
        teamname= data.get('teamname')
        pwd= data.get('pwd')
        phone= data.get('phone')
        email= data.get('email')

        # 检查本地数据库是否已注册
        if User.objects.filter(student_id=studentid).exists():
            response_register={
                'status': 'False',
                'data': {
                    'registertxt': '该账号已被注册'
                }
            }
            return JsonResponse(response_register)
        
        session=requests.Session()
        response_register={}
        url_register1='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/default.aspx?vdir=2&vdxmc=%e5%86%b3%e7%ad%96%e6%94%af%e6%8c%81%e7%b3%bb%e7%bb%9f%e5%af%bc%e8%ae%ba&vrjslogin=True'
        response = session.get(url=url_register1)
        soup = BeautifulSoup(response.text, 'html.parser')
        hidden_fields = extract_hidden_fields(soup)
        data_register1={
            '__EVENTTARGET': hidden_fields.get('__EVENTTARGET', ''),
            '__EVENTARGUMENT': hidden_fields.get('__EVENTARGUMENT', ''),
            '__VIEWSTATE': hidden_fields.get('__VIEWSTATE', ''),
            '__VIEWSTATEGENERATOR': hidden_fields.get('__VIEWSTATEGENERATOR', ''),
            '__EVENTVALIDATION': hidden_fields.get('__EVENTVALIDATION', ''),
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
                student_id=studentid,
                password=pwd,
                name=name,
                user_class=classid,
                team_name=teamname,
                email=email,
                phone=phone,
                group=response_register['data']['group'],
                number=response_register['data']['number']
            )
            new_user.save()  # 保存到数据库中

            new_round =Round(
                uid=new_user,
            )
            new_round.save()  # 保存到数据库中

            new_cycle =Cycle(
                uid=new_user,
                round_id=new_round,
                cycle_number=1,
            )
            new_cycle.save()  # 保存到数据库中

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
    from .models import User
    if request.method == 'POST':
        # 获取前端发送的登录信息

        data=json.loads(request.body)

        stuid = data.get('username')
        password = data.get('password')

        # 检查本地数据库是否已注册
        try:
            user = User.objects.get(student_id=stuid)
        except User.DoesNotExist:
            response_login={
                'status': 'False',
                'data': {
                    'logintxt': '账号未注册'
                }
            }
            return JsonResponse(response_login)

        session=requests.Session()

        # 将用户 UID 保存到会话中
        user = User.objects.get(student_id=stuid)
        request.session['uid'] = user.uid

        url_login1='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/default.aspx?vdir=2&vdxmc=%e5%86%b3%e7%ad%96%e6%94%af%e6%8c%81%e7%b3%bb%e7%bb%9f%e5%af%bc%e8%ae%ba&vrjslogin=True'
        response = session.get(url=url_login1)
        soup = BeautifulSoup(response.text, 'html.parser')
        hidden_fields = extract_hidden_fields(soup)
        
        data_login1={
            '__EVENTTARGET': hidden_fields.get('__EVENTTARGET', ''),
            '__EVENTARGUMENT': hidden_fields.get('__EVENTARGUMENT', ''),
            '__VIEWSTATE': hidden_fields.get('__VIEWSTATE', ''),
            '__VIEWSTATEGENERATOR': hidden_fields.get('__VIEWSTATEGENERATOR', ''),
            '__EVENTVALIDATION': hidden_fields.get('__EVENTVALIDATION', ''),
            'stuid':stuid,
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
            response = JsonResponse(response_login)
            response.set_cookie('sessionid', response_login['data']['sessionid'], httponly=True, secure=True)
        else:
            response_login['status'] = 'False'
            response_login['data'] = {}
            response_login['data']['logintxt'] = smessage.text
            response = JsonResponse(response_login)


        return response


    else:
        return HttpResponse('.....')

@csrf_exempt
def look1(request):
    from .models import User,Round,Cycle,MarketReport,Datakeep
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)

    uid = request.session.get('uid')
    round_reports = Round.objects.filter(uid=uid).annotate(round_id_int=Cast('round_id', IntegerField())).order_by('-round_id_int').first()
    cycle_reports_now = Cycle.objects.filter(round_id=round_reports.round_id).annotate(cycle_id_int=Cast('cycle_id', IntegerField())).order_by('-cycle_id_int').first()
    cycle_reports_1 = Cycle.objects.filter(round_id=round_reports.round_id).annotate(cycle_id_int=Cast('cycle_id', IntegerField())).order_by('cycle_id_int').first()
    market_reports_now = MarketReport.objects.filter(cycle_id=cycle_reports_now.cycle_id).order_by('cycle_id')
    market_reports_1 = MarketReport.objects.filter(cycle_id=cycle_reports_1.cycle_id).order_by('cycle_id')
    if len(market_reports_1) :
        # 数据存在，格式化并返回
        if market_reports_now.last().cycle_id.cycle_id[-1] == '1':
            response_look1 = {}
            for report in market_reports_now:
                response_looknow = {
                    '标题': f'第1周期（创业周期）市场形势报告',
                    '市场容量': report.market_capacity,
                    '原材料': report.raw_materials,
                    '附件': report.attachments,
                    '人员费用': report.personnel_costs,
                    '批量招标': report.bulk_tendering,
                    '批量订购': report.bulk_ordering,
                    '订购价格': report.ordering_price,
                }
                response_look1[response_looknow['标题']] = response_looknow
                break
        else:
            uid = request.session.get('uid')
            user_instance = User.objects.get(uid=uid)
            response_look1="response_look1"
            response_look1 = Datakeep.get_field_data(user_instance,response_look1)
        return JsonResponse(response_look1)

    else:
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
            response = session.get(url=url_look1_switchover)
            soup = BeautifulSoup(response.text, 'html.parser')
            hidden_fields = extract_hidden_fields(soup)
            data_look1_switchover={
                '__VIEWSTATE': hidden_fields.get('__VIEWSTATE', ''),
                '__VIEWSTATEGENERATOR': hidden_fields.get('__VIEWSTATEGENERATOR', ''),
                '__EVENTVALIDATION': hidden_fields.get('__EVENTVALIDATION', ''),
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
        # 将数据存入数据库

        for title, data in response_look1.items():
            # 创建 MarketReport 实例
            MarketReport.objects.create(
                cycle_id=cycle_reports_1,
                market_capacity=data.get('市场容量', ''),
                raw_materials=data.get('原材料', ''),
                attachments=data.get('附件', ''),
                personnel_costs=data.get('人员费用', ''),
                bulk_tendering=data.get('批量招标', ''),
                bulk_ordering=data.get('批量订购', ''),
                ordering_price=data.get('订购价格', ''),
            )
            break

        return JsonResponse(response_look1)



@csrf_exempt
def lookhistory(request):
    from .models import User,Round,Cycle,MarketHistoryReport,Datakeep
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)
    uid = request.session.get('uid')
    round_reports = Round.objects.filter(uid=uid).annotate(round_id_int=Cast('round_id', IntegerField())).order_by('-round_id_int').first()
    cycle_reports_now = Cycle.objects.filter(round_id=round_reports.round_id).annotate(cycle_id_int=Cast('cycle_id', IntegerField())).order_by('-cycle_id_int').first()
    cycle_reports_1 = Cycle.objects.filter(round_id=round_reports.round_id).annotate(cycle_id_int=Cast('cycle_id', IntegerField())).order_by('cycle_id_int').first()
    MarketHistoryReport_now =MarketHistoryReport.objects.filter(cycle_id=cycle_reports_now.cycle_id).order_by('cycle_id')
    MarketHistoryReport_1 = MarketHistoryReport.objects.filter(cycle_id=cycle_reports_1.cycle_id).order_by('cycle_id')
 
    if len(MarketHistoryReport_1) :
        if MarketHistoryReport_now.last().cycle_id.cycle_id[-1] == '1':
            # 数据存在，格式化并返回
            response_lookhistory = {
                '标题': '历史平均材料价格、工资水平及创业注册资金数据',
                '订购批量_批量范围': [
                    '0-25000',
                    '25001-45000',
                    '45001-70000',
                    '70001-'
                ],
                '订购批量_原材料单价（元）': [
                    MarketHistoryReport_now.zero_to_25000_mater,
                    MarketHistoryReport_now.two_fifty_one_to_45000_mater,
                    MarketHistoryReport_now.four_fifty_one_to_70000_mater,
                    MarketHistoryReport_now.seven_zero_zero_one_mater
                ],
                '订购批量_附件单价（元）': [
                    MarketHistoryReport_now.zero_to_25000_att,
                    MarketHistoryReport_now.two_fifty_one_to_45000_att,
                    MarketHistoryReport_now.four_fifty_one_to_70000_att,
                    MarketHistoryReport_now.seven_zero_zero_one_att
                ],
                '部门': [
                    '管理部门',
                    '销售部门',
                    '采购部门',
                    '生产部门',
                    '研究部门'
                ],
                '年薪（万元）': [
                    MarketHistoryReport_now.management,
                    MarketHistoryReport_now.sales,
                    MarketHistoryReport_now.purchase,
                    MarketHistoryReport_now.prd,
                    MarketHistoryReport_now.rnd
                ],
                '资金类型': [
                    '注册资金',
                    '资金储备',
                    '长期贷款',
                    '资金合计'
                ],
                '数额（万元）': [
                    MarketHistoryReport_now.register,
                    MarketHistoryReport_now.reserve,
                    MarketHistoryReport_now.loan,
                    MarketHistoryReport_now.total
                ]
            }
            return JsonResponse(response_lookhistory)
        else:
            uid = request.session.get('uid')
            user_instance = User.objects.get(uid=uid)
            response_lookhistory="response_lookhistory"
            response_lookhistory = Datakeep.get_field_data(user_instance,response_lookhistory)

            return JsonResponse(response_lookhistory)

    else:
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

        MarketHistoryReport.objects.create(
            cycle_id=cycle_reports_1,
            zero_to_25000_mater=response_lookhistory['订购批量_原材料单价（元）'][0],
            zero_to_25000_att=response_lookhistory['订购批量_附件单价（元）'][0],
            two_fifty_one_to_45000_mater=response_lookhistory['订购批量_原材料单价（元）'][1],
            two_fifty_one_to_45000_att=response_lookhistory['订购批量_附件单价（元）'][1],
            four_fifty_one_to_70000_mater=response_lookhistory['订购批量_原材料单价（元）'][2],
            four_fifty_one_to_70000_att=response_lookhistory['订购批量_附件单价（元）'][2],
            seven_zero_zero_one_mater=response_lookhistory['订购批量_原材料单价（元）'][3],
            seven_zero_zero_one_att=response_lookhistory['订购批量_附件单价（元）'][3],
            management=response_lookhistory['年薪（万元）'][0],
            sales=response_lookhistory['年薪（万元）'][1],
            purchase=response_lookhistory['年薪（万元）'][2],
            prd=response_lookhistory['年薪（万元）'][3],
            rnd=response_lookhistory['年薪（万元）'][4],
            register=response_lookhistory['数额（万元）'][0],
            reserve=response_lookhistory['数额（万元）'][1],
            loan=response_lookhistory['数额（万元）'][2],
            total=response_lookhistory['数额（万元）'][3],
        )
    return JsonResponse(response_lookhistory)



@csrf_exempt
def commit_decision(request):
    from .models import User,Round,Cycle,MarketReport,MarketHistoryReport,CompetitionResult,Evaluation,Round,Datakeep,DecisionForm,CompanyReportCostType,CompanyReportCostUnit,CompanyReportProfitLoss,CompanyReportPostTaxProfit,CompanyReportProfitDistribution,CompanyReportFinancial,CompanyReportBalance,CompanyReportCostDpt,CompanyReportMarketPrd,CompanyReportMarket,CompanyReportWarehouse1,CompanyReportWarehouse2,CompanyReportWarehouse3,CompanyReportPersonnel1,CompanyReportPersonnel2,CompanyReportPrd1,CompanyReportPrd2,CompanyReportPrd3
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
        response_look1={}
        tree=etree.HTML(response_submit3.text)

        element1 = tree.xpath('//font[@color="#024802"]/text()')

        cycle_num=int(element1[0][2])+1
        response_submit_decision_data["提交后周期"]=cycle_num


        #获取用户·轮次和周期实例，用于下面创建数据库实例
        uid = request.session.get('uid')
        user_reports = User.objects.get(uid=uid)
        round_reports = Round.objects.filter(uid=uid).annotate(round_id_int=Cast('round_id', IntegerField())).order_by('-round_id_int').first()
        cycle_reports = Cycle.objects.filter(round_id=round_reports.round_id).annotate(cycle_id_int=Cast('cycle_id', IntegerField())).order_by('-cycle_id_int').first()
        
        #插入新的周期数据
        newcycle=Cycle.update_and_insert_cycle(cycle_reports,user_reports,round_reports,cycle_num)
       
        # 1.1
        # 1.1
        # 1.1
        # 1.1
        # 1.1
        #爬取并存入response_look1      
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
            response11=session.post(url=url_look1_switchover,data=data_look1_switchover)
            # 解析HTML内容
            tree1=etree.HTML(response11.text)
            # 使用XPath定位元素
            # 例如，定位一个包含特定文本的元素
            element1 = tree1.xpath('//font[translate(@color, "F", "f")="#ffffff" and @style="font-size:18px"]/text()')
            element2 = tree1.xpath('//font[@color="#000000" and @style="font-size:18px"]/text()')
            element3 = tree1.xpath('//font[@class="title"]/text()')
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
        # 将数据存入数据库
        num=0
        for title, data in response_look1.items():
            num+=1
            if num==cycle_num:
                # 创建 MarketReport 实例
                MarketReport.objects.create(
                    cycle_id=newcycle,
                    market_capacity=data.get('市场容量', ''),
                    raw_materials=data.get('原材料', ''),
                    attachments=data.get('附件', ''),
                    personnel_costs=data.get('人员费用', ''),
                    bulk_tendering=data.get('批量招标', ''),
                    bulk_ordering=data.get('批量订购', ''),
                    ordering_price=data.get('订购价格', ''),
                )
                break
                       
        # 1.2
        # 1.2
        # 1.2
        # 1.2
        # 1.2
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

        MarketHistoryReport.objects.create(
            cycle_id=newcycle,
            zero_to_25000_mater=response_lookhistory['订购批量_原材料单价（元）'][0],
            zero_to_25000_att=response_lookhistory['订购批量_附件单价（元）'][0],
            two_fifty_one_to_45000_mater=response_lookhistory['订购批量_原材料单价（元）'][1],
            two_fifty_one_to_45000_att=response_lookhistory['订购批量_附件单价（元）'][1],
            four_fifty_one_to_70000_mater=response_lookhistory['订购批量_原材料单价（元）'][2],
            four_fifty_one_to_70000_att=response_lookhistory['订购批量_附件单价（元）'][2],
            seven_zero_zero_one_mater=response_lookhistory['订购批量_原材料单价（元）'][3],
            seven_zero_zero_one_att=response_lookhistory['订购批量_附件单价（元）'][3],
            management=response_lookhistory['年薪（万元）'][0],
            sales=response_lookhistory['年薪（万元）'][1],
            purchase=response_lookhistory['年薪（万元）'][2],
            prd=response_lookhistory['年薪（万元）'][3],
            rnd=response_lookhistory['年薪（万元）'][4],
            register=response_lookhistory['数额（万元）'][0],
            reserve=response_lookhistory['数额（万元）'][1],
            loan=response_lookhistory['数额（万元）'][2],
            total=response_lookhistory['数额（万元）'][3],
        )

        # 2
        # 2
        # 2
        # 2
        # 2
        #爬取目标网站
        url='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/adddata/dataadd.aspx'


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


        # 插入数据库
        num=1
        for period, decision_data in response_historical_decision.items():
            num+=1
            if num==cycle_num:
                decision_form = DecisionForm.objects.create(
                    cycle_id=cycle_reports,
                    market_price=decision_data.get('一般市场价格', ''),
                    ad_expense=decision_data.get('广告费用投入', ''),
                    sales_count=decision_data.get('销售人员个数', ''),
                    research_report=decision_data.get('市场和生产研究报告', ''),
                    bid_price=decision_data.get('附一：投标价格', ''),
                    special_products_count=decision_data.get('附二：特殊产品数', ''),
                    raw_materials_qty=decision_data.get('购买原材料量', ''),
                    attachments_qty=decision_data.get('购买附件量', ''),
                    research_personnel_recruited=decision_data.get('科研人员招收数', ''),
                    research_personnel_terminated=decision_data.get('科研人员辞退数', ''),
                    improvement_cost=decision_data.get('产品改进费用', ''),
                    market_plan_qty=decision_data.get('一般市场产品计划量', ''),
                    production_line_investment=decision_data.get('生产线投资数', ''),
                    production_line_sales=decision_data.get('生产线变卖数', ''),
                    maintenance_cost=decision_data.get('维修保养费用', ''),
                    production_investment=decision_data.get('生产合理化投资', ''),
                    production_personnel_recruited=decision_data.get('生产人员招收数', ''),
                    production_personnel_terminated=decision_data.get('生产人员辞退数', ''),
                    robots_purchased=decision_data.get('购买机器人', ''),
                    welfare_expense=decision_data.get('社会福利费用', ''),
                    medium_loan=decision_data.get('中期贷款', ''),
                    securities_purchase=decision_data.get('购买有价证券', ''),
                    dividend_payment=decision_data.get('计划支付股息', ''),
                    management_investment=decision_data.get('管理合理化投资', '')
                )
                break   

        # 4
        # 4
        # 4
        # 4
        # 4
        #爬取并存入compete_outcome
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

        # 创建并保存竞争结果数据
        competition_result = CompetitionResult.objects.create(
            cycle_id=cycle_reports,
            competition_title=compete_outcome['标题'],
            company_market_price=compete_outcome.get('一般市场价格', [None, None])[0],
            competitor_market_price=compete_outcome.get('一般市场价格', [None, None])[1],
            company_ad_expenses=compete_outcome.get('广告费用投入', [None, None])[0],
            competitor_ad_expenses=compete_outcome.get('广告费用投入', [None, None])[1],
            company_sales_staff=compete_outcome.get('销售人员数量', [None, None])[0],
            competitor_sales_staff=compete_outcome.get('销售人员数量', [None, None])[1],
            company_quality_rating=compete_outcome.get('产品质量评价', [None, None])[0],
            competitor_quality_rating=compete_outcome.get('产品质量评价', [None, None])[1],
            company_market_sales_volume=compete_outcome.get('一般市场销售量', [None, None])[0],
            competitor_market_sales_volume=compete_outcome.get('一般市场销售量', [None, None])[1],
            company_market_sales_revenue=compete_outcome.get('一般市场销售额', [None, None])[0],
            competitor_market_sales_revenue=compete_outcome.get('一般市场销售额', [None, None])[1],
            company_theoretical_share=compete_outcome.get('理论市场占有率', [None, None])[0],
            competitor_theoretical_share=compete_outcome.get('理论市场占有率', [None, None])[1],
            company_actual_share=compete_outcome.get('实际市场占有率', [None, None])[0],
            competitor_actual_share=compete_outcome.get('实际市场占有率', [None, None])[1],
            company_extra1_sales_volume=compete_outcome.get('附加市场I销售量', [None, None])[0],
            competitor_extra1_sales_volume=compete_outcome.get('附加市场I销售量', [None, None])[1],
            company_extra1_sales_revenue=compete_outcome.get('附加市场I销售额', [None, None])[0],
            competitor_extra1_sales_revenue=compete_outcome.get('附加市场I销售额', [None, None])[1],
            company_extra2_sales_volume=compete_outcome.get('附加市场II销售量', [None, None])[0],
            competitor_extra2_sales_volume=compete_outcome.get('附加市场II销售量', [None, None])[1],
            company_extra2_sales_revenue=compete_outcome.get('附加市场II销售额', [None, None])[0],
            competitor_extra2_sales_revenue=compete_outcome.get('附加市场II销售额', [None, None])[1],
            company_winning_company=compete_outcome.get('中标企业', [None, None])[0],
            competitor_winning_company=compete_outcome.get('中标企业', [None, None])[1],
            company_bid_price=compete_outcome.get('中标企业投标价格', [None, None])[0],
            competitor_bid_price=compete_outcome.get('中标企业投标价格', [None, None])[1],
            company_inventory=compete_outcome.get('产品累积库存数量', [None, None])[0],
            competitor_inventory=compete_outcome.get('产品累积库存数量', [None, None])[1],
            company_capacity=compete_outcome.get('生产线生产能力', [None, None])[0],
            competitor_capacity=compete_outcome.get('生产线生产能力', [None, None])[1],
            company_profit=compete_outcome.get('税前经营成果', [None, None])[0],
            competitor_profit=compete_outcome.get('税前经营成果', [None, None])[1],
            company_assets_liabilities=compete_outcome.get('资产负债总和', [None, None])[0],
            competitor_assets_liabilities=compete_outcome.get('资产负债总和', [None, None])[1]
        )

        # 5
        # 5
        # 5
        # 5
        # 5
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

        reporthaved_state=0 #是否有报告，0为没有，1为有

        for dictl,urll,text in report_data:
            #当前周期的报告处理
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
            cleaned_element1 = [text.replace('\xa0', '') for text in element1]   #数据 如：['1150', '0', '840', '19873', '0']
            cleaned_element2 = [text.replace('\xa0', '') for text in element2]   #周期数 如：['（第4周期）']
            cleaned_element3 = [text.replace('\xa0', '') for text in element3]   #报告名称 如：['市场生产数据报告']
            cleaned_element1 = [item.strip() for item in cleaned_element1 
                if (re.search(r'\d', item) or item == "---"or item == " ---"or item == " -"or item == "***") 
                and item not in ["生产线负载率100%时生产能力", "(0--1)","(1--5)"]] #数据（再次清洗后） 如：['1150', '0', '840', '19873', '0']

            #判断当前周期是否有报告
            if  cleaned_element3:
                if len(cleaned_element2[0])>8:
                    cleaned_element2[0]=cleaned_element2[0][0]+cleaned_element2[0][6:]  
                dict_data[cleaned_element3[0]+cleaned_element2[0]]=cleaned_element1
                n=cleaned_element2[0][-4]
                reporthaved_state=1
            else:
                if text=='各企业市场营销及生产研究报告' and reporthaved_state==1:
                    dict_data['各企业市场营销及生产研究报告（第'+n+'周期）']='本周期没有订购市场和生产研究报告！'

            cyclenumi=int(n)-1 #记录循环的周期数
            if reporthaved_state==1:
                #历史周期的报告处理
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
                    cleaned_element1 = [text.replace('\xa0', '') for text in element1]   #数据 如：['1150', '0', '840', '19873', '0']
                    cleaned_element2 = [text.replace('\xa0', '') for text in element2]   #周期数 如：['（第4周期）']
                    cleaned_element3 = [text.replace('\xa0', '') for text in element3]   #报告名称 如：['市场生产数据报告']
                    cleaned_element1 = [item.strip() for item in cleaned_element1 
                    if (re.search(r'\d', item) or item == "---"or item == " ---"or item == " -"or item == "***") 
                    and item not in ["生产线负载率100%时生产能力", "(0--1)","(1--5)"]]     #数据（再次清洗后） 如：['1150', '0', '840', '19873', '0']
                    
                    if cleaned_element3:
                        if len(cleaned_element2[0])>8:    #第一周期的各企业市场营销及生产研究报告标题长度大于8，需要截取
                            cleaned_element2[0]=cleaned_element2[0][0]+cleaned_element2[0][6:] 
                        dict_data[cleaned_element3[0]+cleaned_element2[0]]=cleaned_element1
                    else:
                        dict_data['各企业市场营销及生产研究报告（第'+str(cyclenumi)+'周期）']='本周期没有订购市场和生产研究报告！'
                    cyclenumi-=1
            # 将字典项转换为列表并倒序
            reversed_items = list(dict_data.items())[::-1]
            # 将倒序后的列表转换回字典
            dict_data= dict(reversed_items)
                
            if len(dict_data)<7:
                for i in range(len(dict_data),7):
                    dict_data[text+'（第'+str(i+1)+'周期）']='无'
            response_enterreporting[text]=dict_data

        cycle_key = f"第{cycle_num-1}周期"
        CompanyReportCostTypedate = response_enterreporting.get("产品成本类型核算报告", {}).get(f"产品成本类型核算报告（{cycle_key}）", [])
        CompanyReportCostUnitdate = response_enterreporting.get("成本承担单元核算报告", {}).get(f"成本承担单元核算报告（{cycle_key}）", [])
        CompanyReportProfitLossdate = response_enterreporting.get("利润和亏损核算报告", {}).get(f"利润和亏损核算报告（{cycle_key}）", [])
        CompanyReportPostTaxProfitdate = response_enterreporting.get("税后利润核算报告", {}).get(f"税后利润核算报告（{cycle_key}）", [])
        CompanyReportProfitDistributiondate = response_enterreporting.get("利润分配核算报告", {}).get(f"利润分配核算报告（{cycle_key}）", [])
        CompanyReportFinancialdate = response_enterreporting.get("财务报告", {}).get(f"财务报告（{cycle_key}）", [])
        CompanyReportBalanceSheetdate = response_enterreporting.get("资产负债表", {}).get(f"资产负债表（{cycle_key}）", [])
        CompanyReportCostDptdate = response_enterreporting.get("成本发生部门核算报告", {}).get(f"成本发生部门核算报告（{cycle_key}）", [])
        CompanyReportMarketPrddate = response_enterreporting.get("市场生产数据报告", {}).get(f"市场生产数据报告（{cycle_key}）", [])
        CompanyReportMarketResearchdate = response_enterreporting.get("各企业市场营销及生产研究报告", {}).get(f"各企业市场营销及生产研究报告（{cycle_key}）", [])
        # 如果数据存在且不为 "无"
        if CompanyReportMarketPrddate != "无" and CompanyReportMarketPrddate:
            # 创建并保存市场报告数据
            company_report_Market = CompanyReportMarket.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                general_price=CompanyReportMarketPrddate[0],  # 一般市场价格
                att_1_price=CompanyReportMarketPrddate[1],  # 附加市场1价格
                att_2_price=CompanyReportMarketPrddate[2],  # 附加市场2价格s
                general_sales_volume=CompanyReportMarketPrddate[3],  # 一般市场销售量
                att_1_sales_volume=CompanyReportMarketPrddate[4],  # 附加市场1销售量
                att_2_sales_volume=CompanyReportMarketPrddate[5],  # 附加市场2销售量
                general_sales_revenue=CompanyReportMarketPrddate[6],  # 一般市场销售额
                att_1_sales_revenue=CompanyReportMarketPrddate[7],  # 附加市场1销售额
                att_2_sales_revenue=CompanyReportMarketPrddate[8],  # 附加市场2销售额
                share=CompanyReportMarketPrddate[9],  # 市场占有率%
                rate=CompanyReportMarketPrddate[10],  # 产品质量评价
            )
            company_report_Market.save()  # 保存报告数据

            # 创建并保存仓库报告1：原材料数据
            company_report_warehouse1 = CompanyReportWarehouse1.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                beginning_inventory_qty=CompanyReportMarketPrddate[11],  # 期初库存量，
                beginning_inventory_value=CompanyReportMarketPrddate[12],  # 期初库存价值
                beginning_inventory_total=CompanyReportMarketPrddate[13],  # 期初库存总价值
                increase_qty=CompanyReportMarketPrddate[14],  # 增加量
                increase_value=CompanyReportMarketPrddate[15],  # 增加值
                increase_total=CompanyReportMarketPrddate[16],  # 增加总值
                consumed_qty=CompanyReportMarketPrddate[17],  # 消耗量
                consumed_value=CompanyReportMarketPrddate[18],  # 消耗值
                consumed_total=CompanyReportMarketPrddate[19],  # 消耗总值
                final_inventory_qty=CompanyReportMarketPrddate[20],  # 期末库存量
                final_inventory_value=CompanyReportMarketPrddate[21],  # 期末库存价值
                final_inventory_total=CompanyReportMarketPrddate[22],  # 期末库存总值
            )
            company_report_warehouse1.save()  # 保存报告数据 

            # 创建并保存仓库报告2：一般产品数据
            company_report_warehouse2 = CompanyReportWarehouse2.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                beginning_inventory_qty=CompanyReportMarketPrddate[23],  # 期初库存量，从第23位开始
                beginning_inventory_cost=CompanyReportMarketPrddate[24],  # 期初制造成本
                beginning_inventory_value=CompanyReportMarketPrddate[25],  # 期初库存价值
                increase_qty=CompanyReportMarketPrddate[26],  # 增加量
                increase_cost=CompanyReportMarketPrddate[27],  # 增加成本
                increase_value=CompanyReportMarketPrddate[28],  # 增加值
                consumed_qty=CompanyReportMarketPrddate[29],  # 消耗量
                consumed_cost=CompanyReportMarketPrddate[30],  # 消耗成本
                consumed_value=CompanyReportMarketPrddate[31],  # 消耗值
                final_inventory_qty=CompanyReportMarketPrddate[32],  # 期末库存量
                final_inventory_cost=CompanyReportMarketPrddate[33],  # 期末库存成本
                final_inventory_value=CompanyReportMarketPrddate[34],  # 期末库存价值
            )
            company_report_warehouse2.save()  # 保存报告数据
            # 创建并保存仓库报告3：附件数据
            company_report_warehouse3 = CompanyReportWarehouse3.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                beginning_inventory_qty=CompanyReportMarketPrddate[35],  # 期初库存量，从第35位开始
                beginning_inventory_value=CompanyReportMarketPrddate[36],  # 期初库存价值
                beginning_inventory_total=CompanyReportMarketPrddate[37],  # 期初库存总价值
                increase_qty=CompanyReportMarketPrddate[38],  # 增加量
                increase_value=CompanyReportMarketPrddate[39],  # 增加值
                increase_total=CompanyReportMarketPrddate[40],  # 增加总值
                consumed_qty=CompanyReportMarketPrddate[41],  # 消耗量
                consumed_value=CompanyReportMarketPrddate[42],  # 消耗值
                consumed_total=CompanyReportMarketPrddate[43],  # 消耗总值
                final_inventory_qty=CompanyReportMarketPrddate[44],  # 期末库存量
                final_inventory_value=CompanyReportMarketPrddate[45],  # 期末库存价值
                final_inventory_total=CompanyReportMarketPrddate[46],  # 期末库存总值
            )
            company_report_warehouse3.save()  # 保存报告数据

            # 创建并保存人员报告1的数据
            company_report_personnel1 = CompanyReportPersonnel1.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                beginning_personnel_prd=CompanyReportMarketPrddate[47],  # 生产部门期初人员，从第47位开始
                beginning_personnel_rnd=CompanyReportMarketPrddate[48],  # 研究开发部门期初人员
                recruitment_prd=CompanyReportMarketPrddate[49],  # 生产部门招聘人数
                recruitment_rnd=CompanyReportMarketPrddate[50],  # 研究开发部门招聘人数
                fire_prd=CompanyReportMarketPrddate[51],  # 生产部门辞退人数
                fire_rnd=CompanyReportMarketPrddate[52],  # 研究开发部门辞退人数
                flow_prd=CompanyReportMarketPrddate[53],  # 生产部门流动人数
                flow_rnd=CompanyReportMarketPrddate[54],  # 研究开发部门流动人数
                final_personnel_prd=CompanyReportMarketPrddate[55],  # 生产部门期末人员
                final_personnel_rnd=CompanyReportMarketPrddate[56],  # 研究开发部门期末人员
            )
            company_report_personnel1.save()  # 保存报告数据

            # 创建并保存人员报告2的数据
            company_report_personnel2 = CompanyReportPersonnel2.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                sales=CompanyReportMarketPrddate[57],  # 销售部门人员数
                purchase=CompanyReportMarketPrddate[58],  # 采购部门人员数
                management=CompanyReportMarketPrddate[59],  # 管理部门人员数
                coefficient=CompanyReportMarketPrddate[60],  # 管理的合理化系数
            )
            company_report_personnel2.save()  # 保存报告数据

            # 创建并保存生产报告1的数据
            company_report_prd1 = CompanyReportPrd1.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                prev_line=CompanyReportMarketPrddate[61],  # 前周期生产线
                prev_robot=CompanyReportMarketPrddate[62],  # 前周期机器人
                invest_line=CompanyReportMarketPrddate[63],  # 投资生产线
                invest_robot=CompanyReportMarketPrddate[64],  # 投资机器人
                sell_line=CompanyReportMarketPrddate[65],  # 变卖生产线
                sell_robot=CompanyReportMarketPrddate[66],  # 变卖机器人
                curr_line=CompanyReportMarketPrddate[67],  # 本周期生产线
                curr_robot=CompanyReportMarketPrddate[68],  # 本周期机器人
            )
            company_report_prd1.save()  # 保存报告数据

            # 创建并保存生产报告2的数据
            company_report_prd2 = CompanyReportPrd2.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                general_process=CompanyReportMarketPrddate[69],  # 一般产品加工台数
                general_facility=CompanyReportMarketPrddate[70],  # 一般产品设备要求数
                general_personnel=CompanyReportMarketPrddate[71],  # 一般产品人员要求数
                sp_process=CompanyReportMarketPrddate[72],  # 特殊产品加工台数
                sp_facility=CompanyReportMarketPrddate[73],  # 特殊产品设备要求数
                sp_personnel=CompanyReportMarketPrddate[74],  # 特殊产品人员要求数
                total_process=CompanyReportMarketPrddate[75],  # 总产品加工台数
                total_facility=CompanyReportMarketPrddate[76],  # 总产品设备要求数
                total_personnel=CompanyReportMarketPrddate[77],  # 总产品人员要求数
                load_process=CompanyReportMarketPrddate[78],  # 加工台数负载率%
                load_facility=CompanyReportMarketPrddate[79],  # 设备要求数负载率%
                load_personnel=CompanyReportMarketPrddate[80],  # 人员要求数负载率%
            )
            company_report_prd2.save()  # 保存报告数据

            # 创建并保存生产报告3的数据
            company_report_prd3 = CompanyReportPrd3.objects.create(
                cycle_id=cycle_reports,  # 关联周期
                rational=CompanyReportMarketPrddate[81],  # 生产线合理化系数
                maintain=CompanyReportMarketPrddate[82],  # 生产线维修保养系数
                load_100=CompanyReportMarketPrddate[83],  # 生产线负载率100%时生产能力
            )
            company_report_prd3.save()  # 保存报告数据
        
        # 如果产品成本类型核算报告存在，保存数据
        if CompanyReportCostTypedate != "无":
            company_report_Costtype=CompanyReportCostType.objects.create(
                cycle_id=cycle_reports,
                raw_material=CompanyReportCostTypedate[0],  # 原材料
                attachment=CompanyReportCostTypedate[1],  # 附件
                prd_material=CompanyReportCostTypedate[2],  # 生产材料
                salary=CompanyReportCostTypedate[3],  # 工资费用
                salary_direct=CompanyReportCostTypedate[4],  # 直接工资费用
                personnel=CompanyReportCostTypedate[5],  # 人员附加费用
                personnel_direct=CompanyReportCostTypedate[6],  # 直接人员附加费用
                hirefire=CompanyReportCostTypedate[7],  # 招聘/解雇费用
                plant=CompanyReportCostTypedate[8],  # 厂房
                line=CompanyReportCostTypedate[9],  # 生产线
                robot=CompanyReportCostTypedate[10],  # 机器人
                other_fixed=CompanyReportCostTypedate[11],  # 其他固定费用
                maintain=CompanyReportCostTypedate[12],  # 维修费用
                rationalization=CompanyReportCostTypedate[13],  # 合理化
                repair=CompanyReportCostTypedate[14],  # 返修/废品
                inventory=CompanyReportCostTypedate[15],  # 库存费用
                ad=CompanyReportCostTypedate[16],  # 广告费用
                market_research=CompanyReportCostTypedate[17],  # 市场研究
                other_rnd=CompanyReportCostTypedate[18],  # 其它研究开发费用
                total=CompanyReportCostTypedate[19],  # 总费用
            )                
            company_report_Costtype.save()
        
        # 如果成本承担单元核算报告存在，保存数据
        if CompanyReportCostUnitdate != "无":
            cost_units=["原材料","附件","生产材料","材料直接费用","材料间接费用","材料成本","加工直接费用","加工间接费用","加工成本","制造成本","研究开发费用","销售费用","管理费用","产品成本","销售收入","产品库存变化","总的经营收入","生产经营成果"]
            for index,cost_unit in enumerate(cost_units):
                company_report_CostUnit = CompanyReportCostUnit.objects.create(
                    cycle_id=cycle_reports,
                    cost_unit=cost_unit,  # 成本承担单元名称
                    general_market=CompanyReportCostUnitdate[index*4:(index+1)*4][1],  # 一般市场
                    attach_market_1=CompanyReportCostUnitdate[index*4:(index+1)*4][2],  # 附加市场Ⅰ
                    attach_market_2=CompanyReportCostUnitdate[index*4:(index+1)*4][3],  # 附加市场Ⅱ
                    total=CompanyReportCostUnitdate[index*4:(index+1)*4][0],  # 合计
                )
                company_report_CostUnit.save()

        # 如果利润和亏损核算报告存在，保存数据
        if CompanyReportProfitLossdate != "无":
            company_report_ProfitLoss = CompanyReportProfitLoss.objects.create(
                cycle_id=cycle_reports,
                revenue=CompanyReportProfitLossdate[0],  # 销售收入
                inventory_change=CompanyReportProfitLossdate[2],  # 产品库存变化
                production=CompanyReportProfitLossdate[3],  # 销售产品制造成本
                material=CompanyReportProfitLossdate[4],  # 材料费用
                sales=CompanyReportProfitLossdate[5],  # 销售费用
                salary=CompanyReportProfitLossdate[6],  # 工资
                personnel_att=CompanyReportProfitLossdate[7],  # 人员附加费用
                r_and_d=CompanyReportProfitLossdate[8],  # 研究开发费用
                other_personnel=CompanyReportProfitLossdate[9],  # 其他人员费用
                depreciation=CompanyReportProfitLossdate[10],  # 折旧
                management=CompanyReportProfitLossdate[11],  # 管理费用
                other_operating=CompanyReportProfitLossdate[12],  # 其他经营费用
                operating_profit=CompanyReportProfitLossdate[13],  # 生产经营成果
            )
            company_report_ProfitLoss.save()

        # 如果税后利润核算报告存在，保存数据
        if CompanyReportPostTaxProfitdate != "无":
            company_report_PostTaxProfit = CompanyReportPostTaxProfit.objects.create(
                cycle_id=cycle_reports,
                operating_profit=CompanyReportPostTaxProfitdate[0],  # 生产经营成果
                securities_income=CompanyReportPostTaxProfitdate[1],  # 有价证券收入
                interest=CompanyReportPostTaxProfitdate[2],  # 利息费用和其他费用
                general_profit=CompanyReportPostTaxProfitdate[3],  # 一般经营成果
                sp_income=CompanyReportPostTaxProfitdate[4],  # 特别收入
                sp_expense=CompanyReportPostTaxProfitdate[5],  # 特别费用
                pre_tax_profit=CompanyReportPostTaxProfitdate[6],  # 税前利润
                tax=CompanyReportPostTaxProfitdate[7],  # 税收
                netprofit=CompanyReportPostTaxProfitdate[8],  # 周期结余/周期亏损
            )
            company_report_PostTaxProfit.save()

        # 如果利润分配核算报告存在，保存数据
        if CompanyReportProfitDistributiondate != "无":
            company_report_ProfitDistribution = CompanyReportProfitDistribution.objects.create(
                cycle_id=cycle_reports,
                period_profit=CompanyReportProfitDistributiondate[0],  # 周期结余/周期亏损
                previous_loss=CompanyReportProfitDistributiondate[1],  # 前周期亏损结转
                current_profit=CompanyReportProfitDistributiondate[2],  # 本周期利润储备
                capital_balance_profit=CompanyReportProfitDistributiondate[3],  # 资金平衡利润/资金平衡亏损
                dividend=CompanyReportProfitDistributiondate[4],  # 股息
                final_loss=CompanyReportProfitDistributiondate[5],  # 本周期亏损结转
            )
            company_report_ProfitDistribution.save()

        # 如果财务报告存在，保存数据
        if CompanyReportFinancialdate != "无":
            company_report_Financial = CompanyReportFinancial.objects.create(
                cycle_id=cycle_reports,
                beginning_cash=CompanyReportFinancialdate[0],  # 期初现金
                current_sales=CompanyReportFinancialdate[1],  # 本周期产品销售收入
                material=CompanyReportFinancialdate[2],  # 材料费用
                previous_sales=CompanyReportFinancialdate[3],  # 前周期产品销售收入
                labor=CompanyReportFinancialdate[4],  # 人员费用
                other_operating=CompanyReportFinancialdate[5],  # 其他经营费用
                security_income=CompanyReportFinancialdate[6],  # 有价证券收入
                loan_repay=CompanyReportFinancialdate[7],  # 中期和透支贷款归还
                interest_income=CompanyReportFinancialdate[8],  # 利息收入
                interest_expense=CompanyReportFinancialdate[9],  # 利息费用
                robots=CompanyReportFinancialdate[10],  # 购买机器人
                special_income=CompanyReportFinancialdate[11],  # 特殊收入
                line_purchase=CompanyReportFinancialdate[12],  # 购买生产线和厂房
                line_sales=CompanyReportFinancialdate[13],  # 生产线变卖收入
                security_sales=CompanyReportFinancialdate[14],  # 购买有价证券
                tax=CompanyReportFinancialdate[15],  # 税收
                mid_loan=CompanyReportFinancialdate[16],  # 中期贷款
                dividend=CompanyReportFinancialdate[17],  # 股息支付(前周期)
                overdraft_loan=CompanyReportFinancialdate[18],  # 透支贷款
                special_expense=CompanyReportFinancialdate[19],  # 特别费用
                total_income=CompanyReportFinancialdate[20],  # 现金收入合计
                total_expense=CompanyReportFinancialdate[21],  # 现金支出合计
                ending_cash=CompanyReportFinancialdate[22],  # 期末现金
            )
            company_report_Financial.save()

        # 如果资产负债表存在，保存数据
        if CompanyReportBalanceSheetdate != "无":
            company_report_Balance = CompanyReportBalance.objects.create(
                cycle_id=cycle_reports,
                registered_capital=CompanyReportBalanceSheetdate[0],  # 注册资金
                estate=CompanyReportBalanceSheetdate[1],  # 地产和厂房
                capital_reserves=CompanyReportBalanceSheetdate[2],  # 资金储备
                facility=CompanyReportBalanceSheetdate[3],  # 设备和生产设施
                retained_earnings=CompanyReportBalanceSheetdate[4],  # 利润储备
                previous_loss=CompanyReportBalanceSheetdate[5],  # 前周期亏损结转
                current_trans=CompanyReportBalanceSheetdate[6],  # 周期结余/周期亏损
                material_att=CompanyReportBalanceSheetdate[7],  # 原材料与附件
                finished_product=CompanyReportBalanceSheetdate[8],  # 成品
                accounts_receivable=CompanyReportBalanceSheetdate[9],  # 债权
                long_loan=CompanyReportBalanceSheetdate[10],  # 长期贷款
                security=CompanyReportBalanceSheetdate[11],  # 有价证券
                mid_loan=CompanyReportBalanceSheetdate[12],  # 中期贷款
                cash=CompanyReportBalanceSheetdate[13],  # 现金
                short_loan=CompanyReportBalanceSheetdate[14],  # 透支贷款
                total_assets=CompanyReportBalanceSheetdate[15],  # 资产合计
                total_liabilities=CompanyReportBalanceSheetdate[16],  # 负债合计
        )
            
            company_report_Balance.save()

        # 如果成本发生部门核算报告存在，保存数据
        if CompanyReportCostDptdate != "无":
            dpts=["工资","人员附加费用","招聘/解雇","厂房","生产线","机器人","其他固定费用","维修保养","合理化","修理/废品","仓库费用","广告","市场研究","其他研发开发费用"]
            for index, dpt in enumerate(dpts):    
                company_report_CostDpt = CompanyReportCostDpt.objects.create(
                    cycle_id=cycle_reports,  # 将周期与其他数据关联
                    cost_dpt=dpt,  # 成本部门名称
                    total=CompanyReportCostDptdate[6*index:6*(index+1)][0],  # 合计
                    purchase=CompanyReportCostDptdate[6*index:6*(index+1)][1],  # 采购成本
                    prd=CompanyReportCostDptdate[6*index:6*(index+1)][2],  # 生产成本
                    rnd=CompanyReportCostDptdate[6*index:6*(index+1)][3],  # 研发成本
                    inventory=CompanyReportCostDptdate[6*index:6*(index+1)][4],  # 销售库存成本
                    management=CompanyReportCostDptdate[6*index:6*(index+1)][5],  # 管理成本
                )
                company_report_CostDpt.save()

        # 如果各企业市场营销及生产研究报告存在且有订购市场和生产研究报告
        if CompanyReportMarketResearchdate != "无" and CompanyReportMarketResearchdate!="本周期没有订购市场和生产研究报告！":
            # 创建并保存各企业市场营销及生产研究报告
            for i in range(0,2):
                company_report_MarketPrd = CompanyReportMarketPrd.objects.create(
                    cycle_id=cycle_reports,  # 关联周期
                    company_compute= "本企业" if i == 0 else "计算机",  # 本企业/计算机
                    market_price=CompanyReportMarketResearchdate[0+i],   # 一般市场价格
                    ad_expenses=CompanyReportMarketResearchdate[2+i],   # 广告费用投入
                    num_staff=CompanyReportMarketResearchdate[4+i],  # 销售人员数量
                    sales_staff=CompanyReportMarketResearchdate[6+i],  # 销售人员费用
                    product_rating=CompanyReportMarketResearchdate[8+i],  # 产品质量评价
                    product_expense=CompanyReportMarketResearchdate[10+i],  # 产品研究费用
                    market_sales_volume=CompanyReportMarketResearchdate[12+i],  # 一般市场销售量
                    market_sales_revenue=CompanyReportMarketResearchdate[14+i],  # 一般市场销售额
                    theoretical_share=CompanyReportMarketResearchdate[16+i],  # 理论市场占有率
                    actual_share=CompanyReportMarketResearchdate[18+i],  # 实际市场占有率
                    extra1_sales_volume=CompanyReportMarketResearchdate[20+i],  # 附加市场Ⅰ销售量
                    extra1_sales_revenue=CompanyReportMarketResearchdate[22+i],  # 附加市场Ⅰ销售额
                    extra2_sales_volume=CompanyReportMarketResearchdate[24+i],  # 附加市场Ⅱ销售量
                    extra2_sales_revenue=CompanyReportMarketResearchdate[26+i],  # 附加市场Ⅱ销售额
                    winning_company=CompanyReportMarketResearchdate[28+i],  # 中标企业
                    bid_price=CompanyReportMarketResearchdate[30+i],  # 中标企业投标价格
                    material_inventory=CompanyReportMarketResearchdate[32+i],  # 原材料库存量
                    attachment_inventory=CompanyReportMarketResearchdate[34+i],  # 附件库存量
                    inventory=CompanyReportMarketResearchdate[36+i],  # 产品积累库存数量
                    robots=CompanyReportMarketResearchdate[38+i],  # 机器人数量
                    researh_stuff=CompanyReportMarketResearchdate[40+i],  # 研发人员数
                    general_market_plan=CompanyReportMarketResearchdate[42+i],  # 一般市场计划量
                    general_market_prd=CompanyReportMarketResearchdate[44+i],  # 一般市场生产量
                    maintain_coe=CompanyReportMarketResearchdate[46+i],  # 维修保养系数
                    rationalization_coe=CompanyReportMarketResearchdate[48+i],  # 合理化系数
                    prd_capacity=CompanyReportMarketResearchdate[50+i],  # 生产线生产能力
                    prd_personnel=CompanyReportMarketResearchdate[52+i],  # 生产线人员数
                    prd_line_load=CompanyReportMarketResearchdate[54+i],  # 生产线负载率
                    prd_personnel_load=CompanyReportMarketResearchdate[56+i],  # 生产线人员负载率
                    general_market_cost=CompanyReportMarketResearchdate[58+i],  # 一般市场的产品成本
                    profit=CompanyReportMarketResearchdate[60+i],  # 税前经营成果
                    curr_loss=CompanyReportMarketResearchdate[62+i],  # 本周期亏损结转
                    curr_dividend=CompanyReportMarketResearchdate[64+i],  # 本周期股息支付
                    curr_profit=CompanyReportMarketResearchdate[66+i],  # 本周期利润储备
                    curr_mid=CompanyReportMarketResearchdate[68+i],  # 本周期中期贷款
                    curr_ending=CompanyReportMarketResearchdate[70+i],  # 本周期期末现金
                    total_profit=CompanyReportMarketResearchdate[72+i],  # 总的利润储备额
                    curr_loan=CompanyReportMarketResearchdate[74+i],  # 本周期透支贷款
                    assets_liabilities=CompanyReportMarketResearchdate[76+i],  # 资产负债总和
                )
            company_report_MarketPrd.save()  # 保存报告数据

        # 6
        # 6
        # 6
        # 6
        # 6
        #爬取并插入评价总表数据库数据

        #爬取数据
        url='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/result/mreport.aspx?type=1'
        response=session.get(url=url)

        def filter_data(data):
            """只保留包含阿拉伯数字或'--'的数据"""
            filtered_data = {}
            for key, values in data.items():
                filtered_values = [v for v in values if re.search(r'\d', v) or '--' in v]
                filtered_data[key] = filtered_values
            return filtered_data
        summart_evaluation={}
        categories = [
            ['pr', 'nm', 'gs', 'pfz'],
            ['市场类指标', '生产类指标', '财务类指标', '决策综合评价']
        ]
        for i, j in zip(categories[0], categories[1]):
            url = 'http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/result/report.aspx?item='+i 
            response = session.get(url)
            tree=etree.HTML(response.text)
            element= tree.xpath('//font[@style="font-size:16px"]/text()')
            filtered_element = [text.replace('\xa0', '') for text in element]
            summart_evaluation[j]=filtered_element

        url='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/result/quanzhong.aspx'
        response=session.get(url=url)
        tree=etree.HTML(response.text)
        element= tree.xpath('//div[@style="font-size:16px;"]/text()')
        filtered_element = [text.replace('\xa0', '') for text in element]
        summart_evaluation['评价指标权重']=filtered_element
        summart_evaluation = filter_data(summart_evaluation)      

        #开始存入数据
        uid = request.session.get('uid')
        round_reports = Round.objects.filter(uid=uid).annotate(round_id_int=Cast('round_id', IntegerField())).order_by('-round_id_int').first()
        evaluation_dic = {'市场类指标':['一般市场价格','广告费用','销售人员数量','研发投入效应','一般市场计划量','一般市场销售量','一般市场销售额','理论市场占有率','实际市场占有率'],
                        '生产类指标':['一般市场产量','累积产品库存','生产人员数量','生产设备负荷','生产人员负荷','机器人累计数','产品质量评价','设备生产能力'],
                        '财务类指标':['税前经营成果','周期缴纳税收','周期支付股息','总的盈亏累计','周期贷款总额','周期期末现金','资产负债合计'],
                        }
        for type,projects in evaluation_dic.items():
            for i, project in enumerate(projects):
                start_index = i * 17
                end_index = start_index + 17

                # 创建并保存Evaluation记录(计算机)
                evaluation = Evaluation(
                    round_id=round_reports,       # 关联到一个决策轮次
                    project=project,             # 项目名称
                    company='计算机',               # 企业名称
                    cycle_number=cycle_num-1,                # 周期
                    weight=float(summart_evaluation[type][start_index:end_index][0][4]),                   # 权数
                    value=float(summart_evaluation[type][start_index:end_index][cycle_num-1]),                  # 值
                    score_ranking=float(summart_evaluation[type][start_index:end_index][8])                     # 评分
                )
                # 保存到数据库
                evaluation.save()

                # 创建并保存Evaluation记录（本企业）
                evaluation = Evaluation(
                    round_id=round_reports,       # 关联到一个决策轮次
                    project=project,             # 项目名称
                    company='本企业',               # 企业名称
                    cycle_number=cycle_num-1,                # 周期
                    weight=float(summart_evaluation[type][start_index:end_index][0][4]),                   # 权数
                    value=float(summart_evaluation[type][start_index:end_index][cycle_num+7]),                  # 值
                    score_ranking=float(summart_evaluation[type][start_index:end_index][16])                     # 评分
                )
                # 保存到数据库
                evaluation.save()
        # 创建并保存Evaluation记录(计算机)
        evaluation = Evaluation(
            round_id=round_reports,       # 关联到一个决策轮次
            project='决策综合评价' ,        # 项目名称
            company='计算机',               # 企业名称
            cycle_number=cycle_num-1,                # 周期
            value=float(summart_evaluation['决策综合评价'][cycle_num-2]),                  # 值
            score_ranking=float(summart_evaluation['决策综合评价'][7])                     #排名
        )
        # 保存到数据库
        evaluation.save()

        # 创建并保存Evaluation记录（本企业）
        evaluation = Evaluation(
            round_id=round_reports,       # 关联到一个决策轮次
            project='决策综合评价',             # 项目名称
            company='本企业',               # 企业名称
            cycle_number=cycle_num-1,                # 周期                 
            value=float(summart_evaluation['决策综合评价'][cycle_num+6]),                  # 值
            score_ranking=float(summart_evaluation['决策综合评价'][15])                     # 排名
        )
        evaluation.save()


        #插入或更新Datakeep记录
        action = Datakeep.get_or_update_data(
            uid,
            response_look1=response_look1,
            response_lookhistory=response_lookhistory,
            response_historical_decision=response_historical_decision,
            compete_outcome=compete_outcome,
            response_enterreporting=response_enterreporting,
            summart_evaluation=summart_evaluation
        )

    else:
        soup = BeautifulSoup(response_update_decision_data.text, 'html.parser')
        response_submit_decision_data['提交结果']=soup.select_one("#contentplaceholderadd_Label8").text 
    return JsonResponse(response_submit_decision_data)       



@csrf_exempt
def historical_decision(request):
    from .models import User, Datakeep
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)

    # 从Datakeep内获取输出数据
    uid = request.session.get('uid')
    user_instance = User.objects.get(uid=uid)
    response_historical_decision="response_historical_decision"
    response_historical_decision = Datakeep.get_field_data(user_instance,response_historical_decision)

    return JsonResponse(response_historical_decision)


@csrf_exempt
def compete_outcome_fun(request):
    from .models import User,Round,Cycle,CompetitionResult,Datakeep
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)

    # uid = request.session.get('uid')
    # round_reports = Round.objects.filter(uid=uid).annotate(round_id_int=Cast('round_id', IntegerField())).order_by('-round_id_int').first()
    # cycle_reports = Cycle.objects.filter(round_id=round_reports.round_id).annotate(cycle_id_int=Cast('cycle_id', IntegerField())).order_by('-cycle_id_int').first()

    # # 查找数据库中是否已有该周期的数据
    # competition_result = CompetitionResult.objects.filter(cycle_id=cycle_reports.cycle_id).first()

    # if competition_result:
    uid = request.session.get('uid')
    user_instance = User.objects.get(uid=uid)
    compete_outcome="compete_outcome"
    compete_outcome = Datakeep.get_field_data(user_instance,compete_outcome)
    return JsonResponse(compete_outcome)  




@csrf_exempt
def enterreporting(request):
    from .models import User, Datakeep
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)
    uid = request.session.get('uid')
    user_instance = User.objects.get(uid=uid)
    response_enterreporting="response_enterreporting"
    response_enterreporting = Datakeep.get_field_data(user_instance,response_enterreporting)
    return JsonResponse(response_enterreporting)  



@csrf_exempt
def get_summart_evaluation(request):
    from .models import User, Datakeep
    # 从 session 中获取之前保存的 cookies
    session_cookies = request.session.get('session_cookies')

    # 使用 requests.Session() 复用登录状态
    session = requests.Session()
    session.cookies.update(session_cookies)
    uid = request.session.get('uid')
    user_instance = User.objects.get(uid=uid)
    summart_evaluation="summart_evaluation"
    summart_evaluation = Datakeep.get_field_data(user_instance,summart_evaluation)

    return JsonResponse(summart_evaluation) 
