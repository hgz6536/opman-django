# -*-coding:UTF-8 -*-
##################################################
#  _                     _
# | | ____ _  ___   __ _(_)_ __
# | |/ / _` |/ _ \ / _` | | '_ \
# |   < (_| | (_) | (_| | | | | |
# |_|\_\__,_|\___/ \__, |_|_| |_|
#                     |_|
##################################################
from openpyxl import load_workbook
from datetime import datetime


def getworktime(filename, username, workedate):
    workedate = datetime.strptime(str(workedate), '%Y-%m-%d').date()
    wb = load_workbook(filename=filename)
    ws = wb.get_sheet_by_name('Sheet 1')
    rows = ws.rows
    person_daka = []
    for row in rows:
        line = []
        for col in row:
            line.append(col.value)
            # line = [col.value for col in row]
        # print(line)
        try:
            daka_date = datetime.strptime(
                str(line[3]), '%Y-%m-%d %H:%M:%S.%f').date()
        except ValueError:
            daka_date = datetime.strptime(
                str(line[3]), '%Y-%m-%d %H:%M:%S').date()
        else:
            daka_date = datetime.strptime(
                str(line[3]), '%Y-%m-%d %H:%M:%S.%f').date()
        if daka_date == workedate:
            if line[1] == username:
                person_daka.append(line)
            else:
                pass
        else:
            pass
    # return person_daka
    jilu = []
    for i in person_daka:
        jilu.append(i[3])
    # print(jilu)
    return jilu


def twoandmore(mydate, firstime, lastime):
    flag1 = datetime.strptime(
        str(mydate) + ' 09:00:00', '%Y-%m-%d %H:%M:%S')
    flag2 = datetime.strptime(
        str(mydate) + ' 09:30:00', '%Y-%m-%d %H:%M:%S')
    flag3 = datetime.strptime(
        str(mydate) + ' 10:05:00', '%Y-%m-%d %H:%M:%S')
    flag4 = datetime.strptime(
        str(mydate) + ' 18:00:00', '%Y-%m-%d %H:%M:%S')
    flag5 = datetime.strptime(
        str(mydate) + ' 18:30:00', '%Y-%m-%d %H:%M:%S')
    flag6 = datetime.strptime(
        str(mydate) + ' 19:00:00', '%Y-%m-%d %H:%M:%S')
    flag7 = datetime.strptime(
        str(mydate) + ' 19:30:00', '%Y-%m-%d %H:%M:%S')
    flag8 = datetime.strptime(
        str(mydate) + ' 08:00:00', '%Y-%m-%d %H:%M:%S')
    flag9 = datetime.strptime(
        str(mydate) + ' 10:00:00', '%Y-%m-%d %H:%M:%S')
    if flag8 < firstime < flag1:
        print('早上9点之前来的哦,上班没有迟到，继续判断下班时间')
        late = None
        if lastime < flag4:
            print('早退了吗？计算早退时间')
            plus = None
            leave = flag4 - lastime
            return [firstime, lastime, late, plus, leave, '提前下班了，要请假的节奏']
        if flag4 < lastime < flag5:
            print('正常上下班')
            plus = None
            leave = None
            return [firstime, lastime, late, plus, leave, '正常上下班']

        if lastime > flag5:
            print('开始加班了吗？计算加班时间')
            overtime = lastime - flag5
            print('加班%s' % overtime)
            plus = overtime
            leave = None
            return [firstime, lastime, late, plus, leave, '加班']
    if flag1 < firstime < flag2:
        print('早上9点到9点半之间来的哦,上班没有迟到，继续判断下班时间')
        late = None
        if lastime < flag5:
            print('早退了吗？计算早退时间')
            plus = None
            leave = flag5 - lastime
            return [firstime, lastime, late, plus, leave, '提前下班了，要请假的节奏']
        if flag5 < lastime < flag6:
            print('正常上下班')
            plus = None
            leave = None
            return [firstime, lastime, late, plus, leave, '正常上下班']
        if lastime > flag6:
            print('开始加班了吗？计算加班时间')
            overtime = lastime - flag6
            print('加班%s' % overtime)
            plus = overtime
            leave = None
            return [firstime, lastime, late, plus, leave, '加班']
    if flag2 < firstime < flag3:
        print('早上9点半到10点之间来的哦,上班没有迟到，继续判断下班时间')
        late = None
        if lastime < flag6:
            print('早退了吗？计算早退时间')
            plus = None
            leave = flag6 - lastime
            return [firstime, lastime, late, plus, leave, '提前下班了，要请假的节奏']
        if flag6 < lastime < flag7:
            print('正常上下班')
            plus = None
            leave = None
            return [firstime, lastime, late, plus, leave, '正常上下班']
        if lastime > flag7:
            print('开始加班了吗？计算加班时间')
            overtime = lastime - flag7
            print('加班%s' % overtime)
            plus = overtime
            leave = None
            return [firstime, lastime, late, plus, leave, '加班']
    if firstime > flag3:
        print('10点之后来的哦，迟到了计算迟到时间')
        smtime = firstime - flag9
        late = smtime
        print('迟到%s,继续判断下班时间' % smtime)
        if lastime < flag6:
            print('早退了吗？计算早退时间')
            plus = None
            leave = flag6 - lastime
            return [firstime, lastime, late, plus, leave, '迟到+早退']
        if flag6 < lastime < flag7:
            print('下班时间ok')
            plus = None
            leave = None
            return [firstime, lastime, late, plus, leave, '只迟到了']
        if lastime > flag7:
            print('开始加班了吗？计算加班时间')
            overtime = lastime - flag7
            print('加班%s' % overtime)
            plus = overtime
            leave = None
            return [firstime, lastime, late, plus, leave, '迟到+加班']
