# -*-coding:UTF-8 -*-
from random import choice
import string
import hashlib
import os
import time
import smtplib
from datetime import datetime, timedelta
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .commands import getstatusoutput


def SendMail(mfrom, mto, mhost, mpasswd, msub="一封测试邮件", mcontent='test', cc=None, attachFile=None):
    msg = MIMEMultipart()
    EmailContent = MIMEText(mcontent, _subtype='html', _charset='utf-8')
    msg['Subject'] = "%s " % msub
    msg['From'] = mfrom
    if mto.find(',') == -1:
        msg['To'] = mto
    else:
        mto = mto.split(',')
        msg['To'] = ';'.join(mto)
    if cc is not None:
        if cc.find(',') == -1:
            msg['Cc'] = cc
        else:
            cc = cc.split(',')
            msg['Cc'] = ';'.join(cc)
    msg['date'] = time.strftime('%Y %H:%M:%S %z')
    try:
        if attachFile is not None:
            EmailContent = MIMEApplication(open(attachFile, 'rb').read())
            EmailContent["Content-Type"] = 'application/octet-stream'
            fileName = os.path.basename(attachFile)
            EmailContent["Content-Disposition"] = 'attachment; filename="%s"' % fileName
        msg.attach(EmailContent)
        smtp = smtplib.SMTP()
        smtp.connect(mhost)
        smtp.login(mfrom, mpasswd)
        smtp.sendmail(mfrom, mto, msg.as_string())
        smtp.quit()
    except Exception as e:
        print(e)


def radString(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


def rsync(sourceDir, destDir, exclude=None):
    if exclude:
        cmd = "rsync -au --delete {exclude} {sourceDir} {destDir}".format(sourceDir=sourceDir, destDir=destDir,
                                                                          exclude=exclude)
    else:
        cmd = "rsync -au --delete {sourceDir} {destDir}".format(sourceDir=sourceDir, destDir=destDir)
    return getstatusoutput(cmd)


def mkdir(dirPath):
    mkDir = "mkdir -p {dirPath}".format(dirPath=dirPath)
    return getstatusoutput(mkDir)


def cd(localDir):
    os.chdir(localDir)


def pwd():
    return os.getcwd()


def cmds(cmds):
    return getstatusoutput(cmds)


def chown(user, path):
    cmd = "chown -R {user}:{user} {path}".format(user=user, path=path)
    return getstatusoutput(cmd)


def makeToken(strs):
    m = hashlib.md5()
    m.update(strs.encode("utf8"))
    return m.hexdigest()


def lns(spath, dpath):
    if spath and dpath:
        rmLn = "rm -rf {dpath}".format(dpath=dpath)
        status, result = getstatusoutput(rmLn)
        mkLn = "ln -s {spath} {dpath}".format(spath=spath, dpath=dpath)
        return getstatusoutput(mkLn)
    else:
        return (1, "缺少路径")


def getDaysAgo(num):
    threeDayAgo = (datetime.now() - timedelta(days=num))
    timeStamp = int(time.mktime(threeDayAgo.timetuple()))
    otherStyleTime = threeDayAgo.strftime("%Y%m%d")
    return otherStyleTime
