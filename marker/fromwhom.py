# -*- coding:utf8 -*-
import re


def FromWhom(sentence, nlp):
    sentence1 = sentence.replace(' ', '')
    grade = 0
    res = nlp.ner(sentence1)
    tag = 0
    name = ''
    labels = []
    for i in range(len(res)):
        if res[i][1] != 'ORGANIZATION':
            if tag != 0:
                labels.append(name)
                name = ''
                tag = 0
        else:
            tag = 1
            name += res[i][0]

    if len(labels) == 0:
        return 0
    last = labels[len(labels) - 1]  # 机构列表的最后一个元素
    tolerant = 3  # 容忍区间,只容许实体后有几个字符

    # 去除最后的答复时间
    mode = '[0-9零一二两三四五六七八九十Oo○]+[年.-/][0-9一二两三四五六七八九十Oo]+[月.-/][0-9一二两三四五六七八九十Oo]+[号日.-/]'
    dateList = re.findall(mode, sentence1)
    sentence2 = sentence1
    if len(dateList):
        lastDate = dateList[len(dateList) - 1]
        try:
            lastDateIndex = sentence1.rindex(lastDate)
        except ValueError:
            lastDateIndex = 0
        try:
            index = sentence1.rindex(last)
        except ValueError:
            print(labels)
            print(sentence1)
            index = 0

        # 判断lastDate是不是在署名后面
        if index < lastDateIndex:
            sentence2 = sentence1[:lastDateIndex] + sentence1[lastDateIndex + len(lastDate):]

    # 在容忍区间中查找署名
    try:
        index = sentence2.rindex(last)
    except ValueError:
        index = 0
    if index + tolerant + len(last) >= len(sentence2):
        grade += 20
    return grade
