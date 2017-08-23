#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User, Group, Permission
from opman.models import MyUser as User
from opman.models import RoleList, PermissonList
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from opman.models import Project_Order


@login_required()
def user_manage(request):
    if request.method == "GET":
        userList = User.objects.all()
        roleList = RoleList.objects.all()
        permissionList = PermissonList.objects.all()
        return render(request, 'users/user_manage.html',
                      {"user": request.user, "userList": userList, "groupList": roleList,
                       "permissionList": permissionList})


def register(request):
    if request.method == "POST":
        if request.POST.get('password') == request.POST.get('c_password'):
            try:
                user = User.objects.filter(username=request.POST.get('username'))
                if len(user) > 0:
                    return JsonResponse({"code": 500, "data": None, "msg": "注册失败，用户已经存在。"})
                else:
                    user = User()
                    if request.POST.get('rolename'):
                        user.role = RoleList.objects.get(name=request.POST.get('rolename'))
                    else:
                        user.role = RoleList.objects.get(name='运维')
                    user.username = request.POST.get('username')
                    user.email = request.POST.get('email')
                    user.is_staff = 0
                    user.is_active = 0
                    user.is_superuser = 0
                    user.set_password(request.POST.get('password'))
                    user.save()
                    return JsonResponse({"code": 200, "data": None, "msg": "用户注册成功"})
            except Exception as e:
                print(e)
                return JsonResponse({"code": 500, "data": None, "msg": "用户注册失败"})
        else:
            return JsonResponse({"code": 500, "data": None, "msg": "密码不一致，用户注册失败。"})


@login_required()
def user_center(request):
    if request.method == "GET":
        orderList = Project_Order.objects.filter(Q(order_user=User.objects.get(username=request.user)) |
                                                Q(order_audit=User.objects.get(username=request.user))).order_by("id")[
                    0:150]
        return render(request, 'users/user_center.html', {"user": request.user, "orderList": orderList})
    if request.method == "POST":
        if request.POST.get('password') == request.POST.get('c_password'):
            try:
                user = User.objects.get(username=request.user)
                user.set_password(request.POST.get('password'))
                user.save()
                return JsonResponse({"code": 200, "data": None, "msg": "密码修改成功"})
            except Exception as e:
                return JsonResponse({"code": 500, "data": None, "msg": "密码修改失败：%s" % str(e)})
        else:
            return JsonResponse({"code": 500, "data": None, "msg": "密码不一致，密码修改失败。"})


@login_required
@permission_required('auth.change_user', login_url='/noperm/')
def user(request, uid):
    if request.method == "GET":
        try:
            user = User.objects.get(id=uid)
        except Exception as e:
            return render(request, 'users/user_info.html', {"user": request.user, "errorInfo": "用户不存在，可能已经被删除."})
        userPermList = user.permission.all()
        roleList = RoleList.objects.all()
        role = user.role
        allPerm = PermissonList.objects.all()
        return render(request, 'users/user_info.html',
                      {"user": request.user, "user_info": user, "UserpermList": userPermList, "allPerm": allPerm,
                       "groupList": roleList, "role": role})

    elif request.method == "POST":
        try:
            user = User.objects.get(id=uid)
            User.objects.filter(id=uid).update(
                is_active=request.POST.get('is_active'),
                is_superuser=int(request.POST.get('is_superuser')),
                email=request.POST.get('email'),
                username=request.POST.get('username'),
                role=request.POST.get('groups')
            )
            # 如果权限key不存在就单做清除权限
            if request.POST.getlist('perms') is None:
                user.permission.clear()
            else:
                userPermList = []
                for perm in user.permission.all():
                    userPermList.append(perm.id)
                permList = [int(i) for i in request.POST.getlist('perms')]
                addPermList = list(set(permList).difference(set(userPermList)))
                delPermList = list(set(userPermList).difference(set(permList)))
                # 添加新增的权限
                for permId in addPermList:
                    perm = PermissonList.objects.get(id=permId)
                    user.permission.add(perm)
                # 删除去掉的权限
                for permId in delPermList:
                    perm = PermissonList.objects.get(id=permId)
                    user.permission.remove(perm)
            return HttpResponseRedirect('/user/{uid}/'.format(uid=uid))
        except Exception as e:
            print(e)
            return render(request, 'users/user_info.html', {"user": request.user, "errorInfo": "用户资料修改错误：%s" % str(e)})


@login_required
def group(request, gid):
    if request.method == "GET":
        try:
            group = RoleList.objects.get(id=gid)
        except:
            return render(request, 'users/group_info.html', {"user": request.user, "errorInfo": "用户不存在，可能已经被删除."})
        groupPerm = group.permission.all()
        allPerm = PermissonList.objects.all()
        return render(request, 'users/group_info.html',
                      {"user": request.user, "GpermList": groupPerm, "allPerm": allPerm, "group": group})
    elif request.method == "POST":
        try:
            role = RoleList.objects.get(id=gid)
            RoleList.objects.filter(id=gid).update(
                name=request.POST.get('name')
            )
            if request.POST.getlist('perms') is None:
                role.permission.clear()
            else:
                gPermList = []
                for perm in role.permission.all():
                    gPermList.append(perm.id)
                permList = [int(i) for i in request.POST.getlist('perms')]
                addPermList = list(set(permList).difference(set(gPermList)))
                delPermList = list(set(gPermList).difference(set(permList)))
                for permId in addPermList:
                    perm = PermissonList.objects.get(id=permId)
                    role.permission.add(permId)
                for permId in delPermList:
                    perm = PermissonList.objects.get(id=permId)
                    role.permission.remove(permId)
            return HttpResponseRedirect('/group/{gid}/'.format(gid=gid))
        except Exception as e:
            print(e)
            return render(request, 'users/group_info.html', {"user": request.user, "errorInfo": "部门资料修改错误:%s" % str(e)})


@login_required
def permission(request, pid):
    if request.method == "GET":
        try:
            permission = PermissonList.objects.get(id=pid)
        except:
            return render(request, 'users/permission_info.html', {"user": request.user, "errorInfo": "权限不存在，可能已经被删除."})
        return render(request, 'users/permission_info.html', {"user": request.user, "permission": permission})
    elif request.method == "POST":
        try:
            PermissonList.objects.filter(id=pid).update(
                name=request.POST.get('name'),
                url = request.POST.get('url')
            )
            return HttpResponseRedirect('/permission/{gid}/'.format(gid=pid))
        except Exception as e:
            return render(request, 'users/permission_info.html', {"user": request.user, "errorInfo": "用户资料修改错误：%s" % str(e)})
