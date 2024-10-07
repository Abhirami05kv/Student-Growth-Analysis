import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def hod2_home(request):
    staff = get_object_or_404(hod2, admin=request.user)

    total_students = Student.objects.filter(course=staff.course).count()
    # total_leave = LeaveReportStaff.objects.filter(staff=staff).count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name)
        attendance_list.append(attendance_count)
    context = {
        'page_title': 'Staff Panel - ' + str(staff.admin.last_name) + ' (' + str(staff.course) + ')',
        'total_students': total_students,
        'total_attendance': total_attendance,
        'total_leave': 0,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list}

    return render(request, 'hod2_template/home_content.html', context)
def manage_staff_hod2(request):
    if request.method=='POST':
        dept = request.POST.get('departement')
        allStaff = CustomUser.objects.filter(user_type=2)
        course = Staff.objects.filter(course__name__startswith=dept)
        mylist = zip(course,allStaff)
        print(allStaff)
        context = {
            'mylist': mylist,
            'page_title': 'View Staff'
        }
        return render(request, "hod2_template/manage_staff_hod2.html", context)
    return render(request, "hod2_template/manage_staff_hod2.html")

def hod2_take_attendance(request):
    if request.method=='POST':
        dept = request.POST.get('departement')
        allStaff = Staff.objects.filter(course__name__startswith=dept)
        aform=AttendanceStaffForm()
        if request.method=='POST':
            form=AttendanceStaffForm(request.POST)
            if form.is_valid():
                Attendances=request.POST.getlist('present_status')
                date=form.cleaned_data['date']
                for i in range(len(Attendances)):
                    AttendanceModel=AttendanceStaff()
                #AttendanceModel.cl=cl
                    AttendanceModel.date=date
                    AttendanceModel.present_status=Attendances[i]
                #AttendanceModel.course=allStaff[i].course
                    AttendanceModel.save()
                return redirect('hod2_take_attendance')
            else:
                print('form invalid')
        print(aform)
        mylist = zip(allStaff, aform)
        return render(request,'hod2_template/hod2_take_attendance.html',{'mylist':mylist,'staffs':allStaff,'aform':aform})
    return render(request,'hod2_template/hod2_take_attendance.html')
#return render(request,'hod2_template/hod2_take_attendance.html',{'staffs':allStaff,'aform':aform})

# def hod2_view_attendance(request):
#     form=AskDateForm()
#     if request.method=='POST':
#         form=AskDateForm(request.POST)
#         if form.is_valid():
#             date=form.cleaned_data['date']
#             attendancedata=AttendanceStaff.objects.all().filter(date=date,cl=cl)
#            # studentdata=models.StudentExtra.objects.all().filter(cl=cl)
#             mylist=zip(attendancedata)
#             return render(request,'hod2_template/hod2_view_dateask.html',{'mylist':mylist,'date':date})
#         else:
#             print('form invalid')
#     return render(request,'hod2_template/hod2_take_attendance.html',{'form':form})
def hod2_view_attendance(request):
    form=AskDateForm()
    if request.method=='POST':
        form=AskDateForm(request.POST)
        if form.is_valid():
            print("formok")
            date=form.cleaned_data['date']
            dept=request.POST.get('departement')
            attendancedata=AttendanceStaff.objects.all().filter(date=date)
            studentdata=CustomUser.objects.filter(user_type=2)
            course = Staff.objects.filter(course__name__startswith=dept)
            print(studentdata)
            print(attendancedata)
            print(course)

            mylist = zip(course, attendancedata)
            context = {
            'mylist': mylist,
            'date':date,
                }
            return render(request,'hod2_template/hod2_view_attendance_page.html',context)
        else:
            print('form invalid')
    return render(request,'hod2_template/hod2_view_dateask.html',{'form':form})

def hod2_searchdept(request):
    if request.method =="POST":
        data = request.POST
        dept = request.POST.get('departement')
        j = str(dept)
        print(j)
        course = Staff.objects.filter(course__name__startswith=j)
        aform=AttendanceStaffForm()
        return render(request,'hod2_template/hod2_take_search.html',{'course':course})
        
    else:
        print("not ok")
        return render(request,'hod2_template/home_content.html')
