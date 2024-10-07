import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def parent_home(request):
    parent = Parent.objects.filter(admin=request.user).first()
    context = {
        'page_title': 'Parent Portal - ' + str(parent.admin.last_name),
      
    }
    return render(request, 'parent_template/home_content.html', context)
#
def view_report(request):
    parent = Parent.objects.filter(admin=request.user).first()
    results = StudentResult.objects.filter(student=parent.student).values('subject__name', 'test', 'exam')

    return render(request, 'parent_template/report.html', {"results": results})



import numpy as np 
import json
from django.shortcuts import render
from .models import AttendanceReport, StudentResult, Parent


def view_graph(request):
    parent = Parent.objects.filter(admin=request.user).first()
    student = parent.student

    attendance_reports = AttendanceReport.objects.filter(student=student).select_related('attendance')
    results = StudentResult.objects.filter(student=student).order_by('created_at')

    # Prepare data for the chart
    attendance_data = {
        "labels": [report.attendance.date.strftime('%Y-%m-%d') for report in attendance_reports],
        "statuses": [report.status for report in attendance_reports],
    }

    marks_data = {
        "dates": [result.created_at.strftime('%Y-%m-%d') for result in results],
        "marks": [result.exam for result in results],
    }


    # Ensure there is data to work with
    if attendance_reports.exists() and results.exists():
        # Calculate features
        attendance_rate = np.mean([report.status for report in attendance_reports])
        homework_completion = np.mean([result.exam for result in results])
        previous_exam_scores = results.last().exam  # Most recent exam score

        # Normalize features
        features = np.array([attendance_rate, homework_completion, previous_exam_scores])
        mean = np.mean(features)
        std = np.std(features)
        normalized_features = (features - mean) / std

        # Combine features into a single matrix
        X = np.array([normalized_features])
        y = np.array([result.exam for result in results])

        # Add a column of ones to X for the intercept term
        X = np.hstack([np.ones((X.shape[0], 1)), X])

        # Initialize weights
        theta = np.zeros(X.shape[1])

        # Hyperparameters
        learning_rate = 0.001  # Adjusted learning rate
        iterations = 1000

        # Cost function
        def compute_cost(X, y, theta):
            m = len(y)
            predictions = X.dot(theta)
            cost = (1 / (2 * m)) * np.sum(np.square(predictions - y))
            return cost

        # Gradient descent
        def gradient_descent(X, y, theta, learning_rate, iterations):
            m = len(y)
            cost_history = np.zeros(iterations)

            for i in range(iterations):
                predictions = X.dot(theta)
                theta = theta - (1 / m) * learning_rate * (X.T.dot(predictions - y))
                cost_history[i] = compute_cost(X, y, theta)

            return theta, cost_history

        # Train the model
        theta, cost_history = gradient_descent(X, y, theta, learning_rate, iterations)

        # Make a prediction
        new_student_data = np.array([normalized_features])
        new_student_data = np.hstack([np.ones((new_student_data.shape[0], 1)), new_student_data])
        predicted_score = new_student_data.dot(theta)[0]

        # Combine both attendance and marks data into one dictionary
        data = {
            "attendance": attendance_data,
            "marks": marks_data,
            "predicted_score": predicted_score,
        }

    else:
        # Handle the case where there are no attendance reports or results
        data = {
            "attendance": attendance_data,
            "marks": marks_data,
            "predicted_score": None,
        }

    # Convert Python data to JSON
    json_data = json.dumps(data)

    return render(request, 'parent_template/graph.html', {"data": json_data,'predicted_score':predicted_score})


# def view_graph(request):
#     parent = Parent.objects.filter(admin=request.user).first()
#     student = parent.student
#
#     attendance_reports = AttendanceReport.objects.filter(student=student).select_related('attendance')
#     results = StudentResult.objects.filter(student=student).order_by('created_at')
#
#     # Prepare data for the chart
#     attendance_data = {
#         "labels": [report.attendance.date.strftime('%Y-%m-%d') for report in attendance_reports],
#         "statuses": [report.status for report in attendance_reports],
#     }
#
#     marks_data = {
#         "dates": [result.created_at.strftime('%Y-%m-%d') for result in results],
#         "marks": [result.exam for result in results],
#     }
#
#     # Combine both attendance and marks data into one dictionary
#     data = {
#         "attendance": attendance_data,
#         "marks": marks_data,
#     }
#
#     # Convert Python data to JSON
#     json_data = json.dumps(data)
#
#     return render(request, 'parent_template/graph.html', {"data": json_data})

def parent_due(request):
    if request.method=='POST':
        try:
            stud = request.POST.get('student')
            parent = get_object_or_404(Parent, admin=request.user)
            student = Student.objects.all().filter(username=stud)
            print(student)
            field_name1 = 'student_fee'
            field_name2 = 'student_fee_paid'
            obj = Student.objects.filter(username=stud).first()
            field_value1 = getattr(obj, field_name1)
            field_value2 = getattr(obj, field_name2)
            tot = field_value1 - field_value2
        
        
        
        
        
            context = {
                'page_title': 'Parent Portal',
                'student' : student,
                'tot':tot
            }
            return render(request, 'parent_template/parent_due.html', context)
        except Exception as e:
            messages.error(request, "Admin not Updated Student Fee details " + str(e))
            return render(request, 'parent_template/parent_due.html')
    return render(request, 'parent_template/parent_due.html')