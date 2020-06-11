# -*- coding:utf8 -*-

# 电话评分
import re

def Tel(sentence):
    telList = ['119', '12395', '110', '12121', '120', '12117', '122', '999', '12110', '95119', '114', '112', '11185',
               '12306', '12348', '95598', '12318', '12315', '12358', '12365', '12310', '12369', '12333', '12345',
               '12320', '10000', '10010', '10086', '17900', '17911', '17951', '116114', '118114', '10050', '10086999',
               '95555', '95599', '95566', '95568', '95533', '95595', '95588', '95559', '95558', '95508', '95528',
               '95577', '95501', '95561', '95543', '95338', '95546', '95554', '95311', '95353', '4009565656', '11185']
    grade = 0
    # 查找电话号码
    pat = '\d+-\d+-?\d*'
    res = re.findall(pat, sentence)
    # 添加tel.txt中类似12315的电话
    for i in telList:
        if sentence.find(i) != -1:
            res.append(i)
    if len(res) != 0:
        grade += 10

    tolerant = 10  # 容忍区间 TODO 容忍区间可以进一步调小
    prefix = ['咨询', '电话', '拨', '致电', '联系']

    # 查找电话前面是否有 咨询电话：，拨打 等字眼
    for i in res:
        for pre in prefix:
            telIndex = sentence.find(i)
            preIndex = sentence.find(pre)
            if preIndex == -1:
                continue
            if preIndex + tolerant >= telIndex:
                # 在容忍区间内
                grade += 5
                return grade
    return grade