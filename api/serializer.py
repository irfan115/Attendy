from rest_framework import serializers
from api.models import Student, StudentClass, Course, Attendance, Batch
from accounts.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teacher
		fields = ('pk','first_name','last_name','email')

class BatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Batch
		fields = ('pk', 'name', 'shift', 'session')


class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = ('name','rollno')


class CourseSerializer(serializers.ModelSerializer):
	teacher = TeacherSerializer(many=True, read_only=True)
	class Meta:
		model = Course
		fields = ('pk','course_name','course_code','teacher',)

class StudentClassSerializer(serializers.ModelSerializer):
	
	batch = BatchSerializer(read_only=True)
	#student = StudentSerializer(many=True, read_only=True)
	course = CourseSerializer(read_only=True)
	class Meta:
		model = StudentClass
		fields = ('pk','batch', 'course', 'start_timing','end_timing', 'class_days')

class StudentSearchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = ('pk','name', 'rollno')


class AttendenceSaveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Attendance
		fields = ('student','student_class')


class AttendenceSerializer(serializers.ModelSerializer):
	student = StudentSerializer(read_only=True)
	class Meta:
		model = Attendance
		fields = ('student','student_class')