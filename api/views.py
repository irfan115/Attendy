from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from accounts.models import Teacher
from api.models import StudentClass, Student, Attendance
from api.serializer import StudentClassSerializer,  StudentSearchSerializer, AttendenceSaveSerializer,AttendenceSerializer
import datetime

from api.forms import LoginForm
# Create your views here.

class Login(viewsets.ViewSet):
    permission_classes = (AllowAny, )

    def create(self, request):
        form = LoginForm(request.DATA)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            logged_in_user = authenticate(email=email, password=password)
            if logged_in_user:
                try:
                     token, created = Token.objects.get_or_create(
                    user=logged_in_user)
                     if created:
                     	token.save()
                     return Response({'token': token.key, 'success': True}, status=200)
                except Token.DoesNotExist:
                    pass          
            return Response({'token': None, 'success': False, "message": "incorrect email or password"}, status=401)
        else:
            return Response({'token': None, 'success': False, "message": form.errors}, status=400)


class TeacherClassView(viewsets.ReadOnlyModelViewSet):
    model = StudentClass
    permission_classes = (IsAuthenticated, )
    serializer_class = StudentClassSerializer
    queryset = StudentClass.objects.all()

    def get_queryset(self):
        queryset = super(TeacherClassView, self).get_queryset()
        day   = datetime.datetime.today().weekday() 
        return queryset.filter(course__teacher = self.request.user, class_days__contains = day)


class ClassStudentsView(viewsets.ReadOnlyModelViewSet):
    model = Student
    permission_classes = (IsAuthenticated, )
    serializer_class = StudentSearchSerializer
    queryset = Student.objects.all()

    def get_queryset(self):
        queryset = super(ClassStudentsView, self).get_queryset()
        if self.kwargs.get('batch_id'):
            return queryset.filter(batch = self.kwargs.get('batch_id'))


class AttendenceView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def create(self, request):
        form = AttendenceSaveSerializer(data=request.DATA)
        if form.is_valid():
            form.save()
            return Response({'success': True}, status=200)
        return Response({'success': False}, status=400)

class AttendenceDetail(viewsets.ReadOnlyModelViewSet):
    model = Attendance
    permission_classes = (IsAuthenticated, )
    serializer_class = AttendenceSerializer
    queryset = Attendance.objects.all()

    def get_queryset(self):
        queryset = super(AttendenceDetail, self).get_queryset()
        if self.request.GET.get('date') and self.request.GET.get('student_class'):
            return queryset.filter(created__startswith = self.request.GET.get('date'), student_class = self.request.GET.get('student_class'))