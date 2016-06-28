# -*-coding:UTF--
from .analystor import getalldate, gethours, getworktime
from datetime import datetime, timedelta
from openpyxl import load_workbook

wb = load_workbook(filename='/root/kq.xlsx')
ws = wb.get_sheet_by_name('Sheet 1')
rows = ws.rows
alldata = []
for row in rows:
    line = [col.value for col in row]
    alldata.append(line)

datelist = getalldate(2016, 5)
userlist = ['余凌燕']
for user in userlist:
    for date in datelist:
        nextday = datetime.strptime(
            date, '%Y-%m-%d').date() + timedelta(days=1)
        # print(date + user)
        jilu = getworktime(user, date, alldata)
        jilu1 = getworktime(user, nextday, alldata)
        a = gethours(user, date, jilu1, jilu)
        print(a)
