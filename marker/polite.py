# -*- coding:utf8 -*-

# 礼貌得分
import re

def PoliteMark(sentence):
    grade = 0  # 得分
    # 文首部分
    prefix = ['尊敬', '敬爱', '亲爱']  # 敬语定语
    suffix = ['网友', '市民', '同志', '女士', '先生']  # 宾语
    for pre in prefix:
        if not grade == 0:
            break
        for suf in suffix:
            pat = pre + '[^,.，。、！？!?:;；：·~`~—]+' + suf  # 防止出现匹配到例如 " 亲爱的，你反映的网友问题...." 的内容
            m = re.match(pat, sentence)
            if not m == None:
                grade += 6
                break

    if '您好' in sentence or '你好' in sentence:
        grade += 6

    ni = sentence.count('你')
    nin = sentence.count('您')
    if ni < 3 and nin >= 2:
        grade += 10 - ni * 3
    return grade