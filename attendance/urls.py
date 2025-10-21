from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("students/new/", views.student_create_view, name="student_create"),
    path("students/success/", views.student_success_view, name="student_success"),
    path("students/", views.student_list_view, name="student_list"),
    path("farmers/new/", views.farmer_create_view, name="farmer_create"),
    path("farmers/success/", views.farmer_success_view, name="farmer_success"),
    path("farmers/", views.farmer_list_view, name="farmer_list"),
    path("farmers/<int:pk>/update/", views.farmer_update_view, name="farmer_update"),
    path("api/farmers.json", views.farmers_json_api, name="farmers_json_api"),
    path("attendance/mark/", views.mark_attendance_view, name="mark_attendance"),
    path("attendance/", views.attendance_list_view, name="attendance_list"),
]
