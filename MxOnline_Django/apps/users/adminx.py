# _*_ encoding:utf-8 _*_

import xadmin
from .models import EmainverifyReord,Banner
from xadmin import views

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettin(object):
    site_title = '暮学后台管理系统'
    site_footer = '暮学在线网'
    menu_style = 'accordion'

class EmailVerifyRecordAdmin(object):

    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']

class BannerAdmin(object):

    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(EmainverifyReord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettin)