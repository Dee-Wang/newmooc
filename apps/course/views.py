import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.core.urlresolvers import reverse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, Lesson, Video, VideoResource

from organization.models import CourseOrg, Teacher
from operation.models import UserFavor, CourseComments, UserCourse
from users.models import UserProfile


# 所有的课程的列表，以及多种的排序的方式
class CourseListView(View):
    def get(self,request):
        # 课程机构
        all_courses = Course.objects.all()

        hot_courses = all_courses.order_by("click_num")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(description__icontains=search_keywords)|Q(course_category__icontains=search_keywords)
                                             |Q(detail__icontains=search_keywords)|Q(course_notice__icontains=search_keywords)|Q(course_gain__icontains=search_keywords)
                                             |Q(course_tag__icontains=search_keywords)|Q(degree__icontains=search_keywords))

        # 根据学习人数进行排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'new':
                all_courses = all_courses.order_by("-add_time")
            elif sort == 'hot':
                all_courses = all_courses.order_by("-click_num")
            elif sort == 'students':
                all_courses = all_courses.order_by("-learning_num")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "sort":sort,
            "all_corses":all_courses,
            "hot_courses": hot_courses,
            "courses":courses,

        })


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        all_courses = Course.objects.all()
        cur_course = Course.objects.get(id=int(course_id))

        # 一旦发生点击行为，点击量就加1
        cur_course.click_num += 1
        cur_course.save()

        # 判断课程是否已经被收藏
        has_course_fav = False

        if request.user.is_authenticated():
            if UserFavor.objects.filter(user= request.user, fav_id=cur_course.id, fav_type=1):
                has_course_fav = True

        # 判断课程所属培训机构是否已经被收藏
        has_org_fav = False

        if request.user.is_authenticated():
            if UserFavor.objects.filter(user= request.user, fav_id=cur_course.course_org.id, fav_type=2):
                has_org_fav = True

        if course_id:
            all_lessons = cur_course.lesson_set.all()
            lesson_num = all_lessons.count()
            cur_course_org = cur_course.course_org
            tag = cur_course.course_tag
            if tag:
                reco_courses = all_courses.filter(course_tag = tag)[:3]
            else:
                reco_courses = []

        return render(request,"course-detail.html",{
            'course':cur_course,
            'has_org_fav':has_org_fav,
            'has_course_fav':has_course_fav,
            'all_lessons': all_lessons,
            'lesson_mun': lesson_num,
            'cur_course_org': cur_course_org,
            'reco_courses': reco_courses,
        })


# 课程章节视频信息
class CourseVideoView(View):
    def get(self, request, course_id):
        if request.user.is_authenticated():
            # 获取当前的课程，并且每当用户点击我要学习的时候，该课程的学习人数就自己加1
            cur_course = Course.objects.get(id=int(course_id))
            cur_course.learning_num += 1
            cur_course.save()

            # 先判断当前的登录用户是否已经学习了这个课程，如果没学习的话将该课程添加到用户学习课程的数据库中
            cur_user_course = UserCourse.objects.filter(user=request.user)
            course_list = []
            for user_course in cur_user_course:
                course_list.append(user_course.course)

            if cur_course not in course_list:
                user_learn_course = UserCourse()
                user_learn_course.user = request.user
                user_learn_course.course = cur_course
                user_learn_course.save()

            cur_course_lessons = cur_course.lesson_set.all()

            if cur_course:
                the_teacher = cur_course.teacher

            return render(request, "course-video.html", {
                'cur_course': cur_course,
                'cur_course_lessons': cur_course_lessons,
            })
        else:
            # return render(request, "login.html", {})
            return HttpResponseRedirect(reverse('users:login'))



# 课程评论信息
class CourseCommentView(View):
    def get(self, request, course_id):
        cur_course = Course.objects.get(id=int(course_id))
        all_resources = VideoResource.objects.filter(course=cur_course)
        all_comments = CourseComments.objects.filter(course=cur_course)
        return render(request, "course-comment.html", {
            'cur_course': cur_course,
            'all_resources': all_resources,
            'all_comments' : all_comments,
        })


# 添加评论
class AddCourseCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户的登录状态
            return HttpResponse(JsonResponse({"status":"fail", "msg":"用户未登录"}),content_type='application/json')
            # return HttpResponseRedirect(reverse('users:login'))
        else:
            course_id = int(request.POST.get('course_id', 0))
            comments = request.POST.get('comments', '')
            if course_id and comments:
                course_comments = CourseComments()
                course_comments.course = Course.objects.get(id=course_id)
                course_comments.comments = comments
                course_comments.user = request.user
                course_comments.save()
                return HttpResponse(JsonResponse({'status':'success', 'msg':'添加成功'}), content_type='application/json')
            else:
                return HttpResponse(JsonResponse({'status':'fail', 'msg':'添加出错'}), content_type='application/json')


