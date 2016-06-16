# -*-coding:UTF-8 -*-
from openpyxl import load_workbook
from datetime import datetime
import heapq


def GetWorkTime(filename, username, workedate):
    workedate = datetime.strptime(workedate, '%Y-%m-%d').date()
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

    if len(jilu) > 2:
        print(u'有重复打卡')
        # print(jilu)
        # 接下来判断jilu 列表里的数据的最大值和最小值
        on_worke_time = heapq.nsmallest(1, jilu)
        off_worker_time = heapq.nlargest(1, jilu)
        print('上班时间：%s，下班时间：%s' % (on_worke_time[0], off_worker_time[0]))
    if len(jilu) == 2:
        print(u'正常打卡')
        on_worke_time = jilu[0]
        off_worker_time = jilu[1]
        print('上班时间：%s，下班时间：%s' % (on_worke_time[0], off_worker_time[0]))
    if len(jilu) == 1:
        print(u'忘记打卡一次')
        on_worke_time = jilu[0]
        off_worker_time = None
        print('上班时间：%s，下班时间：%s' % (on_worke_time[0], off_worker_time))
    if len(jilu) == 0:
        print(u'没来上班！')
        on_worke_time = None
        off_worker_time = None
        print('上班时间：%s，下班时间：%s' % (on_worke_time, off_worker_time))
if __name__ == '__main__':
    ls = GetWorkTime('/root/kq.xlsx', u'董志成', '2016-5-6')
    # print(ls)
