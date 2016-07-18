#!/usr/bin/python
# coding = utf-8
# -*-coding:UTF-8 -*-
import requests
import json
from git import Repo, cmd, Git
from datetime import datetime, timedelta


def search_user(host, path, token, userinfo):
    url = 'http://' + host + path + 'users?private_token=' + \
          token + '&search=' + userinfo
    r = requests.get(url)
    r.encoding = 'utf-8'
    data = json.loads(r.text)
    for i in data[0]:
        if i == 'id':
            return data[0][i]


def gitlab_log(host, rootoken, proid, day):
    cdate = datetime.now() - timedelta(days=int(day))
    mydate = cdate.strftime("%Y-%m-%dT%H:%M:%SZ")
    path = '/api/v3/projects/' + str(proid) + '/repository/commits'
    url = 'http://' + host + path + \
        '?since=' + mydate + '&private_token=' + rootoken
    r = requests.get(url)
    r.encoding = 'utf-8'
    data = json.loads(r.text)
    return data


def all_user(host, path, token):
    url = 'http://' + host + path + 'users?private_token=' + token
    r = requests.get(url)
    r.encoding = 'utf-8'
    data = json.loads(r.text)
    print(data)


def all_projects(host, path, rootoken):
    url = 'http://' + host + path + 'projects/all?private_token=' + rootoken
    r = requests.get(url)
    r.encoding = 'utf-8'
    data = json.loads(r.text)
    pro_list = []
    for l in data:
        pro_dic = {}
        namespace = l['name_with_namespace'].split('/')
        owner = namespace[0]
        name = namespace[1]
        created_at = l['created_at']
        url = l['http_url_to_repo']
        id = l['id']
        log = gitlab_log(host, rootoken, id, '30')
        pro_dic = {'pro_owner': owner, 'pro_create_time': created_at,
                   'pro_name': name, 'pro_url': url, 'pro_id': id, 'pro_log':log}
        pro_list.append(pro_dic)
    return pro_list


def user_all_projects(host, path, usertoken):
    url = 'http://' + host + path + 'projects?private_token=' + usertoken
    r = requests.get(url)
    if r.status_code == 401:
        return "401 Unauthorized"
    else:
        r.encoding = 'utf-8'
        data = json.loads(r.text)
        pro_list = []
        for l in data:
            pro_dic = {}
            namespace = l['name_with_namespace'].split('/')
            owner = namespace[0]
            name = namespace[1]
            created_at = l['created_at']
            url = l['http_url_to_repo']
            id = l['id']
            log = gitlab_log(host, usertoken, id, '30')
            pro_dic = {'pro_owner': owner, 'pro_create_time': created_at,
                       'pro_name': name, 'pro_url': url, 'pro_id': id, 'pro_log':log}
            pro_list.append(pro_dic)
        return pro_list


def git_log(repopath):
    repo = Repo(repopath)
    ver = repo.iter_commits('master', max_count=50)
    commlist = []
    for i in ver:
        commdic = {}
        message = repo.commit(i).message.rstrip('\n')
        date = repo.commit(i).committed_date
        commdate = datetime.utcfromtimestamp(
            date).strftime("%Y-%m-%d %H:%M:%S")
        name = repo.commit(i).author
        commdic['message'] = message
        commdic['commdate'] = commdate
        commdic['name'] = str(name)
        commdic['id'] = str(i)
        commlist.append(commdic)
    return commlist
