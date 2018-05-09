# _*_ encoding:utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from operation.models import UserFavorite,CourseComments,UserCourse

from .models import Course,CourseResoure
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q
# Create your views here.

class CourseView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.all().order_by('-click_nums')[:3]

        # 课程搜索
        search_keyword = request.GET.get('keywords','')
        if search_keyword:
            all_course = all_course.filter(Q(name__icontains=search_keyword)|Q(des__icontains=search_keyword))


        #课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_course, 3,request=request)

        course = p.page(page)
        return render(request,'course-list.html',{
            'all_course':course,
            'sort': sort,
            'hot_courses': hot_course,
        })


class CourseDetailView(View):
   #课程详情
    def get(self, request,course_id):
        course = Course.objects.get(id = int(course_id))

        #增加课程点击数
        course.click_nums +=1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id),fav_type=1):
                has_fav_course = True

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.CourseOrg.id),fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag = tag)[:1]
        else:
            relate_course = []

        return render(request, 'course-detail.html', {
            'course':course,
            'relate_courses': relate_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin,View):
    # 课程章节信息
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        all_resources = CourseResoure.objects.filter(course=course)

        #查询用户是否已经关联了该课程
        user_course = UserCourse.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_course]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_id = [user_couser.course.id for user_couser in all_user_courses]
        # 获取学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_id).order_by('-click_nums')[:5]

        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
        })


class CommentsView(LoginRequiredMixin,View):
    # 课程章节信息
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResoure.objects.filter(course=course)

        all_comments =  CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,



        })

class AddCommentsView(View):
    # 添加课程评论

    def post(self,request):
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='appplication/json')
        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id) > 0 and comments:
                course_comments = CourseComments()
                course = Course.objects.get(id = int(course_id))
                course_comments.course = course
                course_comments.comments = comments
                course_comments.user = request.user
                course_comments.save()

                return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='appplication/json')

        else:
                return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='appplication/json')


