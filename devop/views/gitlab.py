#!/usr/bin/python
# coding = utf-8
# -*-coding:UTF-8 -*-
import requests
import json


def search_user(host, path, token, userinfo):
    url = 'http://' + host + path + 'users?private_token=' + \
        token + '&search=' + userinfo
    r = requests.get(url)
    r.encoding = 'utf-8'
    data = json.loads(r.text)
    for i in data[0]:
        if i == 'id':
            return data[0][i]


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
    pro_dic = {}
    for l in data:
        for m in l:
            namespace = l['name_with_namespace'].split('/')
            owner = namespace[0]
            name = namespace[1]
            created_at = l['created_at']
            url = l['http_url_to_repo']
            pro_dic = {'pro_owner': owner, 'pro_create_time': created_at,
                       'pro_name': name, 'pro_url': url}
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
        pro_dic = {}
        for l in data:
            for m in l:
                namespace = l['name_with_namespace'].split('/')
                owner = namespace[0]
                name = namespace[1]
                created_at = l['created_at']
                url = l['http_url_to_repo']
                pro_dic = {'pro_owner': owner, 'pro_create_time': created_at,
                           'pro_name': name, 'pro_url': url}
            pro_list.append(pro_dic)
        return pro_list