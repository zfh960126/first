# _*_ encoding:utf-8 _*_
from django.conf.urls import url,include

from .views import CourseView,CourseDetailView,CourseInfoView,CommentsView,AddCommentsView

urlpatterns = (


    #课程机构列表页
    url(r'^list/$', CourseView.as_view(),name='course_list'),

    #课程机构详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(),name='course_detail'),

    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(),name='course_info'),
    #课程评论
    url(r'^comments/(?P<course_id>\d+)/$', CommentsView.as_view(),name='course_comments'),
    #添加课程评论
    url(r'^add_comments/$', AddCommentsView.as_view(),name='add_comment'),

)