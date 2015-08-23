from django.conf.urls import patterns, include, url
from rest_framework import routers
from api.views import  Login, TeacherClassView, ClassStudentsView,AttendenceView, AttendenceDetail
router = routers.SimpleRouter(trailing_slash=False)

router.register(r'login/$', Login, base_name='login')
router.register(r'class/$', TeacherClassView)
router.register(r'class/students/(?P<batch_id>\d+)/$', ClassStudentsView)
router.register(r'class/attendence/$', AttendenceView, base_name="attendence")
router.register(r'class/attendance/$', AttendenceDetail)
urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-token-auth',
                           'rest_framework.authtoken.views.obtain_auth_token'),

                       )