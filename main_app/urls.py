"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from main_app.EditResultView import EditResultView

from . import hod_views, staff_views, student_views, views,hod2_views,parent_views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    #
    path("parentregister", hod_views.add_parent, name='parentregister'),
    path("staffregister", hod_views.staffregister, name='staffregister'),
    path("studentregister", hod_views.add_student, name='studentregister'),
    
    
    path("approveleev", hod_views.approveleev, name='approveleev'),
    
    

    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.approve_staff, name='add_staff'),
    path("hod/add", hod_views.add_hod, name='add_hod'),
    path("parent/add", hod_views.approve_parent, name='add_parent'),
    path("course/add", hod_views.add_course, name='add_course'),
    path("send_student_notification/", hod_views.send_student_notification,
         name='send_student_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("add_session/", hod_views.add_session, name='add_session'),
    path("admin_notify_student", hod_views.admin_notify_student,
         name='admin_notify_student'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", hod_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         hod_views.edit_session, name='edit_session'),
    path("student/view/feedback/", hod_views.student_feedback_message,
         name="student_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
path("parent/view/feedback/", hod_views.parent_feedback_message,
         name="parent_feedback_message",),
    path("view_student_leave", hod_views.view_student_leave,
         name="view_student_leave",),
    path("staff/view/leave/", hod_views.view_staff_leave, name="view_staff_leave",),
    path("attendance/view/", hod_views.admin_view_attendance,
         name="admin_view_attendance",),
    path("attendance/fetch/", hod_views.get_admin_attendance,
         name='get_admin_attendance'),
    path("student/add/", hod_views.approve_student, name='add_student'),
    path("subject/add/", hod_views.add_subject, name='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("hod/manage/", hod_views.manage_hod, name='manage_hod'),

    path("staff/manage/hod2", hod2_views.manage_staff_hod2, name='manage_staff_hod2'),
    path("student/manage/", hod_views.manage_student, name='manage_student'),

    path("parent/manage/", hod_views.manage_parent, name='manage_parent'),


    path("course/manage/", hod_views.manage_course, name='manage_course'),
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("view_dept/", hod_views.view_dept, name='view_dept'),
    path("view_dept_students/<int:id>", hod_views.view_dept_students, name='view_dept_students'),
    path("view_dept_teachers/<int:id>", hod_views.view_dept_teachers, name='view_dept_teachers'),

    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),

    path("hod/edit/<int:staff_id>", hod_views.edit_hod, name='edit_hod'),
    path("hod/delete/<int:staff_id>",
         hod_views.delete_hod, name='delete_hod'),

    path("course/delete/<int:course_id>",
         hod_views.delete_course, name='delete_course'),

    path("subject/delete/<int:subject_id>",
         hod_views.delete_subject, name='delete_subject'),

    path("session/delete/<int:session_id>",
         hod_views.delete_session, name='delete_session'),

    path("student/delete/<int:student_id>",
         hod_views.delete_student, name='delete_student'),
    path("student/edit/<int:student_id>",
         hod_views.edit_student, name='edit_student'),
    path("course/edit/<int:course_id>",
         hod_views.edit_course, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         hod_views.edit_subject, name='edit_subject'),


    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),
     path("hod/home/", hod2_views.hod2_home, name='hod2_home'),
      path("parent/home/", parent_views.parent_home, name='parent_home'),

    path("parent/view_graph/", parent_views.view_graph, name='view_graph'),
    path('parent/report/', parent_views.view_report, name='view_report'),

    path('upload_materials/', staff_views.upload_materials, name='upload_materials'),
    path('pdf_list', staff_views.pdf_list, name='pdf_list'),
    path('pdf/<int:pk>/', staff_views.pdf_detail, name='pdf_detail'),
    path('pdf_parent/<int:pk>/', staff_views.pdf_detail_parent, name='pdf_detail_parent'),

    path('upload_assignments/', staff_views.upload_assignment, name='upload_assignments'),
    path('assignment_list', staff_views.assignment_list, name='assignment_list'),
    path('assignment_list_stu', staff_views.assignment_list_stu, name='assignment_list_stu'),

    path('assignment_list_parent', staff_views.assignment_list_parent, name='assignment_list_parent'),

    path('assignment/<int:pk>/', staff_views.assignment_detail, name='assignment_detail'),
    path('assignment/edit/<int:pk>/', staff_views.edit_assignment, name='edit_assignment'),
    path('assignment/edit_stu/<int:pk>/', staff_views.edit_assignmentstu, name='edit_assignmentstu'),


    path('upload_tt/', staff_views.upload_tt, name='upload_tt'),
    path('tt_list', staff_views.tt_list, name='tt_list'),
    path('tt/<int:pk>/', staff_views.tt_detail, name='tt_detail'),

    path('students/', hod_views.student_list, name='student_list'),
    path('report/<int:student_id>/', hod_views.view_report, name='view_report_admin'),

    path("parent/due/", parent_views.parent_due, name='parent_due'),
     #path("hod/dept/search", hod2_views.hod2_searchdept, name='searchdept'),
    path("staff/apply/leave/", staff_views.staff_apply_leave,
         name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),

    path("parent/feedback/", staff_views.parent_feedback, name='parent_feedback'),

    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path("staff/attendance/take/", staff_views.staff_take_attendance,
         name='staff_take_attendance'),
     path("hod2/attendance/take/", hod2_views.hod2_take_attendance,
         name='hod2_take_attendance'),
     path("hod2/attendance/view/", hod2_views.hod2_view_attendance,
         name='hod2_view_attendance'),
    path("staff/attendance/update/", staff_views.staff_update_attendance,
         name='staff_update_attendance'),
    path("staff/get_students/", staff_views.get_students, name='get_students'),
    path("staff/attendance/fetch/", staff_views.get_student_attendance,
         name='get_student_attendance'),
    path("staff/attendance/save/",
         staff_views.save_attendance, name='save_attendance'),
    path("staff/attendance/update/",
         staff_views.update_attendance, name='update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),
    path("staff/result/add/", staff_views.staff_add_result, name='staff_add_result'),
    path("staff/result/edit/", EditResultView.as_view(),
         name='edit_student_result'),
    path('staff/result/fetch/', staff_views.fetch_student_result,
         name='fetch_student_result'),



    # Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student/view/attendance/", student_views.student_view_attendance,
         name='student_view_attendance'),
    path("student/apply/leave/", student_views.student_apply_leave,
         name='student_apply_leave'),
    path("student/feedback/", student_views.student_feedback,
         name='student_feedback'),
    path("student/view/profile/", student_views.student_view_profile,
         name='student_view_profile'),
    path("student/fcmtoken/", student_views.student_fcmtoken,
         name='student_fcmtoken'),
    path("student/view/notification/", student_views.student_view_notification,
         name="student_view_notification"),
    path('student/view/result/', student_views.student_view_result,
         name='student_view_result'),

]
