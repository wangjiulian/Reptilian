
import time
import requests
from bs4 import BeautifulSoup


class JD_crawl:
    def __init__(self, username, password):


        try:
            self.headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
                'Referer': 'https://www.jd.com/'

            }
            self.login_url = 'https://passport.jd.com/new/login.aspx'
            self.post_url = "https://passport.jd.com/uc/loginService"
            self.auth_url = "https://passport.jd.com/uc/showAuthCode"
            self.session = requests.session()
            self.username = username
            self.password = password
        except Exception as e:
            print(e)


    def get_login_info(self):
        html = self.session.get(self.login_url, headers = self.headers).content
        soup = BeautifulSoup(html,'lxml')

        uuid = soup.select('#uuid')[0].get('value')
        eid = soup.select('#eid')[0].get('value')
        fp = soup.select('input[name="fp"]')[0].get('value')
        _t = soup.select('input[name="_t"]')[0].get('value')
        login_type = soup.select('#loginType')[0].get('value')
        pub_key = soup.select('#pubKey')[0].get('value')
        sa_token = soup.select('#sa_token')[0].get('value')
        use_slide_auth_code = soup.select('#useSlideAuthCode')[0].get('value')



        data = {
            'uuid': uuid,
            'eid': eid,
            'fp': fp,
            '_t': _t,
            'loginType': login_type,
            'loginname': self.username,
            'nloginpwd': self.password,
            'pubKey': pub_key,
            'sa_token': sa_token,
            'useSlideAuthCode': 1
        }
        return  data


    def login(self):
        data = self.get_login_info()
        headers = {
            'referer': self.post_url,
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            login_page = self.session.post(self.post_url, data = data, headers = headers)
            print(login_page)
        except Exception as e:
            print(e)



if __name__ == '__main__':
    un = input('请输入账号：')
    pwd = input('请输入密码：')
    jd = JD_crawl(un, pwd)
    jd.login()

