# docker deploy - 容器部署方式

**公共镜像地址：** registry.cn-shenzhen.aliyuncs.com/itcp/opman-docker:latest

- **创建容器**

`docker pull registry.cn-shenzhen.aliyuncs.com/itcp/opman-docker:latest`

在宿主机准备好 /docker_storage 这样的目录作数据卷挂载

`docker run -dit --name=opman -p 8010:80 -p 8080:8000 -v /docker_storage/opman:/storage registry.cn-shenzhen.aliyuncs.com/itcp/opman-docker:latest /usr/sbin/init`

- **进入容器配置**

`docker exec -it opman /bin/bash`

查看内部的环境说明

`cat /root/doc.txt`

检查环境

`/usr/local/nginx/sbin/nginx -h`
`python3 -h`
`pip3 -h`
`uwsgi -h`

创建存放访问日志的目录，以便宿主机外面可以直接查看

`mkdir -p /storage/nginxlog`


- **配置负载均衡，反向代理**

转发到容器(如果你的主机只跑这opman cmdb，那就把宿主机80端口直接映射到容器的80，就不用转发了)

vi /etc/nginx/conf/vhost/opman.conf
```
server {
    listen 80;
    server_name opman.xxx.com;
    charset utf8;

    location / {
        proxy_pass http://0.0.0.0:8010/;
        proxy_set_header  X-Forwarded-For $remote_addr;
        proxy_set_header  X-Forwarded-Host $server_name;
        proxy_set_header Host $host;
    }
}

```

----
