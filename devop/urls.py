"""devop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.views.generic.base import RedirectView
from devop.views.index import index, login, logout, noperm, config
from devop.views.user import user_center, user_manage, user, register, group, permission
from devop.views.app import apps_list, apps_model, apps_add, apps_playbook_modf,apps_playbook_file,apps_playbook_run,ansible_log,ansible_run
from devop.views.deploy import deploy_add, deploy_list, deploy_ask, deploy_init,deploy_order,deploy_log
from devop.views.cron import cron_log, cron_add, cron_list, cron_config
from devop.views.assets import assets_config,assets_add,assets_list,assets_log,assets_modf,assets_view
from devop.restapis import user_api, deploy_api, assets_api

# from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/media/favicon.ico')),
    url(r'^$', index),
    url(r'^config', config),
    url(r'^noperm', noperm, name='permissiondenyurl'),
    url(r'^login', login),
    url(r'^logout', logout),
    url(r'^register/', register),
    url(r'^user/(?P<uid>[0-9]+)/$', user),
    url(r'^user/center/$', user_center),
    url(r'^users/manage$', user_manage),
    url(r'^group/(?P<gid>[0-9]+)/$', group),
    url(r'^permission/(?P<pid>[0-9]+)/$', permission),

    url(r'^assets_config', assets_config),
    url(r'^assets_add', assets_add),
    url(r'^assets_list', assets_list),
    url(r'^assets_log', assets_log),
    url(r'^assets_mod/(?P<aid>[0-9]+)/$',assets_modf),
    url(r'^assets_view/(?P<aid>[0-9]+)/$',assets_view),

    url(r'^apps/$', apps_list),
    url(r'^apps/model/$', apps_model),
    url(r'^apps/playbook/add/$', apps_add),
    url(r'^apps/playbook/modf/(?P<pid>[0-9]+)/$',apps_playbook_modf),
    url(r'^apps/playbook/file/(?P<pid>[0-9]+)/$',apps_playbook_file),
    url(r'^apps/playbook/run/(?P<pid>[0-9]+)/$',apps_playbook_run),
    url(r'^apps/log/$', ansible_log),
    url(r'^apps/run/$',ansible_run),

    url(r'^deploy_order', deploy_order),
    url(r'^deploy_add', deploy_add),
    url(r'^deploy_list', deploy_list),
    url(r'^deploy_log', deploy_log),

    url(r'^cron_config', cron_config),
    url(r'^cron_list', cron_list),
    url(r'^cron_add', cron_add),
    url(r'^cron_log', cron_log),

    url(r'^api/user/$', user_api.user_list),
    url(r'^api/user/(?P<id>[0-9]+)/$', user_api.user_detail),
    url(r'^api/group/$', user_api.group_list),
    url(r'^api/group/(?P<id>[0-9]+)/$', user_api.group_detail),
    url(r'^api/permission/$', user_api.group_list),
    url(r'^api/permission/(?P<id>[0-9]+)/$', user_api.group_detail),
    url(r'^api/server/$', assets_api.asset_server_list),
    url(r'^api/server/(?P<id>[0-9]+)/$', assets_api.asset_server_detail),
    url(r'^api/service/$', assets_api.service_list),
    url(r'^api/service/(?P<id>[0-9]+)/$', assets_api.service_detail),
    url(r'^api/business/$', assets_api.business_list),
    url(r'^api/business/(?P<id>[0-9]+)/$', assets_api.business_detail),
    url(r'^api/idc/$', assets_api.idc_list),
    url(r'^api/idc/(?P<id>[0-9]+)/$', assets_api.idc_detail),
    url(r'^api/assets/$', assets_api.asset_list),
    url(r'^api/assets/(?P<id>[0-9]+)/$', assets_api.asset_detail),
    url(r'^api/order/(?P<username>.+)/$', deploy_api.OrderList.as_view()),
    url(r'^api/zone/$', assets_api.zone_list),
    url(r'^api/zone/(?P<id>[0-9]+)/$', assets_api.zone_detail),
    url(r'^api/raid/$', assets_api.raid_list),
    url(r'^api/raid/(?P<id>[0-9]+)/$', assets_api.raid_detail),
    url(r'^api/line/$', assets_api.line_list),
    url(r'^api/line/(?P<id>[0-9]+)/$', assets_api.line_detail),
]
