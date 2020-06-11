# -*- coding:utf8 -*-
# 答复日期评分
import datetime
import re


# 统一日期格式
def unify(date):
    date2 = date.replace(' ', '')
    date2 = date2.replace('-', '.')
    date2 = date2.replace('—', '.')
    date2 = date2.replace('/', '.')
    date2 = date2.replace('年', '.')
    date2 = date2.replace('月', '.')
    date2 = date2.replace('日', '.')
    year = ''
    month = ''
    day = ''
    try:
        chinese_english = dict(零=0, 一=1, 二=2, 三=3, 四=4, 五=5, 六=6, 七=7, 八=8, 九=9, 十=10, O=0, o=0)
        chinese_english.update(
            {'〇': 0, '○': 0, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9})
        year = date2.split('.')[0]
        month = date2.split(".")[1]
        day = date2.split(".")[2]

        m = re.match('[0-9零一二两三四五六七八九十〇Oo]{4}', year)
        if not m == None:
            year = "".join(str(chinese_english[i]) for i in year)

        m = re.match('[一二两三四五六七八九十]{1,2}', month)
        if not m == None:
            month = "".join(str(chinese_english[i]) for i in month)
            if len(month) >= 3:
                month = month[0] + month[2]

        m = re.match('[一二两三四五六七八九十]{1,3}', day)
        if not m == None:
            if len(day) >= 3:
                day = day[0] + day[2]
            day = "".join(str(chinese_english[i]) for i in day)
            if len(day) == 3:
                day = day[0] + day[2]
    except Exception:
        pass
    finally:
        final_date = year + "年" + month + "月" + day + "日"
        return final_date


def ReplyDate(sentence):
    grade = 20
    tolerant = 7  # 容许文本最后有几个字符
    mode = '[0-9零一二两三四五六七八九十〇Oo○][0-9零二一两三四五六七八九十〇Oo○]{3,4}[年\.\-/]' \
           '[0-9一二两三四五六七八九十〇Oo ]{1,2}[月\.\-/][0-9一二两三四五六七八九十〇Oo ]{1,3}[号日\.\-/]?'
    mode1 = '[0-9]{4}年[0-9]+月[0-9]+[号日]'
    mode2 = '[零一二两三四五六七八九十〇Oo○]{4}[年][一二两三四五六七八九十〇Oo]+[月]' \
            '[一二两三四五六七八九十〇Oo]+[号日]'
    mode3 = '[0-9]{4}[\.\-/][0-9]+[\.\-/][0-9]+'
    dateList = re.findall(mode, sentence)

    if len(dateList) == 0:
        # 没有匹配到日期
        return 0
    last = len(dateList) - 1
    last = dateList[last]  # 最后出现的日期
    try:
        if sentence.rindex(last) + len(last) + tolerant >= len(sentence):  # 最后一个日期出现的位置在文本最后容错区域内即认为是答复日期

            # 将三种用类似O的表示转化为零
            last = str(last).replace('o', '零')
            last = str(last).replace('○', '零')
            last = str(last).replace('O', '零')
            # print(sentence)
            # 检测日期格式是否统一
            m1 = re.match(mode1, last)
            m2 = re.match(mode2, last)
            m3 = re.match(mode3, last)
            if m1 == None and m2 == None and m3 == None:
                # 日期不统一则扣分
                grade -= 10
            last = unify(last)  # 统一格式供检测日期是否存在

            # 日期是否存在
            date_p = datetime.datetime.strptime(last, '%Y年%m月%d日').date()
        else:
            return 0
    except ValueError:
        return 0
    return grade
