#! /usr/bin/env python
# --*-- coding:utf-8 --*--

__author__ = 'jeff.yu'

from sys import path
from os.path import sep
import json
from common.tools import combinationChoice, datetime_timestamp, JsonToStr
from random import choice


class Producer(object):

    def __init__(self, queryType):
        self.queryType = queryType
        self.setDimensionFile()
        self.getStructData()
        self.getDimension()
        self.getData()
        self.setDatasource()
        self.setQueryReportId()
        self.setQuerySetting()
        self.setQueryDimension()
        self.setQueryData()
        self.setQueryFilter()
        self.setQueryTopn()
        self.setQuerySort()

    def setDimensionFile(self):
        if self.queryType not in ('yeahmobi', 'tradingdesk'):
            exit(-1)
        parentPath = path[0].replace('cases', 'config')
        self.dimensionFile = '{0}{1}{2}.json'.format(parentPath, sep, self.queryType)

    def getStructData(self):
        try:
            with open(self.dimensionFile) as f:
                lines = f.read()
        except Exception as e:
            raise e
        else:
            if isinstance(lines, dict):
                self.structData = lines
            else:
                try:
                    self.structData = json.loads(lines)
                except Exception as e:
                    raise e

    def setDatasource(self):
        datasourceMap = {'yeahmobi': 'ymds_druid_datasource',
                         'tradingdesk': 'contrack_druid_datasource_ds'}
        self.queryDatasource = datasourceMap.get(self.queryType)

    def setQueryReportId(self):
        self.queryReportId = ''
        choiced = combinationChoice(range(100), 10)
        for choice in choiced:
            self.queryReportId += str(choice)


    def getDimension(self):
        self.dimensions = self.structData.get('dimensions')

    def getData(self):
        self.data = self.structData.get('data')

    def setQuerySetting(self):
        timeStart, timeEnd = datetime_timestamp()
        self.querySetting = {"time":{"start":timeStart,"end":timeEnd,"timezone":0},
                             "return_format":"json",
                             "report_id":self.queryReportId,
                             "data_source":self.queryDatasource,
                             "pagination":{"size":1000000,"page":0}
        }

    def setQueryDimension(self):
        self.queryDimension = combinationChoice(self.dimensions, 5)

    def setQueryData(self):
        self.queryData = combinationChoice(self.data, 4)

    def setQueryFilter(self):
        # 该过滤条件只针对查询接口
        # FilterValue 需要重新获取
        self.filterList = {}
        choiceItem = self.data + self.dimensions
        filterCount = choice(range(1, 4)) # 随机生成过滤条件的深度
        filterValue = []
        dimensionOperatorList = ('$eq', '$neq', '$in', '$nin') # dimension 常用的过滤操作
        dataOperatorList = ('$gt', '$gte', '$lt', '$lte') # data 常用的过滤操作
        for count in range(filterCount):
            filterKey = choice(choiceItem)
            if filterKey not in self.filterList:
                if filterKey in self.data:
                    self.filterList[filterKey] = {choice(dataOperatorList): filterValue}
                else:
                    self.filterList[filterKey] = {choice(dimensionOperatorList): filterValue}
            else:
                pass
        self.queryFilter = {'$and': self.filterList}

    def setQuerySort(self):
        self.querySort = {}
        self.querySort['orderBy'] = choice(self.data)  # 从所有的data中获取，而不是从query的data中获取
        self.querySort['order'] = choice((1, -1))

    def setQueryTopn(self):
        self.queryTopn = {}
        self.queryTopn['metricvalue'] = choice(self.data) # 从所有的data中获取，而不是从query的data中获取
        self.queryTopn['threshold'] = choice(range(1,100))

    def getQuery(self):
        jsonQuery = {"settings":self.querySetting,
                     "group":self.queryDimension,
                     "data":self.queryData,
                     "topn":self.queryTopn,
                     "filters":self.queryFilter,
                     "sort":[self.querySort]}
        return JsonToStr(jsonQuery)

if __name__ == '__main__':
    p = Producer('yeahmobi')
    print p.getQuery()