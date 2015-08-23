from django.contrib import admin

# Register your models here.
from .models import Student, StudentClass, Course, Attendance, Batch

class BatchAdmin(admin.ModelAdmin):
	list_filter = ('name',)
	list_display = ('name','shift',)

class StudentAdmin(admin.ModelAdmin):
	list_filter = ('name',)
	list_display = ('name', 'rollno','batch',)

class StudentClassAdmin(admin.ModelAdmin):
	list_filter = ('batch',)
	list_display = ('batch','course')

class CourseAdmin(admin.ModelAdmin):
	list_filter = ('course_name',)
	list_display = ('course_name','course_code',)

class AttendanceAdmin(admin.ModelAdmin):
	list_filter = ('student',)
	list_display = ('student','student_class',)

admin.site.register(Batch, BatchAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentClass,StudentClassAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Attendance,AttendanceAdmin)