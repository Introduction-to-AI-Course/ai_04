# -*- coding:utf8 -*-
import pandas as pd
import datetime


def run():
    data=pd.read_excel(r'outfile\热点问题留言明细表含热度指数.xlsx')
    flag=data['问题ID'][0]
    max=data['留言时间'][0]
    min=data['留言时间'][0]
    timearray=[]
    hotflag=[]
    hotflag.append(data['热点问题评分'][0])
    #前n-1个
    for index,row in data.iterrows():
        if flag==row['问题ID']:
            if row['留言时间']>=max:
                max=row['留言时间']
            else:
                min=row['留言时间']
        else:
            hotflag.append(row['热点问题评分'])
            string_1 = pd.to_datetime(max).strftime("%Y%m%d")
            string_2 = pd.to_datetime(min).strftime("%Y%m%d")
            timearray.append(string_2+"至"+string_1)
            max=row['留言时间']
            min=row['留言时间']
        flag = row['问题ID']
    #第n个
    string_1 = pd.to_datetime(max).strftime("%Y%m%d")
    string_2 = pd.to_datetime(min).strftime("%Y%m%d")
    timearray.append(string_2+"至"+string_1)
    newtimearray=[]
    for x in timearray:
        new=[]
        for y in x:
            new.append(y)
        new.insert(4, '/')
        new.insert(7, '/')
        new.insert(15, '/')
        new.insert(18, '/')
        string=""
        for t in new:
            string=string+t
        newtimearray.append(string)
    print(newtimearray)
    df=pd.DataFrame(columns=['热度排名', '问题ID', '热度指数', '时间范围', '地点/人群', '问题描述'])
    df['问题ID']=[x+1 for x in range(5)]
    df['热度排名']=[x+1 for x in range(5)]
    df['热度指数']=[x for x in hotflag]
    df['时间范围']=[x for x in newtimearray]

    df.to_excel('outfile/问题2 热点问题表.xlsx',index=False)

