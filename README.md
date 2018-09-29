# OpMan2.0

## 运行环境介绍 ##

系统：Mac

软件：Python3.6,Django1.11.3,MySQL5.7

注意：此项目尚未开发完整,尚不能部署线上使用,仅供学习,弱要看效果修改setting文件改成debug模式直接run起来就行,忽略下面的ngx配置(高手可无视)

docker容器镜像部署： 请查看docker_deploy.md 文档发说明

## 全新UI ##

![](https://github.com/hgz6536/hgz6536.github.io/blob/master/images/OpMan2.0.png)

## 部署方法 ##

- 创建uwsgi,nginx进程运行的用户

`useradd opman`

- 安装MySQL5.7,并设置my.cnf

`character-set-server = utf8`

`character-set-client-handshake = FALSE`

`sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER`

- 登录MySQL,并授权项目账号

`GRANT ALL PRIVILEGES ON devop.* TO dbuser_op@'%' IDENTIFIED BY 'devop@2015***';`

- MySQL连接配置在opman-django/devop/settings.py

`DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'devop',
        'USER': 'dbuser_op',
        'PASSWORD': 'devop@2015***',
        'HOST': 'localhost',
        'PORT': '',
    }
}`

- 安装Redis

`https://niubilety.com/redis%E5%85%A5%E9%97%A8%E4%B8%80/`

- 执行ansible如果用密码的方式需要安装sshpass 命令

`yum install sshpass -y`

- 克隆代码

`cd /data/webroot`

`git clone https://github.com/hgz6536/opman-django.git`

`cd opman-django && pip3 install -r requirements.txt`

- 初始化项目

`python manage.py makemigrations opman`

`python manage.py migrate`

`python manage.py createsuperuser`

- 导入样例数据

`python manage.py loaddata initdb/opman.json`

- 启动celery worker进程

`/usr/bin/python manage.py celery worker --loglevel=info -E -c 2 &`

- 安装uwsgi

`pip3 install uwsgi`

- nginx配置文件

upstream opman {

        server 127.0.0.1:8000;
}

server {

        listen 80;
        server_name opman.niubilety.com
        charset utf-8;

        gzip on;
        gzip_min_length 1000;
        gzip_buffers 4 16k;
        gzip_http_version 1.1;
        gzip_comp_level 3;
        gzip_vary on;

        client_max_body_size 8M;

        #access_log /data/logs/nginx/opman_access.log;
        #error_log /data/logs/nginx/opman_error.log;

        location /medis {
                alias /data/webroot/opman-django/media;
        }

        location /static {
                alias /data/webroot/opman-django/static;
        }

        location / {
                uwsgi_pass opman;
                include /etc/nginx/uwsgi_params;
        }

}

- 启动uwsgi

`uwsgi --ini /data/webroot/opman-django/uwsgi.ini`

- 平滑重启uwsgi

`uwsgi --reload /tmp/opman.pid`

- 启动nginx

`/etc/init.d/nginx start`

\** 要注意的
如果前端的图标访问不了，只需要在nginx配置 /static/ 路径中加入如下参数 
```
        add_header Access-Control-Allow-Origin opman.itcp.cc;
        add_header Access-Control-Allow-Credentials 'true';
        add_header Access-Control-Allow-Headers X-Requested-With;
        add_header Access-Control-Allow-Methods GET,POST,OPTIONS;
```

## 本项目交流群 ##
`580838402`

如果困惑直击QQ
<a target="_blank" href="http://wpa.qq.com/msgrd?v=3&uin=847644968&site=qq&menu=yes">
     <img border="0" src="http://wpa.qq.com/pa?p=2:847644968:52" alt="点击这里给我发消息" title="点击这里给我发消息"/>
</a>


## 扫个红包以表支持 ##

![](https://github.com/hgz6536/hgz6536.github.io/blob/master/images/hongbao.jpg)

## 土豪可直接现金支持 ##

![](https://github.com/hgz6536/hgz6536.github.io/blob/master/images/zhifubao.jpg)
