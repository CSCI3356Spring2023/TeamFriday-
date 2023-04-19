from django.contrib import admin
from .models import User, Student, Instructor, Admin, Application, Course, Semester

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Application)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Admin)
