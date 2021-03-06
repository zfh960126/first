# _*_ encoding:utf-8 _*_

import xadmin
from .models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):

    list_display = ['name', 'des', 'add_time',]
    search_fields = ['name', 'des', ]
    list_filter = ['name', 'des', 'add_time',]

class CourseOrgAdmin(object):

    list_display = ['name', 'des', 'click_nums','fav_nums', 'image', 'address', 'city', 'add_time',]
    search_fields = ['name', 'des', 'click_nums','fav_nums', 'image', 'address', 'city',]
    list_filter =['name', 'des', 'click_nums','fav_nums', 'image', 'address', 'city', 'add_time',]





class TeacherAdmin(object):


    list_display = ['org', 'name', 'work_years','work_company', 'work_position', 'points', 'click_num','fav_nums', 'add_time',]
    search_fields = ['org', 'name', 'work_years','work_company', 'work_position', 'points', 'click_num','fav_nums',]
    list_filter = ['org', 'name', 'work_years','work_company', 'work_position', 'points', 'click_num','fav_nums', 'add_time',]


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
