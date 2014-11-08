#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

from random import choice
from datetime import date, timedelta
import redis
import time
import json



def combinationChoice(seq, count):
    """
    :param seq: [1,2,3,4,5,6,7,8,9,10]
    :param count: 3
    :return: [2,10,3]
    """
    choiceItem = []
    if not seq:
        return choiceItem
    loopCount = len(seq)
    for i in range(loopCount):
        selected = choice(seq)
        if selected not in choiceItem:
            choiceItem.append(selected)
        if len(choiceItem) == count:
            break
    return choiceItem


def datetime_timestamp():
    time_end = date.today()
    time_start = time_end + timedelta(days=-1)
    str_time_start, str_time_end = time_start.strftime('%Y-%m-%d'), time_end.strftime('%Y-%m-%d')
    return int(time.mktime(time.strptime(str_time_start, '%Y-%m-%d'))) + 28800, int(time.mktime(time.strptime(str_time_end, '%Y-%m-%d'))) + 28800


def queryConvert(jsonQuery):
    return str(jsonQuery)

def getIdList(redisHost, redisPort):
    try:
        r = redis.Redis(host= redisHost,
                        port= redisPort,
                        db = 0)
    except Exception as e:
        raise e

    offerList = (offerId.lstrip('o') for offerId in r.keys('o*'))
    affIdList = r.keys('a*')
    affList = []
    amList = []
    for aff in affIdList:
        affList.append(aff.lstrip('a'))
        amList.append(json.loads(aff).get('affManagerId'))
    return offerList, affList, amList

def JsonToStr(jsonReq):
    return str(jsonReq).replace("'", '"')