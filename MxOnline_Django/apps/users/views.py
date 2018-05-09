from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
import json

from .models import UserProfile,EmainverifyReord,Banner
from .forms import LoginForm,RegisteForm,ForgetForm,ModifyPwdForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from .forms import UploadImageForm
from operation.models import UserCourse,UserFavorite,UserMessage
from django.http import HttpResponse,HttpResponseRedirect
from organization.models import CourseOrg,Teacher
from course.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
         try:
             user = UserProfile.objects.get(Q(username=username)|Q(email=username))
             if user.check_password(password):
                 return user
         except Exception as  e:
             return None

class AciveUserView(View):
    def get(self,request,active_code):
        all_records = EmainverifyReord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email =email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')

        return render(request,'login.html')


class RegisterView(View):
    def get(self,request):
        register_form = RegisteForm()
        return render(request,'register.html',{'register':register_form})


    def post(self,request):
        register_form = RegisteForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html',{'register_form': register_form})#,"msg": "用户已存在"})

            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #写入欢迎注册信息
            user_message = UserMessage()
            user_message.ueer = user_profile.id
            user_message.message = "欢迎注册"
            user_message.save()

            send_register_email(user_name,"register")
            return render(request, 'index.html')

        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html',
                                  {"msg": "用户未激活"})  # ,"login_form":login_form}


            else:
                return render(request, 'login.html',
                              {"msg": "用户名或密码错误！"})  # ,"login_form":login_form}

        else:
            return render(request,'login.html',{"login_form":login_form})#,"login_form":login_form}

class LogoutView(View):
    def get(self,request):
        logout(request)

        return HttpResponseRedirect(reverse('index') )


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form': forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email, "forget")
            return render(request,'send_success.html',{"forget_form":forget_form})#,"login_form":login_form}
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})

#
# # Create your views here.
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username')
#         pass_word = request.POST.get('password')
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             return render(request, 'login.html', {"msg":"用户名或密码错误！"})
#
#
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})


class ResetView(View):
    def get(self,request,active_code):
        all_records = EmainverifyReord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html',{"email":email})
        else:
            return render(request, 'active_fail.html')

        return render(request,'login.html')
class ModifyPwdView(View):
    #修改用户密码
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1",'')
            pwd2 = request.POST.get("password2",'')
            email = request.POST.get("email",'')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {"email": email,'msg':'密码不一致'})
            user = UserProfile.objects.get(email = email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get("email",'')
            return render(request, 'password_reset.html', {"email": email,'modify_form':modify_form})

class UserinfoView(LoginRequiredMixin,View):
    #用户个人信息
    def get(self,request):
        return render(request, 'usercenter-info.html', {

        })
    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='appplication/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='appplication/json')


class UploadImageView(View):
    #用户修改头像
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='appplication/json')

        else:
            return HttpResponse('{"status":"fail"}', content_type='appplication/json')


class UpdatePwdView(View):
    #在个人中心修改用户密码
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1",'')
            pwd2 = request.POST.get("password2",'')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='appplication/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='appplication/json')
        else:
            print(modify_form.errors)
            return HttpResponse(json.dumps(modify_form.errors), content_type='appplication/json')


class SendEmailCodeView(View):
    #发送邮箱验证码
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email =email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='appplication/json')

        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='appplication/json')


class UpdateEmailView(View):
    #修改个人邮箱
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code', '')

        existed_records = EmainverifyReord.objects.filter(email=email,code=code,send_type = 'update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='appplication/json')

        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='appplication/json')


class MyCourseView(View):
    #我的课程
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return  render(request,'usercenter-mycourse.html',{
            "user_courses": user_courses


      })




class MyFavOrgView(View):
    #我的收藏
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return  render(request,'usercenter-fav-org.html',{
            "org_list": org_list


      })

class MyFavTeacherView(View):
    # 我的收藏
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list

        })


class MyFavCourseView(View):
    # 我的收藏
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list

        })


class MyMessageView(View):
    # 我的收藏
    def get(self, request):
        all_message = UserMessage.objects.filter(id=request.user.id)


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_message, 1, request=request)

        messages = p.page(page)


        return render(request, 'usercenter-message.html', {
            "messages": messages

        })

class IndexView(View):
    def get(self,request):
        #幕学在线主页
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_course = Course.objects.filter(is_banner=False)[0:16]
        course_orgs = CourseOrg.objects.all()
        return render(request,'index.html',{
            "all_banners": all_banners,
            "courses": courses,
            "banner_course": banner_course,
            "course_orgs": course_orgs,
        })