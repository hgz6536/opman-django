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
from .kaoqin import getworktime, twoandmore


class Analystor(object):
    """Statistics overtime hours during working days and holidays"""

    def __init__(self, mydate, filename, username, *args):
        super(Analystor, self).__init__()
        self.mydate = mydate
        self.filename = filename
        self.username = username
        self.nextday = datetime.strptime(
            self.mydate, '%Y-%m-%d').date() + timedelta(days=1)
        self.lst = getworktime(self.filename, self.username, self.nextday)
        self.args = getworktime(self.filename, self.username, self.mydate)
        self.myweek = datetime.strptime(self.mydate, '%Y-%m-%d').weekday()
        self.flag0 = datetime.strptime(
            str(self.nextday) + ' 08:00:00', '%Y-%m-%d %H:%M:%S')
        self.flag1 = datetime.strptime(
            str(self.mydate) + ' 09:00:00', '%Y-%m-%d %H:%M:%S')
        self.flag2 = datetime.strptime(
            str(self.mydate) + ' 09:30:00', '%Y-%m-%d %H:%M:%S')
        self.flag3 = datetime.strptime(
            str(self.mydate) + ' 10:00:00', '%Y-%m-%d %H:%M:%S')
        self.flag4 = datetime.strptime(
            str(self.mydate) + ' 18:00:00', '%Y-%m-%d %H:%M:%S')
        self.flag5 = datetime.strptime(
            str(self.mydate) + ' 18:30:00', '%Y-%m-%d %H:%M:%S')
        self.flag6 = datetime.strptime(
            str(self.mydate) + ' 19:00:00', '%Y-%m-%d %H:%M:%S')
        self.flag7 = datetime.strptime(
            str(self.mydate) + ' 19:30:00', '%Y-%m-%d %H:%M:%S')
        self.flag8 = datetime.strptime(
            str(self.mydate) + ' 08:00:00', '%Y-%m-%d %H:%M:%S')
        self.flag9 = datetime.strptime(
            str(self.mydate) + ' 10:05:00', '%Y-%m-%d %H:%M:%S')

    def is_WorkDay(self):
        if self.myweek in [5, 6]:
            # print('星期天')
            return False
        else:
            # print('工作日')
            return True

    def GetHours(self):

        if Analystor.is_WorkDay(self):
            print('torday is workday')
            if len(self.args) == 0:
                print(self.mydate + ':' + '全天请假')
                return {'username': self.username, 'on': None, 'off': None, 'late': None, 'plus': None, 'leave': '1天', 'content': None}
            if len(self.args) == 1:
                print('发现打卡一次')
                if self.args[0] < self.flag8:
                    print('此次为凌晨打卡，根据规定，凌晨打卡的加班时间算在了前一天的加班时间里，所以今天判断应该是休息了一天')
                    return {'username': self.username, 'on': None, 'off': None, 'late': None, 'plus': None, 'leave': '1天', 'content': '凌晨有1次打卡，判断昨天加班今天没上班'}
                else:
                    # 判断第二天凌晨是不是有打卡
                    if len(self.lst) != 0:
                        if heapq.nsmallest(1, self.lst)[0] < self.flag0:
                            print('次日凌晨有打卡，把加班时间累计在今天')
                            print(self.args[0])
                            '''
                             开始计算加班
                             先判断这次打卡时间属于哪个时间段，是9:00-18:00 还是 9:30-18:30 或者 10:00-19:00
                            '''
                            if self.args[0] < self.flag1:
                                print('早上9点之前来的哦')
                                overtime = heapq.nsmallest(1, self.lst)[
                                    0] - self.flag5
                                print('加班%s' % overtime)
                                return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst), 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                            if self.flag1 < self.args[0] < self.flag2:
                                print('9点到9点半之间来的哦')
                                overtime = heapq.nsmallest(1, self.lst)[
                                    0] - self.flag6
                                print('加班%s' % overtime)
                                return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst), 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                            if self.flag2 < self.args[0] < self.flag3:
                                print('9点半到10点之间来的哦')
                                overtime = heapq.nsmallest(1, self.lst)[
                                    0] - self.flag7
                                print('加班%s' % overtime)
                                return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst), 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                            if self.args[0] > self.flag9:
                                print('迟到了哦，开始计算迟到的时间：打卡时间-10:00:00')
                                smtime = self.args[
                                    0] - self.flag3
                                print('迟到%s' % smtime)
                                print('再算加班时间:次日凌晨时间-19:30:00')
                                overtime = heapq.nsmallest(1, self.lst)[
                                    0] - self.flag7
                                print('加班%s' % overtime)
                                return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst), 'late': smtime, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}

                    else:
                        print('次日凌晨没有打卡，判断为忘记打卡一次，有问题人工审核')
                        if self.args[0] < self.flag3:
                            print('次日凌晨没有打卡，也没发现迟到，判断为忘记打卡一次，有问题人工审核')
                            return {'username': self.username, 'on': self.args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡'}
                        else:
                            if self.args[0] > self.flag9:
                                smtime = self.args[
                                    0] - self.flag3
                                if smtime > timedelta(hours=3, minutes=0, seconds=0):
                                    print('此次打卡为下午，继续和19:00:00比较')
                                    return {'username': self.username, 'on': None, 'off': self.args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡'}
                                else:
                                    print('此次打卡为上午，应该是迟到了，计算迟到时间')
                                    chidao = self.args[
                                        0] - self.flag3
                                    print('迟到%s' % chidao)
                                    return {'username': self.username, 'on': self.args[0], 'off': None, 'late': chidao, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡并且上班迟到了'}

            if len(self.args) == 2:
                print('发现打卡2次')
                # 先判断下2次打卡的最小值，是不是有迟到情况
                firstime = heapq.nsmallest(1, self.args)[0]
                lastime = heapq.nlargest(1, self.args)[0]
                diff = lastime - firstime
                if diff < timedelta(hours=0, minutes=30, seconds=0):
                    print('两次打卡时间间隔在30分钟内，合并打卡记录')
                    self.args = heapq.nsmallest(1, self.args)
                    if heapq.nsmallest(1, self.lst)[0] < self.flag0:
                        print('次日凌晨有打卡，把加班时间累计在今天')
                        if self.args[0] < self.flag1:
                            print('早上9点之前来的哦')
                            overtime = heapq.nsmallest(1, self.lst)[
                                0] - self.flag5
                            print('加班%s' % overtime)
                            return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst)[0], 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if self.flag1 < self.args[0] < self.flag2:
                            print('9点到9点半之间来的哦')
                            overtime = heapq.nsmallest(1, self.lst)[
                                0] - self.flag6
                            print('加班%s' % overtime)
                            return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst)[0], 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if self.flag2 < self.args[0] < self.flag3:
                            print('9点半到10点之间来的哦')
                            overtime = heapq.nsmallest(1, self.lst)[
                                0] - self.flag7
                            print('加班%s' % overtime)
                            return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst)[0], 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if self.args[0] > self.flag9:
                            print('迟到了哦，开始计算迟到的时间：打卡时间-10:00:00')
                            smtime = self.args[0] - self.flag3
                            print('迟到%s' % smtime)
                            print('再算加班时间:次日凌晨时间-19:30:00')
                            overtime = heapq.nsmallest(1, self.lst)[
                                0] - self.flag7
                            print('加班%s' % overtime)
                            return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst)[0], 'late': smtime, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                    else:
                        print('次日凌晨没有打卡，判断为忘记打卡一次，有问题人工审核')
                        if self.args[0] < self.flag3:
                            print('次日凌晨没有打卡，也没发现迟到，判断为忘记打卡一次，有问题人工审核')
                            return {'username': self.username, 'on': self.args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡'}
                        else:
                            if self.args[0] > self.flag3:
                                smtime = self.args[0] - self.flag3
                                if smtime > timedelta(hours=3, minutes=0, seconds=0):
                                    print('此次打卡为下午，继续和19:00:00比较')
                                    if self.args[0] > self.flag6:
                                        print('下午没有早退')
                                        return {'username': self.username, 'on': None, 'off': self.args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡，人工审核'}
                                    else:
                                        print('可能早退了,人工审核')
                                        return {'username': self.username, 'on': None, 'off': self.args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡，人工审核'}
                                else:
                                    print('此次打卡为上午，应该是迟到了，计算迟到时间')
                                    chidao = self.args[0] - self.flag3
                                    print('迟到%s' % chidao)
                                    return {'username': self.username, 'on': self.args[0], 'off': None, 'late': chidao, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡，人工审核'}

                else:
                    if firstime < self.flag8:
                        print('当天有凌晨打卡记录,按规定凌晨的加班算在了前一天里，合并打卡记录')
                        self.args = heapq.nlargest(1, self.args)
                        if heapq.nsmallest(1, self.lst)[0] < self.flag0:
                            print('次日凌晨有打卡，把加班时间累计在今天')
                            if self.args[0] < self.flag1:
                                print('早上9点之前来的哦')
                                overtime = heapq.nsmallest(1, self.lst)[
                                    0] - self.flag5
                                print('加班%s' % overtime)
                                return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst)[0], 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                            if self.flag1 < self.args[0] < self.flag2:
                                print('9点到9点半之间来的哦')
                                overtime = heapq.nsmallest(1, self.lst)[
                                    0] - self.flag6
                                print('加班%s' % overtime)
                                return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst)[0], 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                            if self.flag2 < self.args[0] < self.flag3:
                                print('9点半到10点之间来的哦')
                                overtime = heapq.nsmallest(1, self.lst)[
                                    0] - self.flag7
                                print('加班%s' % overtime)
                                return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst)[0], 'late': None, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                            if self.args[0] > self.flag9:
                                print('迟到了哦，开始计算迟到的时间：打卡时间-10:00:00')
                                smtime = self.args[
                                    0] - self.flag3
                                print('迟到%s' % smtime)
                                print('再算加班时间:次日凌晨时间-19:30:00')
                                overtime = heapq.nsmallest(1, self.lst)[
                                    0] - self.flag7
                                print('加班%s' % overtime)
                                return {'username': self.username, 'on': self.args[0], 'off': heapq.nsmallest(1, self.lst)[0], 'late': smtime, 'plus': overtime, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        else:
                            print('次日凌晨没有打卡，判断为忘记打卡一次，有问题人工审核')
                            if self.args[0] < self.flag3:
                                print('次日凌晨没有打卡，也没发现迟到，判断为忘记打卡一次，有问题人工审核')
                                return {'username': self.username, 'on': self.args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡'}
                            else:
                                if self.args[0] > self.flag9:
                                    smtime = self.args[
                                        0] - self.flag3
                                    if smtime > timedelta(hours=3, minutes=0, seconds=0):
                                        print('此次打卡为下午，继续和19:00:00比较')
                                        if self.args[0] > self.flag6:
                                            print('下午没有早退')
                                            return {'username': self.username, 'on': None, 'off': self.args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡，人工审核'}
                                        else:
                                            print('可能早退了,人工审核')
                                            return {'username': self.username, 'on': None, 'off': self.args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡，人工审核'}
                                    else:
                                        print('此次打卡为上午，应该是迟到了，计算迟到时间')
                                        chidao = self.args[
                                            0] - self.flag3
                                        print('迟到%s' % chidao)
                                        return {'username': self.username, 'on': self.args[0], 'off': None, 'late': chidao, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡，人工审核'}
                                else:
                                    if self.args[0] < self.flag3:
                                        print('看起来没有迟到')
                                        return {'username': self.username, 'on': self.args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡，人工审核'}
                                    else:
                                        print('似乎迟到了，计算迟到时间')
                                        smtime = self.args[0] - self.flag3
                                        print('迟到%s' % smtime)
                                        return {'username': self.username, 'on': self.args[0], 'off': None, 'late': smtime, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡，人工审核'}
                    else:
                        firstime = heapq.nsmallest(1, self.args)[0]
                        lastime = heapq.nlargest(1, self.args)[0]
                        ll = twoandmore(self.mydate, firstime, lastime)
                        return {'username': self.username, 'on': ll[0], 'off': ll[1], 'late': ll[2], 'plus': ll[3], 'leave': ll[4], 'content': ll[5]}
            if len(self.args) >= 3:
                print('发现%d次打卡' % len(self.args))
                firstime = heapq.nsmallest(1, self.args)[0]
                lastime = heapq.nlargest(1, self.args)[0]
                ll = twoandmore(self.mydate, firstime, lastime)
                return {'username': self.username, 'on': ll[0], 'off': ll[1], 'late': ll[2], 'plus': ll[3], 'leave': ll[4], 'content': ll[5]}
        else:
            print('torday is sunday')
            if len(self.args) == 1:
                print('加班只打一次卡，人工审核')
                return {'username': self.username, 'on': self.args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '加班只打一次卡,人工审核'}
            if len(self.args) == 2:
                print('发现2次打卡，由于是星期天直接算加班时间')
                overtime = self.args[1] - self.args[0]
                print('加班%s' % overtime)
                return {'username': self.username, 'on': self.args[0], 'off': self.args[1], 'late': None, 'plus': overtime, 'leave': None, 'content': '假日加班'}
            if len(self.args) >= 3:
                firstime = heapq.nsmallest(1, self.args)[0]
                lastime = heapq.nlargest(1, self.args)[0]
                overtime = lastime - firstime
                return {'username': self.username, 'on': firstime, 'off': lastime, 'late': None, 'plus': overtime, 'leave': None, 'content': '假日加班'}
