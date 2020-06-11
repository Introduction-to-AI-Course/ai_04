# -*- coding:utf8 -*-

# 是否有感谢来信/关心/...
import re


def thx(sentence):
    grade = 0
    Suffix = ['来信', '理解', '支持', '关心', '关注', '建议', '监督']
    pat = '[感谢]谢[\u4e00-\u9fa5]*'
    for i in range(len(Suffix)):
        m = re.findall(pat + Suffix[i], sentence)
        # print(m)
        if len(m):
            grade += 10
            break
    return grade