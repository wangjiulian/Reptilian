#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/8/18 下午11:45
# @Author   : avery.wang
# @File     : itchat_talk.py

import douban
import itchat


@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE])
def simple_reply(msg):
    global movie_info_all
    # 接受用户任意包含'电影'的字样，跳转到指定页面等待
    if u'电影' in msg['Text']:
        douban_object.browser_hotopen()
        douban_object.cvt_cmd_to_ctgy_url(msg['Text'])
        movie_category_option = ' '.join(douban.movie_category)
        itchat.send_msg('------请选择一种类型-----\n' + movie_category_option, msg['FromUserName']);
    #接受用户的电影类型输入，并执行概括信息爬取，然后反馈给用户
    elif msg['Text'] in douban.movie_category:
        itchat.send_msg('正在查找' + msg['Text'] + '电影.....',msg['FromUserName'])
        del douban.command_cache[:]
        douban.command_cache.append(msg['Text'])
        #进行概括信息爬取,并将所有排列列表扩展到一起
        movie_info_all = douban_object.browser_action_general_info(msg['Text'])
        itchat.send_msg('----按热度排序----\n' +'\n' +'\n'.join(douban.movie_info_hot), msg['FromUserName'])
        itchat.send_msg('----按时间排序----\n' + '\n' + '\n'.join(douban.movie_info_time), msg['FromUserName'])
        itchat.send_msg('----按评论排序----\n' + '\n' + '\n'.join(douban.movie_info_comment), msg['FromUserName'])
    # 接受用户的电影名选择，并进行制定电影的详细字段信息爬取，然后反馈给用户
    else:
        search_index = 0
        for x in movie_info_all:
            if msg['Text'] in x:
                itchat.send_msg('正在查找' + msg['Text'] + '...', msg['FromUserName'])
                loc = movie_info_all.index(x)
                if 0<= loc < 10:
                    search_index = 1
                elif 10<= loc <20:
                    search_index = 2
                else:
                    search_index = 3
                break


        if search_index == 0:

            return

        url_result = douban_object.browser_action_detail_info(search_index,msg['Text'])
        html_result = douban_object.download_detail_info_html(url_result)
        douban_object.parse_detail_info(html_result)
        itchat.send_msg('\n\n'.join(douban.movie_detail_info), msg['FromUserName'])




if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    douban_object = douban.DoubanSpider()
    movie_info_all = []
    itchat.run()


