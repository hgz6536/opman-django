# -*-coding:UTF-8 -*-
from datetime import datetime, timedelta
import calendar
import heapq


def is_workday(mydate):
    myweek = datetime.strptime(mydate, '%Y-%m-%d').weekday()
    if myweek in [5, 6]:
        return False
    else:
        return True


def getalldate(year, month):
    lst = []
    pre = calendar.monthrange(year, month)[1]
    for i in range(1, pre + 1):
        lst.append(str(year) + '-' + str(month) + '-' + str(i))
    return lst


def getworktime(username, workedate, args):
    workedate = datetime.strptime(str(workedate), '%Y-%m-%d').date()
    person_daka = []
    for line in args:
        if line[1] == username:
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
                person_daka.append(line)
            else:
                pass
        else:
            pass
    jilu = []
    for i in person_daka:
        jilu.append(i[3])
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
            return [firstime, lastime, late, plus, leave.seconds, '提前下班了，要请假的节奏']
        if flag4 < lastime < flag5:
            print('正常上下班')
            plus = None
            leave = None
            return [firstime, lastime, late, plus, leave, '正常上下班']

        if lastime > flag5:
            print('开始加班了吗？计算加班时间')
            overtime = lastime - flag5
            print('加班%s' % overtime)
            plus = overtime.seconds
            leave = None
            return [firstime, lastime, late, plus, leave, '加班']
    if flag1 < firstime < flag2:
        print('早上9点到9点半之间来的哦,上班没有迟到，继续判断下班时间')
        late = None
        if lastime < flag5:
            print('早退了吗？计算早退时间')
            plus = None
            leave = flag5 - lastime
            return [firstime, lastime, late, plus, leave.seconds, '提前下班了，要请假的节奏']
        if flag5 < lastime < flag6:
            print('正常上下班')
            plus = None
            leave = None
            return [firstime, lastime, late, plus, leave, '正常上下班']
        if lastime > flag6:
            print('开始加班了吗？计算加班时间')
            overtime = lastime - flag6
            print('加班%s' % overtime)
            plus = overtime.seconds
            leave = None
            return [firstime, lastime, late, plus, leave, '加班']
    if flag2 < firstime < flag3:
        print('早上9点半到10点之间来的哦,上班没有迟到，继续判断下班时间')
        late = None
        if lastime < flag6:
            print('早退了吗？计算早退时间')
            plus = None
            leave = flag6 - lastime
            return [firstime, lastime, late, plus, leave.seconds, '提前下班了，要请假的节奏']
        if flag6 < lastime < flag7:
            print('正常上下班')
            plus = None
            leave = None
            return [firstime, lastime, late, plus, leave, '正常上下班']
        if lastime > flag7:
            print('开始加班了吗？计算加班时间')
            overtime = lastime - flag7
            print('加班%s' % overtime)
            plus = overtime.seconds
            leave = None
            return [firstime, lastime, late, plus, leave, '加班']
    if firstime > flag3:
        print('10点之后来的哦，迟到了计算迟到时间')
        smtime = firstime - flag9
        late = smtime.seconds
        print('迟到%s,继续判断下班时间' % smtime)
        if lastime < flag6:
            print('早退了吗？计算早退时间')
            plus = None
            leave = flag6 - lastime
            return [firstime, lastime, late, plus, leave.seconds, '迟到+早退']
        if flag6 < lastime < flag7:
            print('下班时间ok')
            plus = None
            leave = None
            return [firstime, lastime, late, plus, leave, '只迟到了']
        if lastime > flag7:
            print('开始加班了吗？计算加班时间')
            overtime = lastime - flag7
            print('加班%s' % overtime)
            plus = overtime.seconds
            leave = None
            return [firstime, lastime, late, plus, leave, '迟到+加班']


def gethours(username, mydate, lst, args):
    nextday = datetime.strptime(mydate, '%Y-%m-%d').date() + timedelta(days=1)
    flag0 = datetime.strptime(
        str(nextday) + ' 08:00:00', '%Y-%m-%d %H:%M:%S')
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

    if is_workday(mydate):
        print('%s is workday' % mydate)
        if len(args) == 0:
            print(mydate + ':' + '全天请假')
            return {'username': username, 'date':mydate, 'on': None, 'off': None, 'late': None, 'plus': None, 'leave': 86400, 'content': '全天请假'}
        if len(args) == 1:
            print('发现打卡一次')
            if args[0] < flag8:
                print('此次为凌晨打卡，根据规定，凌晨打卡的加班时间算在了前一天的加班时间里，所以今天判断应该是休息了一天')
                return {'username': username, 'date':mydate, 'on': None, 'off': None, 'late': None, 'plus': None, 'leave': 86400, 'content': '凌晨有1次打卡，判断昨天加班今天没上班'}
            else:
                # 判断第二天凌晨是不是有打卡
                if len(lst) != 0:
                    if heapq.nsmallest(1, lst)[0] < flag0:
                        print('次日凌晨有打卡，把加班时间累计在今天')
                        print(args[0])
                        '''
                        开始计算加班
                        先判断这次打卡时间属于哪个时间段，是9:00-18:00 还是 9:30-18:30 或者 10:00-19:00
                        '''
                        if args[0] < flag1:
                            print('早上9点之前来的哦')
                            overtime = heapq.nsmallest(1, lst)[0] - flag5
                            print('加班%s' % overtime)
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst), 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if flag1 < args[0] < flag2:
                            print('9点到9点半之间来的哦')
                            overtime = heapq.nsmallest(1, lst)[0] - flag6
                            print('加班%s' % overtime)
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst), 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if flag2 < args[0] < flag3:
                            print('9点半到10点之间来的哦')
                            overtime = heapq.nsmallest(1, lst)[0] - flag7
                            print('加班%s' % overtime)
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst), 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if args[0] > flag9:
                            print('迟到了哦，开始计算迟到的时间：打卡时间-10:00:00')
                            smtime = args[0] - flag3
                            print('迟到%s' % smtime)
                            print('再算加班时间:次日凌晨时间-19:30:00')
                            overtime = heapq.nsmallest(1, lst)[0] - flag7
                            print('加班%s' % overtime)
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst), 'late': smtime.seconds, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                else:
                    print('次日凌晨没有打卡，判断为忘记打卡一次，有问题人工审核')
                    if args[0] < flag3:
                        print('次日凌晨没有打卡，也没发现迟到，判断为忘记打卡一次，有问题人工审核')
                        return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡'}
                    else:
                        if args[0] > flag9:
                            smtime = args[0] - flag3
                            if smtime > timedelta(hours=3, minutes=0, seconds=0):
                                print('此次打卡为下午，继续和19:00:00比较')
                                return {'username': username, 'date':mydate, 'on': None, 'off': args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡'}
                            else:
                                print('此次打卡为上午，应该是迟到了，计算迟到时间')
                                chidao = args[0] - flag3
                                print('迟到%s' % chidao)
                                return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': chidao.seconds, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡并且上班迟到了'}
        if len(args) == 2:
            print('发现打卡2次')
            # 先判断下2次打卡的最小值，是不是有迟到情况
            firstime = heapq.nsmallest(1, args)[0]
            lastime = heapq.nlargest(1, args)[0]
            diff = lastime - firstime
            if diff < timedelta(hours=0, minutes=30, seconds=0):
                print('两次打卡时间间隔在30分钟内，合并打卡记录')
                args = heapq.nsmallest(1, args)
                if heapq.nsmallest(1, lst)[0] < flag0:
                    print('次日凌晨有打卡，把加班时间累计在今天')
                    if args[0] < flag1:
                        print('早上9点之前来的哦')
                        overtime = heapq.nsmallest(1, lst)[0] - flag5
                        print('加班%s' % overtime)
                        return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst)[0], 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                    if flag1 < args[0] < flag2:
                        print('9点到9点半之间来的哦')
                        overtime = heapq.nsmallest(1, lst)[0] - flag6
                        print('加班%s' % overtime)
                        return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst)[0], 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                    if flag2 < args[0] < flag3:
                        print('9点半到10点之间来的哦')
                        overtime = heapq.nsmallest(1, lst)[0] - flag7
                        print('加班%s' % overtime)
                        return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst)[0], 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                    if args[0] > flag9:
                        print('迟到了哦，开始计算迟到的时间：打卡时间-10:00:00')
                        smtime = args[0] - flag3
                        print('迟到%s' % smtime)
                        print('再算加班时间:次日凌晨时间-19:30:00')
                        overtime = heapq.nsmallest(1, lst)[0] - flag7
                        print('加班%s' % overtime)
                        return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst)[0], 'late': smtime.seconds, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                else:
                    print('次日凌晨没有打卡，判断为忘记打卡一次，有问题人工审核')
                    if args[0] < flag3:
                        print('次日凌晨没有打卡，也没发现迟到，判断为忘记打卡一次，有问题人工审核')
                        return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡'}
                    else:
                        if args[0] > flag3:
                            smtime = args[0] - flag3
                            if smtime > timedelta(hours=3, minutes=0, seconds=0):
                                print('此次打卡为下午，继续和19:00:00比较')
                                if args[0] > flag6:
                                    print('下午没有早退')
                                    return {'username': username, 'date':mydate, 'on': None, 'off': args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡，人工审核'}
                                else:
                                    print('可能早退了,人工审核')
                                    return {'username': username, 'date':mydate, 'on': None, 'off': args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡，人工审核'}
                            else:
                                print('此次打卡为上午，应该是迟到了，计算迟到时间')
                                chidao = args[0] - flag3
                                print('迟到%s' % chidao)
                                return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': chidao.seconds, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡，人工审核'}
            else:
                if firstime < flag8:
                    print('当天有凌晨打卡记录,按规定凌晨的加班算在了前一天里，合并打卡记录')
                    args = heapq.nlargest(1, args)
                    if heapq.nsmallest(1, lst)[0] < flag0:
                        print('次日凌晨有打卡，把加班时间累计在今天')
                        if args[0] < flag1:
                            print('早上9点之前来的哦')
                            overtime = heapq.nsmallest(1, lst)[0] - flag5
                            print('加班%s' % overtime)
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst)[0], 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if flag1 < args[0] < flag2:
                            print('9点到9点半之间来的哦')
                            overtime = heapq.nsmallest(1, lst)[0] - flag6
                            print('加班%s' % overtime)
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst)[0], 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if flag2 < args[0] < flag3:
                            print('9点半到10点之间来的哦')
                            overtime = heapq.nsmallest(1, lst)[0] - flag7
                            print('加班%s' % overtime)
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst)[0], 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                        if args[0] > flag9:
                            print('迟到了哦，开始计算迟到的时间：打卡时间-10:00:00')
                            smtime = args[0] - flag3
                            print('迟到%s' % smtime)
                            print('再算加班时间:次日凌晨时间-19:30:00')
                            overtime = heapq.nsmallest(1, lst)[0] - flag7
                            print('加班%s' % overtime)
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': heapq.nsmallest(1, lst)[0], 'late': smtime.seconds, 'plus': overtime.seconds, 'leave': None, 'content': '次日凌晨加班时间累计到今天'}
                    else:
                        print('次日凌晨没有打卡，判断为忘记打卡一次，有问题人工审核')
                        if args[0] < flag3:
                            print('次日凌晨没有打卡，也没发现迟到，判断为忘记打卡一次，有问题人工审核')
                            return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡'}
                        else:
                            if args[0] > flag9:
                                smtime = args[0] - flag3
                                if smtime > timedelta(hours=3, minutes=0, seconds=0):
                                    print('此次打卡为下午，继续和19:00:00比较')
                                    if args[0] > flag6:
                                        print('下午没有早退')
                                        return {'username': username, 'date':mydate, 'on': None, 'off': args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡，人工审核'}
                                    else:
                                        print('可能早退了,人工审核')
                                        return {'username': username, 'date':mydate, 'on': None, 'off': args[0], 'late': None, 'plus': None, 'leave': None, 'content': '判断为上班忘记打卡，人工审核'}
                                else:
                                    print('此次打卡为上午，应该是迟到了，计算迟到时间')
                                    chidao = args[0] - flag3
                                    print('迟到%s' % chidao)
                                    return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': chidao.seconds, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡，人工审核'}
                            else:
                                if args[0] < flag3:
                                    print('看起来没有迟到')
                                    return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡，人工审核'}
                                else:
                                    print('似乎迟到了，计算迟到时间')
                                    smtime = args[0] - flag3
                                    print('迟到%s' % smtime)
                                    return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': smtime.seconds, 'plus': None, 'leave': None, 'content': '判断为下班忘记打卡，人工审核'}
                else:
                    firstime = heapq.nsmallest(1, args)[0]
                    lastime = heapq.nlargest(1, args)[0]
                    ll = twoandmore(mydate, firstime, lastime)
                    return {'username': username, 'date':mydate, 'on': ll[0], 'off': ll[1], 'late': ll[2], 'plus': ll[3], 'leave': ll[4], 'content': ll[5]}
        if len(args) >= 3:
            print('发现%d次打卡' % len(args))
            firstime = heapq.nsmallest(1, args)[0]
            lastime = heapq.nlargest(1, args)[0]
            ll = twoandmore(mydate, firstime, lastime)
            return {'username': username, 'date':mydate, 'on': ll[0], 'off': ll[1], 'late': ll[2], 'plus': ll[3], 'leave': ll[4], 'content': ll[5]}
    else:
        print('%s is sunday' % mydate)
        if len(args) == 1:
            print('加班只打一次卡，人工审核')
            return {'username': username, 'date':mydate, 'on': args[0], 'off': None, 'late': None, 'plus': None, 'leave': None, 'content': '加班只打一次卡,人工审核'}
        if len(args) == 2:
            print('发现2次打卡，由于是星期天直接算加班时间')
            overtime = args[1] - args[0]
            print('加班%s' % overtime)
            return {'username': username, 'date':mydate, 'on': args[0], 'off': args[1], 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '假日加班'}
        if len(args) >= 3:
            firstime = heapq.nsmallest(1, args)[0]
            lastime = heapq.nlargest(1, args)[0]
            overtime = lastime - firstime
            return {'username': username, 'date':mydate, 'on': firstime, 'off': lastime, 'late': None, 'plus': overtime.seconds, 'leave': None, 'content': '假日加班'}
