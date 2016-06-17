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


def GetWorkTime(filename, username, workedate):
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
