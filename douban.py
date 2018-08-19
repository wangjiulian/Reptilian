import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from time import  sleep
from selenium import  webdriver



headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

movie_category = ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳门',
                  '华语', '欧美', '韩国', '日本', '动作', '喜剧', '爱情',
                  '科幻', '悬疑', '恐怖', '动画']

movie_info_hot = []
movie_info_time = []
movie_info_comment = []
command_cache = []
movie_detail_info = []

class DoubanSpider(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.douban_url_base = 'https://movie.douban.com/'
        self.url_category = ''
        self.url_picture = ''
        self.url_movie_detail_info = []

    #接受用户电影搜索
    def cvt_cmd_to_ctgy_url(self, command):

        if '电影' == command:
            self.url_category = self.douban_url_base +'explore'

    #打开浏览器就绪
    def browser_hotopen(self):
        print('打开浏览器')
        self.driver.get(self.douban_url_base)

    #根据电影类型爬取数据
    def browser_action_general_info(self, type_command):

        self.driver.get(self.url_category)
        sleep(1)
        # 点击选择电影类型
        for num in range(0, len(movie_category)):
            if type_command == movie_category[num]:
                self.driver.find_element_by_xpath('//*[@class="tags"]/div/label[{}]'.format(num + 1)).click()
        sleep(1)
        # 进行电影概况信息爬取
        self.browser_crawl_general_info()
        return movie_info_hot + movie_info_time + movie_info_comment



    # 爬取热门，时间，评分 前10个电影数据
    def browser_crawl_general_info(self):

        # 清空顺列排列的列表，为用户下一次操作准备
        del movie_info_hot[:]
        del movie_info_time[:]
        del movie_info_comment[:]
        for num in range(1,4):
            # 分别点击hot, time, comment顺序排列
            self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div'
                                              '[1]/form/div[3]/div[1]/label[{}]/input'.format(num)).click()
            sleep(1)
            # 分别获取三组顺序排列的前十个电影名和评分
            for counter in range(1, 11):
                if num == 1:
                    movie_info_hot.append(self.get_movie_general_info(counter))
                elif num == 2:
                    movie_info_time.append(self.get_movie_general_info(counter))
                elif num == 3:
                    movie_info_comment.append(self.get_movie_general_info(counter))
                else:
                    pass
        #对数据进行清洗整理
        self.clean_general_info()

    def get_movie_general_info(self, counter):

        each_movie_info = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]'
                                                            '/div/div[4]/div/a[{}]/p'.format(counter)).text
        return each_movie_info

    #清洗数据
    @staticmethod
    def clean_general_info():
        for num in range(0, len(movie_info_hot)):
            movie_info_hot[num] = movie_info_hot[num].replace(' ', ':  ')
            movie_info_time[num] = movie_info_time[num].replace(' ', ':  ')
            movie_info_comment[num] = movie_info_comment[num].replace(' ', ':  ')
            movie_info_hot[num] = str(num + 1) + '.' + movie_info_hot[num] + '分'
            movie_info_time[num] = str(num + 1) + '.' + movie_info_time[num] + '分'
            movie_info_comment[num] = str(num + 1) + '.' + movie_info_comment[num] + '分'


    #根据电影类型+排序类型+电影位置 获取地址
    def browser_action_detail_info(self, counter, movie_name):

        movie_click_num = 0
        # click the type of moive
        # 点击上次用户选择的电影类型
        for num in range(0, len(movie_category)):
            if command_cache[0] == movie_category[num]:
                self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div[1]'
                                                  '/form/div[1]/div[1]/label[{}]'.format(num + 1)).click()
        sleep(1)
        #点击选择用户选择的电影所在顺序排列
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[2]/div'
                                          '[1]/form/div[3]/div[1]/label[{}]/input'.format(counter)).click()

        sleep(1)
        if counter == 1:
            for x in range(0, len(movie_info_hot)):
                if movie_name in movie_info_hot[x]:
                    movie_click_num = x + 1
        elif counter == 2:
            for x in range(0, len(movie_info_time)):
                if movie_name in movie_info_time[x]:
                    movie_click_num = x + 1
        else:
            for x in range(0, len(movie_info_comment)):
                if movie_name in movie_info_comment[x]:
                    movie_click_num = x + 1

         # 点击电影名称进入详细界面,记录详细界面的url
        movie_detail_url = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[4]/div/a[{}]'
                                                             .format(movie_click_num)).get_attribute('href')
        return movie_detail_url

    # 下载电影详情界面
    @staticmethod
    def download_detail_info_html(url_target):
            try:
                response = urllib.request.Request(url_target, headers = headers)
                result = urllib.request.urlopen(response)
                html = result.read().decode('utf-8')
                return html
            except urllib.error.HTTPError as e:
                if hasattr(e,'code'):
                    print(e.code)
            except urllib.error.URLError as e:
                if hasattr(e,'reason'):
                    print(e.reason)

    @staticmethod
    def parse_detail_info(html_result):

        # 清空详细信息列表
        del movie_detail_info[:]
        # 定义详细信息字段
        movie_name = ''
        director_name = '导演：'
        actor_name_list = '主演：'
        movie_type = '类型：'
        movie_date = '上映日期：'
        movie_runtime = '片长：'

        soup = BeautifulSoup(html_result, 'lxml')
        # 用BeautilSoup 方法从下载页面提取字段信息
        movie_name = movie_name + soup.find('span', property='v:itemreviewed').string.strip()\
        + soup.find('span',class_='year').string.strip()
        director_name = director_name + soup.find('a', rel='v:directedBy').string.strip()
        for x in soup.find_all('a',rel='v:starring'):
            actor_name_list = actor_name_list + x.string.strip()+'/'

        for x in soup.find_all('span', property='v:genre'):
            movie_type = movie_type + x.string.strip()+'/';

        movie_date = movie_date + soup.find('span', property='v:initialReleaseDate').string.strip()
        movie_runtime = movie_runtime + soup.find('span',property='v:runtime').string.strip()

        #将所有信息存入详细信息列表中
        movie_detail_info.append(movie_name)
        movie_detail_info.append(director_name)
        movie_detail_info.append(actor_name_list)
        movie_detail_info.append(movie_type)
        movie_detail_info.append(movie_date)
        movie_detail_info.append(movie_runtime)




if __name__ == '__main__':
     douban = DoubanSpider()
     # un = input('请输入关键字')
     # if u'电影' in un:
     #     douban.browser_hotopen()
     #     douban.cvt_cmd_to_ctgy_url('电影')
     #     movie_catrgory_option = ' '.join(movie_category)
     #     print('----请选择一种类型----\n' + movie_catrgory_option)

     # douban.browser_hotopen()
     # douban.cvt_cmd_to_ctgy_url('电影')
     # movie_catrgory_option = ' '.join(movie_category)
     # print('----请选择一种类型----\n' + movie_catrgory_option)
     # in_movie_type = input('请输入电影类型')
     # del  command_cache[:]
     # command_cache.append(in_movie_type)
     # movie_info_all = douban.browser_action_general_info(in_movie_type)
     # print('-----按热度排序----\n\n'+ ''.join(movie_info_hot)+'\n')
     # print('-----按时间排序----\n\n' + ''.join(movie_info_time) + '\n')
     # print('-----按评论排序----\n\n' + ''.join(movie_info_comment) + '\n')
     #
     # in_movie_name = input('请输入电影名称')
     # search_num = 0
     # for x in movie_info_all:
     #    if in_movie_name in x:
     #        loc = movie_info_all.index(x)
     #        if 0<=loc<10:
     #            search_num = 1
     #        elif 10<= loc < 20:
     #            search_num = 2
     #        else:
     #            search_num = 3
     #        break
     #
     # url_result = douban.browser_action_detail_info(search_num,in_movie_name)
     # html_result = douban.download_detail_info_html(url_result)
     # douban.parse_detail_info(html_result)
     # print(movie_detail_info)















