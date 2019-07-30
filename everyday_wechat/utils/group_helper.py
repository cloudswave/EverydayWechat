# -*- coding: utf-8 -*-
"""
Project: EverydayWechat-Github
Creator: DoubleThunder
Create time: 2019-07-11 12:55
Introduction: 群消息处理
"""

import re
from datetime import datetime
import itchat

from everyday_wechat.utils import config
from everyday_wechat.utils.pattern_helper import handle_msg_helper
from everyday_wechat.utils.data_collection import (
    get_weather_info,
    get_bot_info,
    # get_calendar_info,
)
at_compile = r'(@.*?\s{1,}).*?'
common_msg = '@{ated_name}\u2005\n{text}'
# import pysnooper
# @pysnooper.snoop()
def handle_group_helper(msg):
    """
    处理群消息
    :param msg:
    :return:
    """

    conf = config.get('group_helper_conf')
    if not conf.get('is_open'):
        return
    text = msg['Text']

    # 如果开启了 『艾特才回复』，而群用户又没有艾特你。不处理消息
    if conf.get('is_at') and not msg.isAt:
        return

    uuid = msg.fromUserName  # 群 uid
    ated_uuid = msg.actualUserName  # 艾特你的用户的uuid
    ated_name = msg.actualNickName  # 艾特你的人的群里的名称

    is_all = conf.get('is_all', False)
    user_uuids = conf.get('group_black_uuids') if is_all else conf.get('group_white_uuids')

    # 开启回复所有群，而用户是黑名单，不处理消息
    if is_all and uuid in user_uuids:
        return

    # 未回复所有群，而用户不是白名单，不处理消息
    if not is_all and uuid not in user_uuids:
        return
    # 去掉 at 标记
    text = re.sub(at_compile, '', text)
    retext = handle_msg_helper(text, ated_uuid, ated_name)
    if retext:
        itchat.send(retext, toUserName=uuid)
        return

    # 其他结果都没有匹配到，走自动回复的路
    if conf.get('is_auto_reply'):
        reply_text = get_bot_info(text, ated_uuid)  # 获取自动回复
        if reply_text:  # 如内容不为空，回复消息
            reply_text = common_msg.format(ated_name=ated_name, text=reply_text)
            itchat.send(reply_text, uuid)
            print('回复{}：{}'.format(ated_name, reply_text))
        else:
            print('自动回复失败\n')


# 通过用户id找好友
def get_city_by_uuid(uid):
    """
    通过用户的uid得到用户的城市
    最好是与机器人是好友关系
    """
    itchat.get_friends(update=True)
    info = itchat.search_friends(userName=uid)
    # print('info:'+str(info))
    if not info:
        return None
    city = info.city
    # print('city:'+city)
    return city
