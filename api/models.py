from django.db import models
from accounts.models import Teacher
from multiselectfield import MultiSelectField
# Create your models here.

class Batch(models.Model):
	MORNING = 0
	EVENING = 1
	shifts = (
		(MORNING, 'Morning'),
		(EVENING, 'Evening'),
	)

	name    = models.CharField(max_length=120)
	shift   = models.PositiveIntegerField(choices=shifts)
	session = models.CharField(max_length=50)

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Batch"

	def __unicode__(self):
		return self.name	

class Student(models.Model):
	batch = models.ForeignKey(Batch, related_name="class_students")
	name = models.CharField(max_length=50)
	rollno = models.IntegerField()

	dated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name


class Course(models.Model):
	teacher = models.ManyToManyField(Teacher)
	course_name = models.CharField(max_length=50)
	course_code = models.CharField(max_length=8)

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.course_name



class StudentClass(models.Model):

	MONDAY = 0
	TUESDAY = 1
	WEDNESDAY = 2
	THURSDAY = 3
	FRIDAY = 4
	SATURDAY = 5
	SUNDAY = 6

	days = (
		(MONDAY, 'Monday'),
		(TUESDAY, 'Tuesday'),
		(WEDNESDAY, 'Wednesday'),
		(THURSDAY, 'Thursday'),
		(FRIDAY, 'Friday'),
		(SATURDAY, 'Saturday'),
		(SUNDAY, 'Sunday')
	)

	batch = models.ForeignKey(Batch, related_name="classes")
	course = models.ForeignKey(Course)

	start_timing  =  models.DateTimeField()
	end_timing    =  models.DateTimeField()
	class_days = MultiSelectField(choices=days, max_length=20)

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "student class"

	def __unicode__(self):
		return self.course.course_name


class Attendance(models.Model):
	student = models.ForeignKey(Student)
	student_class = models.ForeignKey(StudentClass)

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.student.name