import requests
from bs4 import BeautifulSoup
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

#辅助函数，重新登录
def relogin(uid):
    print('重新登陆')
    from .models import User
    session=requests.Session()
    user=User.objects.get(uid=uid)
    url_relogin='http://www.jctd.net/cyjc/cyrjdkweb/cysx/rjdkweb/default.aspx?vdir=2&vdxmc=%e5%86%b3%e7%ad%96%e6%94%af%e6%8c%81%e7%b3%bb%e7%bb%9f%e5%af%bc%e8%ae%ba&vrjslogin=True'
    response = session.get(url=url_relogin)
    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_fields = extract_hidden_fields(soup)
    
    data_relogin={
        '__EVENTTARGET': hidden_fields.get('__EVENTTARGET', ''),
        '__EVENTARGUMENT': hidden_fields.get('__EVENTARGUMENT', ''),
        '__VIEWSTATE': hidden_fields.get('__VIEWSTATE', ''),
        '__VIEWSTATEGENERATOR': hidden_fields.get('__VIEWSTATEGENERATOR', ''),
        '__EVENTVALIDATION': hidden_fields.get('__EVENTVALIDATION', ''),
        'stuid':user.student_id,
        'mima':user.password,
        'login': '登录',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    }
    response_relogin=session.post(url=url_relogin,data=data_relogin)
    return session.cookies.get_dict()