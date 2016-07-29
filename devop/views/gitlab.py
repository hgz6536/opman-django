# -*-coding:UTF-8 -*-
import requests
import json
from datetime import datetime, timedelta


class Gitlab(object):
    """get some data from Gitlab"""

    def __init__(self, host, rootoken):
        super(Gitlab, self).__init__()
        self.host = host
        self.rootoken = rootoken

    def get_all_users(self):
        url = 'http://' + self.host + '/api/v3/users?private_token=' + self.rootoken
        r = requests.get(url)
        r.encoding = 'utf-8'
        data = json.loads(r.text)
        return data

    def get_all_projects(self):
        url = 'http://' + self.host + '/api/v3/projects/all?private_token=' + self.rootoken
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
            pro_dic = {'pro_owner': owner, 'pro_create_time': created_at,
                       'pro_name': name, 'pro_url': url, 'pro_id': id}
            pro_list.append(pro_dic)
        return pro_list

    def get_user_projects(self, usertoken):
        url = 'http://' + self.host + '/api/v3/projects?private_token=' + usertoken
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
                pro_dic = {'pro_owner': owner, 'pro_create_time': created_at,
                           'pro_name': name, 'pro_url': url, 'pro_id': id}
                pro_list.append(pro_dic)
        return pro_list

    def get_all_branches(self, pid):
        url = 'http://' + self.host + '/api/v3/projects/' + str(pid) + \
            '/repository/branches?private_token=' + self.rootoken
        r = requests.get(url)
        r.encoding = 'utf-8'
        data = json.loads(r.text)
        b_list = []
        for b in data:
            name = b['name']
            b_list.append(name)
        return b_list

    def get_commit_log(self, pid, ref_name=None, day=30):
        cdate = datetime.now() - timedelta(days=int(day))
        mydate = cdate.strftime("%Y-%m-%dT%H:%M:%SZ")
        if ref_name is None:
            url = 'http://' + self.host + '/api/v3/projects/' + \
                str(pid) + '/repository/commits?since=' + \
                mydate + '&private_token=' + self.rootoken
        else:
            url = 'http://' + self.host + '/api/v3/projects/' + \
                str(pid) + '/repository/commits?since=' + \
                mydate + '&ref_name=' + ref_name + '&private_token =' + self.rootoken
        r = requests.get(url)
        r.encoding = 'utf-8'
        data = json.loads(r.text)
        return data
