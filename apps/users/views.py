import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Banner
from course.models import Course
from operation.models import UserCourse, UserFavor, UserMessage
from organization.models import CourseOrg

from .forms import LoginForm,RegisterForm,ForgetPwdForm, ResetPwdForm, UploadImageForm, UserChangeInfoForm, UpdatePasswpordForm
from utils.email_send import send_email

# Create your views here.
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # user = UserProfile.objects.get(username = username)
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)|Q(phone_num=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登录
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username = user_name, password = pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                    # return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg":"用户名或者密码错误"})
        else:
            return render(request, "login.html", { "login_form": login_form})


# 用户登出（注销）
class LogoutView(View):
    def get(self, request):
        logout(request)
        request.user.is_authenticated = False
        return HttpResponseRedirect(reverse('index'))


# 用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form':register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email = user_name):
                return render(request, "register.html", { "register_form": register_form, "msg": "用户已经存在" })
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_email(user_name, "register")
            return render(request, "active_successfully.html")
        else:
            return render(request, "register.html", {"register_form": register_form, "msg": "填入的信息有误" })


# 用户激活
class ActiveView(View):
    def get(self,request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# 用户忘记密码
class ForgetPasswordView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form })

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email = user_name):
                send_email(user_name, "forget_password")
                return render(request, "send_successfully.html", {"forgetpwd_form": forgetpwd_form })
            else:
                return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form, "msg": "该邮箱未注册账户" })
        else:
            return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form })


# 用户进入重设密码的页面
class ResetPasswordView(View):
    def get(self,request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email })
        else:
            return render(request, "resetpwdfail.html")


# 用户在重设密码的界面输入修改的密码
class ModifyPasswordView(View):
    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            password1 = request.POST.get("password1","")
            password2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if password1 == password2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password1)
                user.save()
                return render(request, "login.html")
            else:
                return render(request, "password_reset.html", {"resetpwd_form": resetpwd_form}, {"msg": "两次密码不一致"})
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"resetpwd_form": resetpwd_form},{"email":email}, {"msg": "密码输入错误"})


# 用户个人信息页面
class UserInfoView(View):
    def get(self,request):
        return render(request, "usercenter-info.html")


# 用户个人学习课程列表
class MyCourseView(View):
    def get(self, request):
        if request.user.is_authenticated():
            all_user_course = UserCourse.objects.filter(user=request.user)

            # 对课程进行分页
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_user_course, 3, request=request)
            user_courses = p.page(page)

        return render(request, "usercenter-mycourse.html", {
            "all_user_course" : all_user_course,
            "user_courses" : user_courses,
        })


# 用户消息列表
class UserMessageView(View):
    def get(self, request):
        """我们在设计数据库的时候如果user=0的话是发送给全部的用户的消息。
           user不等于0的时候，对应的是用户的id，找到对应id的用户，填入对应的数据库.
           在所有的消息中设置一个布尔类型的属性，用来表示消息是否已经度过了，默认是False，表示消息是未读的，读过以后变成True。
        """

        # 下面是自己一开始想到的方法，声明一个列表存储消息，但是这样做就不能存储每条消息对应的添加时间
        # # 定义一个列表用来存储要显示的所有未读的消息
        # all_unread_message = []
        #
        # # 取出所有的给所有用户发送的未读消息
        # to_alluser_message = UserMessage.objects.filter(user=0, is_read=False)
        #
        # # 对于Query Set中的每一个对象，一点用户跳转到该页面，就看到了这些消息，我们就将这些消息设成已读
        # for alluser_message in to_alluser_message:
        #     alluser_message.is_read = True
        #     all_unread_message.append(alluser_message.message)
        #
        # # 接下来是获取只发送给当前用户的未读的消息
        # to_theuser_message = UserMessage.objects.filter(user=request.user.id, is_read=False)
        #
        # # 和上面的类似，用户点金页面之后就默认读了这些消息，就把这些消息设置成已读
        # for theuser_message in to_theuser_message:
        #     theuser_message.is_read = True
        #     all_unread_message.append(theuser_message.message)


        # 首先获得所有的课程
        all_messages = UserMessage.objects.filter(Q(user=0)|Q(user=request.user.id))

        # 其实很简单就能实现按条件过滤，首先获取所有的未读的消息
        all_unread_message = all_messages.filter(is_read=False)

        # 对所有的消息，将是否已读设置成已读,并将修改保存到数据库
        for unread_message in all_unread_message:
            unread_message.is_read = True
            unread_message.save()

        # 对用户的消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 3, request=request)
        usermessages = p.page(page)

        return render(request, "usercenter-message.html", {
            "usermessages": usermessages,
        })


# 用户收藏的课程的列表
class UserFavCourseView(View):
    def get(self, request):
        all_userfav_course = UserFavor.objects.filter(user=request.user , fav_type=1)
        user_favcourse_list = []
        for userfav_course in all_userfav_course:
            fav_course = Course.objects.get(id=userfav_course.fav_id)
            user_favcourse_list.append(fav_course)


        # 对处理好的数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_favcourse_list, 3, request=request)
        fav_courses = p.page(page)
        return render(request, "usercenter-fav-course.html", {
            'fav_courses':fav_courses,

        })


# 用户收藏的讲师的列表
class UserFavTeacherView(View):
    def get(self, request):
        all_userfav_teacher = UserFavor.objects.filter(user=request.user , fav_type=3)
        user_favteacher_list = []
        for userfav_teacher in all_userfav_teacher:
            fav_teacher = Course.objects.get(id=userfav_teacher.fav_id)
            user_favteacher_list.append(fav_teacher)

        # 对处理好的数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_favteacher_list, 3, request=request)
        fav_teachers = p.page(page)
        return render(request, "usercenter-fav-teacher.html", {
            'fav_teachers':fav_teachers,
        })


# 用户收藏的培训机构的列表
class UserFavOrgView(View):
    def get(self, request):
        all_userfav_org = UserFavor.objects.filter(user=request.user, fav_type=2)
        user_favorg_list = []
        for userfav_org  in all_userfav_org :
            fav_org  = Course.objects.get(id=userfav_org.fav_id)
            user_favorg_list.append(fav_org )

        # 对处理好的数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_favorg_list, 3, request=request)
        fav_orgs = p.page(page)
        return render(request, "usercenter-fav-org.html", {
            'fav_orgs':fav_orgs,
        })


# 用户修改个人头像
class UploadImageView(View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            # image_form.save()
            return HttpResponse("{'status':'success', 'msg':'头像修改成功'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'头像修改失败'}", content_type='application/json')


# 发送邮箱验证码
class SendEmailCodeView(View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_email(email, "change_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')


# 修改邮箱用户填写验证码之后的校验和后台处理
class UpdateEmailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="change_email")

        # 判断是否存在这条记录，如果存在的话作出相应的修改.
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


# 用户修改个人信息（非头像信息）
class ModifyPersonalInfoView(View):

    def post(self, request):
        if request.user.is_authenticated():
            # 这里在参数中一定要加上inatance=request.user,也就是指明我是对当前用户的修改，如果没有这个参数的话，就会被默认成添加一条新的记录。
            user_info_form = UserChangeInfoForm(request.POST, instance=request.user)
            if user_info_form.is_valid():
                user_info_form.save()
                return HttpResponse("{'status':'success', 'msg':'个人信息修改成功'}", content_type='application/json')
            else:
                return HttpResponse(json.dumps(user_info_form.errors_), content_type='application/json')
        else:
            return render(request, 'login.html')



# 网站首页
class IndexView(View):
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_course = Course.objects.filter(is_banner=True)[:5]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, "index.html", {
            "all_banners":all_banners,
            "courses":courses,
            "banner_course":banner_course,
            "course_orgs":course_orgs,
        })


# 全局404错误页面的配置
def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 全局500错误页面的配置
def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

# 用户在个人信息界面修改个人密码，不用验证旧密码
class UpdatePwdView(View):
    def post(self, request):
        updatepwd_form = UpdatePasswpordForm(request.POST)
        if updatepwd_form.is_valid():
            # 从前端提交的form表单中获取数据
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")

            # 输入新的密码，如果密码形式符合规定，而且两次输入的密码一致，修改密码成功
            if password1 == password2:
                user = request.user
                user.password = make_password(password1)
                user.save()
                return HttpResponse(JsonResponse({'status':'success', 'msg':'密码修改成功'}), content_type='application/json')
            else:
                return HttpResponse(JsonResponse({'status':'fail', 'msg':'两次输入的密码不一致'}), content_type='application/json')
        else:
            return HttpResponse(JsonResponse(updatepwd_form.errors_), content_type='application/json')


# # 用户在个人中心点击修改密码进行密码的修改，和上面忘记密码不同的是这里需要验证旧密码
# class ChangePasswordView(View):
#     def post(self, request):
#         changepwd_form = ChangePasswpordForm(request.POST)
#         if changepwd_form.is_valid():
#             # 从前端提交的form表单中获取数据
#             oldpassword = request.POST.get("oldpassword", "")
#             password1 = request.POST.get("password1", "")
#             password2 = request.POST.get("password2", "")
#
#             # 先验证旧密码，验证通过才能继续修改密码
#             if make_password(oldpassword) == request.user.password:
#                 if password1 == password2:
#                     user = request.user
#                     user.password = make_password(password1)
#                     user.save()
#                     return HttpResponse("{'status':'success', 'msg':'密码修改成功'}", content_type='application/json')
#                 else:
#                     return HttpResponse("{'status':'fail', 'msg':'两次输入的密码不一致'}", content_type='application/json')
#         else:
#             return HttpResponse(json.dumps(changepwd_form.errors_), content_type='application/json')


# # 用户修改个人邮箱
# class ModifyPersonalEmailView(View):
#
#     def post(self, request):
#
#         if not request.user.is_authenticated():
#             # 判断用户的登录状态
#             return HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')
#
#         if request.user.is_authenticated():
#             email = request.POST.get('email','')
#             code = request.POST.get('code','')
#
#         exist_records = UserProfile.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
