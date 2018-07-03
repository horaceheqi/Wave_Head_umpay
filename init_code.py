import numpy as np
import pandas as pd
import time


class initialize(object):

    def __init__(self):
        self.list_data = list()
        self.columns = list()
        self.body = list()

    def get_datas(self, fileName):
        with open(fileName, 'r', encoding='utf-8', errors='replace') as fRead:
            for lines in fRead.readlines():
                temp_list = list()
                data_line = lines.strip().split(',')
                for temp in data_line:
                    if temp == 'unknown':
                        temp_list.append(0)
                    else:
                        temp_list.append(temp)
                self.list_data.append(temp_list)
        self.columns = self.list_data[0]
        self.body = self.list_data[1:]
        # print(self.name)
        # print(self.body)

    def calculateData(self):
        df = pd.DataFrame(self.body, columns=self.columns)
        df['资产负增长环比_1'] = (df['借记卡消费金额_近4个月_第2月汇总'].map(float)- df['借记卡消费金额_近4个月_第1月汇总'].map(float))/df['借记卡消费金额_近4个月_第1月汇总'].map(int)
        df['资产负增长环比_2'] = (df['借记卡消费金额_近4个月_第3月汇总'].map(float) - df['借记卡消费金额_近4个月_第2月汇总'].map(float)) / df['借记卡消费金额_近4个月_第2月汇总'].map(int)
        df['资产负增长环比_3'] = (df['借记卡消费金额_近4个月_第4月汇总'].map(float) - df['借记卡消费金额_近4个月_第3月汇总'].map(float)) /df['借记卡消费金额_近4个月_第3月汇总'].map(int)
        df['消费正增长_1'] = df['借记卡消费金额_近4个月_第1月汇总'].map(float) + df['信用卡出账金额_近4个月_第1月汇总'].map(float)
        df['消费正增长_2'] = df['借记卡消费金额_近4个月_第2月汇总'].map(float) + df['信用卡出账金额_近4个月_第2月汇总'].map(float)
        df['消费正增长_3'] = df['借记卡消费金额_近4个月_第3月汇总'].map(float) + df['信用卡出账金额_近4个月_第3月汇总'].map(float)
        df['消费正增长_4'] = df['借记卡消费金额_近4个月_第4月汇总'].map(float) + df['信用卡出账金额_近4个月_第4月汇总'].map(float)
        df['消费正增长环比_1'] = (df['消费正增长_2'] - df['消费正增长_1']) / df['消费正增长_1']
        df['消费正增长环比_2'] = (df['消费正增长_3'] - df['消费正增长_2']) / df['消费正增长_2']
        df['消费正增长环比_3'] = (df['消费正增长_4'] - df['消费正增长_3']) / df['消费正增长_3']
        df.rename(columns={'信用评分(标准版)_近3个月_第1月汇总':'信用评分_1'}, inplace=True)
        df.rename(columns={'信用评分(标准版)_近3个月_第2月汇总': '信用评分_2'}, inplace=True)
        df.rename(columns={'信用评分(标准版)_近3个月_第3月汇总': '信用评分_3'}, inplace=True)
        df.rename(columns={'历史风险评估(还款意愿及能力)_近3个月_第1月汇总': '风险评分_1'}, inplace=True)
        df.rename(columns={'历史风险评估(还款意愿及能力)_近3个月_第2月汇总': '风险评分_2'}, inplace=True)
        df.rename(columns={'历史风险评估(还款意愿及能力)_近3个月_第3月汇总': '风险评分_3'}, inplace=True)
        df.rename(columns={'潜在承债能力(标准版)_近3个月_第1月汇总': '潜在承债能力下降_1'}, inplace=True)
        df.rename(columns={'潜在承债能力(标准版)_近3个月_第2月汇总': '潜在承债能力下降_2'}, inplace=True)
        df.rename(columns={'潜在承债能力(标准版)_近3个月_第3月汇总': '潜在承债能力下降_3'}, inplace=True)
        result_cloumns = ['mobileid','identityNo','name','querymonth','cid','资产负增长环比_1','资产负增长环比_2','资产负增长环比_3',
                          '消费正增长_1','消费正增长_2','消费正增长_3','信用评分_1','信用评分_2',
                          '信用评分_3','风险评分_1','风险评分_2','风险评分_3','潜在承债能力下降_1',
                          '潜在承债能力下降_2','潜在承债能力下降_3']
        result = df[result_cloumns]
        result = result.fillna(0)
        result = result.replace(np.inf, 0)
        result.to_csv('result.csv', encoding='utf-8', index=False)
        # print(result.head(100))


if __name__ == '__main__':
    dataFile = r'D:/联动优势/日常/数据/2018-6/波动类抬头/Hive000115285_1.txt'
    start = time.clock()
    demo = initialize()
    demo.get_datas(dataFile)
    demo.calculateData()
    end = time.clock()
    print("消耗时间：%f s" % (end - start))