from django.contrib import admin
from .models import Attendance, Farmer, Student


class AttendanceInline(admin.TabularInline):
	model = Attendance
	extra = 0
	fields = ("date", "is_present", "check_in_time", "check_out_time", "remarks")


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
	list_display = ("name", "farm", "age", "phone_number", "email")
	search_fields = ("name", "farm", "phone_number", "email")
	list_filter = ("farm",)
	inlines = [AttendanceInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
	list_display = ("farmer", "date", "is_present", "check_in_time", "check_out_time")
	list_filter = ("date", "is_present")
	search_fields = ("farmer__name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ("name", "school", "age", "phone_number", "email")
	search_fields = ("name", "school", "phone_number", "email")
	list_filter = ("school",)
