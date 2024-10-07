import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
from django.core.mail import send_mail

def send_email_view(email):
    subject = f'Attendance!'
    message = f'you are absent today!.'
    email_from = 'your_email@example.com'
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse('Email sent successfully!')

def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_students = Student.objects.filter(course=staff.course).count()
    total_leave = LeaveReportStaff.objects.filter(staff=staff).count()
    subjects = Subject.objects.filter(staff=staff)
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
        'total_leave': total_leave,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list
    }
    return render(request, 'staff_template/home_content.html', context)


def staff_take_attendance(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff_id=staff)
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'Take Attendance'
    }

    return render(request, 'staff_template/staff_take_attendance.html', context)


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        students = Student.objects.filter(
            course_id=subject.course.id, session=session)
        student_data = []
        for student in students:
            data = {
                    "id": student.id,
                    "name": student.admin.last_name + " " + student.admin.first_name
                    }
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e

from .forms import PDFUploadForm,AssignmentsForm,TimeTableForm
from django.shortcuts import render, get_object_or_404

from .models import PDFDocument,Assignments,TimeTable
def upload_materials(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list')
    else:
        form = PDFUploadForm()
    return render(request, 'staff_template/upload_pdf.html', {'form': form})
def pdf_list(request):
    documents = PDFDocument.objects.all()
    return render(request, 'staff_template/pdf_list.html', {'documents': documents})


# myapp/views.py



def pdf_detail(request, pk):
    print(pk)
    print()
    document = get_object_or_404(PDFDocument, pk=pk)
    print(document)
    return render(request, 'staff_template/pdf_detail.html', {'document': document})

def pdf_detail_parent(request, pk):
    print(pk)
    print()
    document = get_object_or_404(Assignments, pk=pk)
    print(document)
    return render(request, 'staff_template/pdf_detail.html', {'document': document})


def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentsForm(request.POST, request.FILES)
        if form.is_valid():
            staff_value=form.save(commit=False)
            print(staff_value)
            staff_value.staff=Staff.objects.filter(admin=request.user).first()
            staff_value.save()
            return redirect('assignment_list')
    else:
        form = AssignmentsForm()
    return render(request, 'staff_template/upload_pdf.html', {'form': form})
def assignment_list(request):
    documents = Assignments.objects.filter(staff__admin=request.user)
    return render(request, 'staff_template/pdf_list.html', {'documents': documents})


# myapp/views.py

def assignment_list_parent(request):
    student=Parent.objects.filter(admin=request.user).first().student
    print(student)
    documents = Assignments.objects.filter(student=student)
    print(documents)
    return render(request, 'staff_template/pdf_list.html', {'documents': documents})
def assignment_list_stu(request):
    documents = Assignments.objects.filter(student__admin=request.user)
    return render(request, 'staff_template/pdf_list.html', {'documents': documents})
def edit_assignmentstu(request, pk):
    assignment = get_object_or_404(Assignments, pk=pk)
    if request.method == 'POST':
        form = AssignmentsFormstu(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_list_stu')
    else:
        form = AssignmentsFormstu(instance=assignment)
    return render(request, 'staff_template/edit_pdf.html', {'form': form, 'assignment': assignment})


def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignments, pk=pk)
    if request.method == 'POST':
        form = AssignmentsForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentsForm(instance=assignment)
    return render(request, 'staff_template/edit_pdf.html', {'form': form, 'assignment': assignment})
def assignment_detail(request, pk):
    document = get_object_or_404(Assignments, pk=pk)
    return render(request, 'staff_template/pdf_detail.html', {'document': document})




def upload_tt(request):
    if request.method == 'POST':
        form = TimeTableForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tt_list')
    else:
        form = TimeTableForm()
    return render(request, 'staff_template/upload_pdf.html', {'form': form})
def tt_list(request):
    documents = TimeTable.objects.all()
    return render(request, 'staff_template/pdf_list.html', {'documents': documents})

def tt_detail(request, pk):
    document = get_object_or_404(TimeTable, pk=pk)
    return render(request, 'staff_template/pdf_detail.html', {'document': document})


@csrf_exempt
def save_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    students = json.loads(student_data)
    session = get_object_or_404(Session, id=session_id)
    subject = get_object_or_404(Subject, id=subject_id)
    attendance = Attendance(session=session, subject=subject, date=date)
    attendance.save()

    for student_dict in students:
        student = get_object_or_404(Student, id=student_dict.get('id'))
        attendance_report = AttendanceReport(student=student, attendance=attendance, status=student_dict.get('status'))
        attendance_report.save()


    return HttpResponse("OK")


def staff_update_attendance(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff_id=staff)
    sessions = Session.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'Update Attendance'
    }

    return render(request, 'staff_template/staff_update_attendance.html', context)


@csrf_exempt
def get_student_attendance(request):
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        date = get_object_or_404(Attendance, id=attendance_date_id)
        attendance_data = AttendanceReport.objects.filter(attendance=date)
        student_data = []
        for attendance in attendance_data:
            data = {"id": attendance.student.admin.id,
                    "name": attendance.student.admin.last_name + " " + attendance.student.admin.first_name,
                    "status": attendance.status}
            student_data.append(data)
        return JsonResponse(json.dumps(student_data), content_type='application/json', safe=False)
    except Exception as e:
        return e


@csrf_exempt
def update_attendance(request):
    student_data = request.POST.get('student_ids')
    date = request.POST.get('date')
    students = json.loads(student_data)
    try:
        attendance = get_object_or_404(Attendance, id=date)

        for student_dict in students:
            student = get_object_or_404(
                Student, admin_id=student_dict.get('id'))
            attendance_report = get_object_or_404(AttendanceReport, student=student, attendance=attendance)
            attendance_report.status = student_dict.get('status')
            attendance_report.save()
    except Exception as e:
        return None

    return HttpResponse("OK")


def staff_apply_leave(request):
    form = LeaveReportStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportStaff.objects.filter(staff=staff),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('staff_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_apply_leave.html", context)


def staff_feedback(request):
    form = FeedbackStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStaff.objects.filter(staff=staff),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('staff_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_feedback.html", context)


def parent_feedback(request):
    form = FeedbackParentForm(request.POST or None)
    parent = get_object_or_404(Parent, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackParent.objects.filter(parent=parent),
        'page_title': 'Add Feedback'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.parent = parent
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('parent_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_feedback.html", context)


def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(request.POST or None, request.FILES or None,instance=staff)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = staff.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                staff.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('staff_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "staff_template/staff_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "staff_template/staff_view_profile.html", context)

    return render(request, "staff_template/staff_view_profile.html", context)


@csrf_exempt
def staff_fcmtoken(request):
    token = request.POST.get('token')
    try:
        staff_user = get_object_or_404(CustomUser, id=request.user.id)
        staff_user.fcm_token = token
        staff_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def staff_view_notification(request):
    staff = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "staff_template/staff_view_notification.html", context)


def staff_add_result(request):
    staff = get_object_or_404(Staff, admin=request.user)
    subjects = Subject.objects.filter(staff=staff)
    sessions = Session.objects.all()
    context = {
        'page_title': 'Result Upload',
        'subjects': subjects,
        'sessions': sessions
    }
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_list')
            subject_id = request.POST.get('subject')
            test = request.POST.get('test')
            exam = request.POST.get('exam')
            student = get_object_or_404(Student, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)
            try:
                data = StudentResult.objects.get(
                    student=student, subject=subject)
                data.exam = exam
                data.test = test
                data.save()
                messages.success(request, "Scores Updated")
            except:
                result = StudentResult(student=student, subject=subject, test=test, exam=exam)
                result.save()
                messages.success(request, "Scores Saved")
        except Exception as e:
            messages.warning(request, "Error Occured While Processing Form")
    return render(request, "staff_template/staff_add_result.html", context)


@csrf_exempt
def fetch_student_result(request):
    try:
        subject_id = request.POST.get('subject')
        student_id = request.POST.get('student')
        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)
        result = StudentResult.objects.get(student=student, subject=subject)
        result_data = {
            'exam': result.exam,
            'test': result.test
        }
        return HttpResponse(json.dumps(result_data))
    except Exception as e:
        return HttpResponse('False')
