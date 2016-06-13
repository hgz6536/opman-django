# opman

## 运行环境介绍 ##

系统：KaLi 2016

软件：Python3.5,Django1.9

## 项目还在进行中 ##

从今以后会把项目的进度，已经有什么样的功能会一一列出来

## 当前功能 ##

用户权限管理已经完成,released v1.0

## 结果展示 ##
###编辑用户###
![](https://github.com/hgz6536/hgz6536.github.io/blob/master/images/EditPermission.png)
###当用户访问/user/add时就会出现以下界面###
![](https://github.com/hgz6536/hgz6536.github.io/blob/master/images/DenyUrl.png)
###实现了组【部门或者角色】的权限管理###
不展示图片了,和上面的用户类似的页面,当用户没有/user/add 权限时,如果其所在的组有这个url的权限也是可以访问的,用户权限只是让权限粒度更小，从而更灵活.