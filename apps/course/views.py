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

from utils.mixin_utils import LoginRequiredMixin


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
class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # 获取当前的课程
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
class CourseVideoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        if request.user.is_authenticated():
            # 获取当前的课程，并且每当用户点击我要学习的时候，该课程的学习人数就自己加1
            cur_course = Course.objects.get(id=int(course_id))

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
                # 在视图函数中计算效率更高，因为只是进行一次计算，而在models中每次获取学习人数的时候都要遍历一遍，获得学习的人数
                cur_course.learning_num += 1
                cur_course.save()

            cur_course_lessons = cur_course.lesson_set.all()

            if cur_course:
                the_teacher = cur_course.teacher

            # 获取学习当前课程的用户还学习了的课程
            user_courses = UserCourse.objects.filter(course=cur_course)
            user_ids = [user_course.user.id for user_course in user_courses]
            all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            # # 接下来我们会根据得到的用户的id获取所有的学习该课程的用户并且获取这些用户对应的所有的课程，存储成一个列表的形式，我们取出列表的前三个元素，
            # # 并且使用集合将列表中的重复的的元素过滤掉，发送给前端文件一个可迭代的集合了性的对象
            # all_learned_courses = [all_user_other_courses.course for all_user_other_courses in all_user_courses]
            # # other_courses = set(all_learned_courses.filter(id!=cur_course.id)[:5])
            # other_courses = set(all_learned_courses[:3])

            # 还有一种方法,先获取所有的课程的id
            course_ids = [user_course.course.id for user_course in all_user_courses]
            # 根据课程的id获取所有的课程
            related_courses = set(Course.objects.filter(id__in=course_ids).order_by("-click_num")[:3])


            return render(request, "course-video.html", {
                'cur_course': cur_course,
                'cur_course_lessons': cur_course_lessons,
                'related_courses':related_courses,
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

        # 获取学习当前课程的用户还学习了的课程
        user_courses = UserCourse.objects.filter(course=cur_course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 获取所有的课程的id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 根据课程的id获取所有的课程
        related_courses = set(Course.objects.filter(id__in=course_ids).order_by("-click_num")[:3])
        return render(request, "course-comment.html", {
            'cur_course': cur_course,
            'all_resources': all_resources,
            'all_comments' : all_comments,
            'related_courses': related_courses,
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


# # 课程播放
# class Course