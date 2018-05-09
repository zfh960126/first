# _*_ encoding:utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskFoem
from course.models import Course
from operation.models import UserFavorite
from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from course.models import Course
from django.db.models import Q
# Create your views here.

class OrgView(View):
    #课程机构列表功能
    def get(self,request):
        #课程机构
        all_rgs =CourseOrg.objects.all()
        hot_orgs = all_rgs.order_by('click_nums')[:3]
        #城市
        all_citys = CityDict.objects.all()
        #取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_rgs = all_rgs.filter(city_id=int(city_id))

        # 机构搜索
        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_rgs = all_rgs.filter(Q(name__icontains=search_keyword) | Q(des__icontains=search_keyword))

        #类别筛选
        category = request.GET.get('ct','')
        if category:
            all_rgs = all_rgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_rgs = all_rgs.order_by('students')
            elif sort == 'courses':
                all_rgs = all_rgs.order_by('course_nums')



        org_nums = all_rgs.count()
        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_rgs, 3,request=request)

        orgs = p.page(page)

        return render(request,'org-list.html',{
            "all_rgs":orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            'category':category,
            'hot_orgs': hot_orgs,
            'sort': sort,
                    })

class AddUserAskView(View):
    '''用户添加咨询'''

    def post(self,request):
        userask_form = UserAskFoem(request.POST)
        if userask_form.is_valid():
            userask_form = userask_form.save(commit=True)
            return HttpResponse("{'statue':'success'}",content_type='appplication/json')
        else:
            return HttpResponse("{'statue':'fail','msg':'添加出错'}",content_type='appplication/json')


class OrgHomeView(View):
    #"机构首页"
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id = int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id = int(course_org.id)):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })

class OrgCourseView(View):
    #"机构列表页"
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id = int(org_id))
        course_org.click_nums +=1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id)):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })

class OrgDescView(View):
    #"机构介绍"
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id)):
                has_fav = True
        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })

class OrgTeacherView(View):
    #"讲师介绍"
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_teacher = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id)):
                has_fav = True
        return render(request, 'org-detail-teachers.html',{
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })

class OrgFavView(View):
    #"用户收藏"
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        print(fav_id,fav_type)
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='appplication/json')
        exit_recodes = UserFavorite.objects.filter(user=request.user,fav_id = int(fav_id),fav_type = int(fav_type))
        if exit_recodes:
            exit_recodes.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id = int(fav_id))
                course.fav_nums -=1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id = int(fav_id))
                course_org.fav_nums -=1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id = int(fav_id))
                teacher.fav_nums -=1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"fail","msg":"收藏"}', content_type='appplication/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()


                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='appplication/json')

            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='appplication/json')


class TeacherListView(View):
    #课程讲师列表
    def get(self, request):
        all_teachers = Teacher.objects.all()

        search_keyword = request.GET.get('keywords', '')
        if search_keyword:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keyword) | Q(work_company__icontains=search_keyword))

        current_nav = 'teacher'

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_num')

        sorted_teacher = Teacher.objects.all().order_by('-click_num')[:3]

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html',{
            'all_teachers':teachers,
            'sorted_teacher': sorted_teacher,
            'sort': sort,
            'current_nav': current_nav,

        })


class TeacherDetailView(View):
    #课程讲师列表
    def get(self, request,teacher_id):

        teacher = Teacher.objects.get(id = int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        all_course = Course.objects.filter(teacher=teacher)
        sorted_teachers = Teacher.objects.all().order_by('-click_num')[:3]

        has_teacher_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.id),fav_type=3):
                has_teacher_fav = True

        has_org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(teacher.org.id), fav_type=2):
                has_org_fav = True

        return render(request, 'teacher-detail.html',{
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teachers': sorted_teachers,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav,


        })