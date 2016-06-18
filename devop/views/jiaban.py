# -*-coding:UTF-8 -*-
###########################################
#    _ _       _
#   (_|_) __ _| |__   __ _ _ __
#   | | |/ _` | '_ \ / _` | '_ \
#   | | | (_| | |_) | (_| | | | |
#  _/ |_|\__,_|_.__/ \__,_|_| |_|
# |__/
###########################################

from datetime import datetime, timedelta
import heapq
from devop.views.kaoqin import getworktime


class Analystor(object):
    """Statistics overtime hours during working days and holidays"""

    def __init__(self, mydate, filename, username, *args):
        super(Analystor, self).__init__()
        self.mydate = mydate
        self.filename = filename
        self.username = username
        self.args = getworktime(self.filename, self.username, self.mydate)
        self.myweek = datetime.strptime(self.mydate, '%Y-%m-%d').weekday()

    def is_workday(self):
        if self.myweek in [5, 6]:
            # print('星期天')
            return False
        else:
            # print('工作日')
            return True

    def gethours(self):
        if Analystor.is_workday(self):
            print('torday is workday')
            if len(self.args) == 0:
                print(self.mydate + ':' + '全天请假')
            if len(self.args) == 1:
                print('发现打卡一次')
                # 判断第二天凌晨是不是有打卡
                nextday = datetime.strptime(
                    self.mydate, '%Y-%m-%d').date() + timedelta(days=1)
                lst = getworktime(self.filename, self.username, nextday)
                flag0 = datetime.strptime(
                    str(nextday) + ' 08:00:00', '%Y-%m-%d %H:%M:%S')
                if heapq.nsmallest(1, lst)[0] < flag0:
                    print('次日凌晨有打卡，把加班时间累计在今天')
                    print(self.args[0])
                    '''
                    # 开始计算加班
                    # 先判断这次打卡时间属于哪个时间段，是9:00-18:00 还是 9:30-18:30 或者 10:00-19:00
                    '''
                    flag1 = datetime.strptime(
                        str(self.mydate) + ' 09:00:00', '%Y-%m-%d %H:%M:%S')
                    flag2 = datetime.strptime(
                        str(self.mydate) + ' 09:30:00', '%Y-%m-%d %H:%M:%S')
                    flag3 = datetime.strptime(
                        str(self.mydate) + ' 10:00:00', '%Y-%m-%d %H:%M:%S')
                    if self.args[0] < flag1:
                        print('早上9点之前来的哦')
                        overtime = heapq.nsmallest(
                            1, lst)[0] - datetime.strptime(str(self.mydate) + ' 18:30:00', '%Y-%m-%d %H:%M:%S')
                        print(overtime)
                    if flag1 < self.args[0] < flag2:
                        print('9点到9点半之间来的哦')
                        overtime = heapq.nsmallest(1, lst)[
                                       0] - datetime.strptime(str(self.mydate) + ' 19:00:00', '%Y-%m-%d %H:%M:%S')
                        print(overtime)
                    if flag2 < self.args[0] < flag3:
                        print('9点半到10点之间来的哦')
                        overtime = heapq.nsmallest(1, lst)[
                                       0] - datetime.strptime(str(self.mydate) + ' 19:30:00', '%Y-%m-%d %H:%M:%S')

                    if self.args[0] > flag3:
                        print('迟到了哦，开始计算迟到的时间')
                        print('开始查找下班时间')
                        pass
                        smtime = self.args[
                                     0] - datetime.strptime(str(self.mydate) + ' 10:00:00', '%Y-%m-%d %H:%M:%S')
                        print(smtime)

                else:
                    print('凌晨没有打卡，武断的判断为忘记打卡一次')

            else:
                print('忘记打卡了')
        else:
            print('torday is sunday')
