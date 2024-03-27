from django.urls import path
from .views import (
    login, 
    index,
    student,
    acc_setting, 
    logout,
    book_hostel,
    room_details,
    log_activity,
    student_profile, 
    admin_dashboard,
    admin_profile,
    admin_view_students_acc,
    admin_register_students_acc,
    admin_view_booking,
    admin_manage_students,
    admin_manage_rooms,
    admin_manage_courses,
    administrator_acc_setting
    )
from . import api
urlpatterns=[
    path('login/', login, name="Login"),
    path('logout/', logout, name="Logout"),
    path('', index, name="Home_Page"),
    path('student/dashboard/', student, name="Home_Page"),
    path('student/acc-setting/', acc_setting, name="acc_setting"),
    path('student/book-hostel/', book_hostel, name="book_hostel"),
    path('student/room-details/', room_details, name="room_details"),
    path('student/log-activity/', log_activity, name='log_activity'),
    path('student/profile/', student_profile, name='student_profile'),
    path('check_email/', api.check_email, name='check_email'),
    path('check_password/', api.check_password, name='check_password'),
    path('check_room/', api.check_room, name='check_room'),


    path('administrator/dashboard/', admin_dashboard, name="Admin page_Page"),
    path('administrator/profile/', admin_profile, name="admin_profile_Page"),
    path('administrator/register-student/', admin_register_students_acc, name="admin_register_students_acc"),
    path('administrator/view-students-acc/', admin_view_students_acc, name="admin_view_students_acc"),
    path('administrator/bookings/', admin_view_booking, name="administrator_bookings"),
    path('administrator/manage-students/', admin_manage_students, name="administrator_manage_students"),
    path('administrator/manage-rooms/', admin_manage_rooms, name="administrator_manage_rooms"),
    path('administrator/manage-courses/', admin_manage_courses, name="administrator_manage-courses"),
    path('administrator/acc-setting/', administrator_acc_setting, name="administrator_manage-courses"),


]