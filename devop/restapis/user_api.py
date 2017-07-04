#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from rest_framework import viewsets, permissions
from rest_framework import status
from devop.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from opman.models import MyUser as User
from opman.models import RoleList,PermissonList
from devop.tasks import recordAssets


@api_view(['GET', 'POST'])
def user_list(request, format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id, format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('opman.delete_user'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def group_list(request, format=None):
    if request.method == 'GET':
        snippets = RoleList.objects.all()
        serializer = GroupSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),
                               content="添加部门：{group_name}".format(group_name=request.data.get("name")), type="group",
                               id=serializer.data.get('id'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, id, format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = RoleList.objects.get(id=id)
    except RoleList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GroupSerializer(snippet, data=request.data)
        old_name = snippet.name
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),
                               content="修改部门名称：{old_name} -> {group_name}".format(old_name=old_name,
                                                                                  group_name=request.data.get("name")),
                               type="group", id=id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        recordAssets.delay(user=str(request.user), content="删除部门：{group_name}".format(group_name=snippet.name),
                           type="group", id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def permission_list(request, format=None):
    if request.method == 'GET':
        snippets = PermissonList.objects.all()
        serializer = PermissionSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def permission_detail(request, id, format=None):
    try:
        snippet = PermissonList.objects.get(id=id)
    except PermissonList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PermissionSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PermissionSerializer(snippet, data=request.data)
        old_name = snippet.name
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),
                               content="修改权限名称：{old_name} -> {per_name}".format(old_name=old_name,
                                                                                  per_name=request.data.get("name")),
                               type="group", id=id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('opman.delete_group'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        recordAssets.delay(user=str(request.user), content="删除权限：{per_name}".format(per_name=snippet.name),
                           type="group", id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)

