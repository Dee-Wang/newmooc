from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from course.models import Course
from operation.models import UserFavor
from .forms import UserWantForm



# 机构列表
class OrgView(View):
    def get(self,request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_num")[:5]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) |Q(city__name__icontains=search_keywords)
                |Q(description__icontains=search_keywords)|Q(address__icontains=search_keywords)|Q(category__icontains=search_keywords))
        # 所在城市
        all_cities = CityDict.objects.all()
        # 取出筛选的城市
        city_id = request.GET.get('city', '')

        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 根据类别筛选
        category = request.GET.get('ct',"")
        if category:
            all_orgs = all_orgs.filter(category = category)

        # 根据学习人数进行排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by("-course_nums")
            elif sort == 'favors':
                all_orgs = all_orgs.order_by("-favor_num")
            elif sort == 'popularity':
                all_orgs = all_orgs.order_by("-click_num")



        # 在所有的筛选完成之后计算出符合条件的选项的数量
        org_nums = all_orgs.count()

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs" : all_orgs,
            "orgs" : orgs,
            "all_cities" : all_cities,
            "city_id":city_id,
            "category":category,
            "org_nums":org_nums,
            "hot_orgs":hot_orgs,
            "sort":sort,
        })


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id = int(org_id))

        # 一旦发生点击行为，这里就是在机构列表页或者其他途径点击了这个机构查看详情，或者在这个机构详情的首页刷新，都算是点击行为。点击数就加1
        course_org.click_num += 1
        course_org.save()

        has_org_fav = False

        if request.user.is_authenticated():
            if UserFavor.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_org_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()

        return render(request, 'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teahers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_org_fav':has_org_fav,
        })


# 机构课程信息
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_courses = course_org.course_set.all()
        # 判断用户是否已经收藏这个机构
        has_fav = False

        if request.user.is_authenticated():
            if UserFavor.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True


        #teacher_course = all_courses.filter(teacher=teacher)

        return render(request, 'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 机构简述
class OrgDescriptionView(View):
    def get(self, request, org_id):
        current_page = "description"
        course_org = CourseOrg.objects.get(id = int(org_id))

        # 判断用户是否已经收藏这个机构
        has_fav = False

        if request.user.is_authenticated():
            if UserFavor.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        #teacher_course = all_courses.filter(teacher=teacher)

        return render(request, 'org-detail-desc.html',{
            'course_org':course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


# 机构讲师列表
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_teachers = course_org.teacher_set.all()

        # 判断用户是否已经收藏这个机构
        has_fav = False

        if request.user.is_authenticated():
            if UserFavor.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html',{
            'all_teahers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


# 教师信息列表
class TeacherListView(View):
    def get(self,request):
        # 所有的教师
        all_teachers = Teacher.objects.all()
        hot_teachers = all_teachers.order_by("-click_num")[:5]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(
                Q(name__icontains=search_keywords)|Q(work_company__icontains=search_keywords)
                |Q(work_position__icontains=search_keywords)|Q(characters__icontains=search_keywords)
                |Q(organization__name__icontains=search_keywords)|Q(organization__city__name__icontains=search_keywords))

        # 根据学习人数进行排序
        sort = request.GET.get('sort', "")
        if sort == 'hot':
            all_teachers = all_teachers.order_by("-click_num")

        # 在所有的筛选完成之后计算出符合条件的选项的数量
        teacher_nums = all_teachers.count()

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 3, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers" : all_teachers,
            "teachers" : teachers,
            "teacher_nums":teacher_nums,
            "hot_teachers":hot_teachers,
            "sort":sort,
        })



# 教师详情
class TeacherDetailView(View):
    def get(self, request, teacher_id):
        all_teachers = Teacher.objects.all()
        hot_teachers = all_teachers.order_by("-click_num")[:5]

        cur_teacher = Teacher.objects.get(id = int(teacher_id))

        # 一旦产生点击行为，就将点击数加1
        cur_teacher.click_num += 1
        cur_teacher.save()

        # 获取当前的教师所讲授的所有的课程
        all_courses = cur_teacher.course_set.all()

        # 判断用户是否已经收藏这个教师
        has_teacher_fav = False

        if request.user.is_authenticated():
            if UserFavor.objects.filter(user=request.user, fav_id=cur_teacher.id, fav_type=3):
                has_teacher_fav = True

        # 判断培训机构是否已经被收藏
        has_org_fav = False

        if request.user.is_authenticated():
            if UserFavor.objects.filter(user= request.user, fav_id=cur_teacher.organization.id, fav_type=2):
                has_org_fav = True

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        curteacher_course = p.page(page)

        return render(request, 'teacher-detail.html',{
            'all_courses':all_courses,
            'cur_teacher':cur_teacher,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav,
            'hot_teachers':hot_teachers,
            'curteacher_course ':curteacher_course,
        })


# 我要学习表单配置
class AdduserwantView(View):
    def post(self, request):
        userwant_form = UserWantForm(request.POST)

        if userwant_form.is_valid():
            userwant_form.save(commit=True)
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'添加出错'}", content_type='application/json')


# 用户收藏和取消用户收藏
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户的登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}',content_type='application/json')

        exist_records = UserFavor.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_records:
            # 如果用户收藏已经存在，那么再次点击表示用户取消这个收藏
            exist_records.delete()

            # 取消收藏的时候，根据不停地分类对应的收藏数就减去1,这里fav_type等于1时对应课程，等于2对应培训机构，等于3对应讲师
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.favor_num -= 1
                if course.favor_num <= 0:
                    course.favor_num = 0
                course.save()
            elif int(fav_type) == 2:
                cur_couseorg = CourseOrg.objects.get(id=int(fav_id))
                cur_couseorg.favor_num -= 1
                if cur_couseorg.favor_num <= 0:
                    cur_couseorg.favor_num = 0
                cur_couseorg.save()
            elif int(fav_type) == 3:
                cur_teacher = Teacher.objects.get(id=int(fav_id))
                cur_teacher.favor_num -= 1
                if cur_teacher.favor_num <= 0:
                    cur_teacher.favor_num = 0
                cur_teacher.save()

            return HttpResponse('{"status":"fail", "msg":"取消收藏"}', content_type='application/json')
        else:
            user_fav = UserFavor()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                # 用户收藏的时候对应的项目的收藏数就自动加1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.favor_num += 1
                    course.save()
                elif int(fav_type) == 2:
                    cur_couseorg = CourseOrg.objects.get(id=int(fav_id))
                    cur_couseorg.favor_num += 1
                    cur_couseorg.save()
                elif int(fav_type) == 3:
                    cur_teacher = Teacher.objects.get(id=int(fav_id))
                    cur_teacher.favor_num += 1
                    cur_teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出问题"}', content_type='application/json')




