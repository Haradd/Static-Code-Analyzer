from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage

from .models import Report
from .forms import UserForm
from .functions import analyze, make_pdf

import os


def reports(request):
    if not request.user.is_authenticated():
        return render(request, 'analyzer/login.html')
    else:
        reports_list = Report.objects.filter(user=request.user).order_by('-date')
        return render(request, 'analyzer/reports.html', {'reports_list': reports_list})


def upload_form(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if request.method == 'POST' and request.FILES.getlist('pyfiles'):

        #project name input validation
        for report in Report.objects.all():
            if report.name == request.POST['project-name']:
                return render(request, 'analyzer/upload.html', {
                    'error_message': 'Project already exists, try another name',
                })

        #.py files validation
        for file in request.FILES.getlist('pyfiles'):
            if file.name[-3:] != '.py':
                print(file.name)
                return render(request, 'analyzer/upload.html', {
                    'error_message': 'Please select only python files',
                })

        #checkers selection
        checker_options = ','.join(request.POST.getlist('checker_option'))
        if checker_options == '':  #if user didn't chose any option, take all
            checker_options = 'W,E,F'
        maccabe_complexity = ','.join(request.POST.getlist('maccabe-option'))
        options = ['--count', '--max-complexity={}'.format(maccabe_complexity), '--select C,{}'.format(checker_options), '--statistics', '--format=pylint']

        # save and analyze each uploaded file
        fs = FileSystemStorage()
        for file in request.FILES.getlist('pyfiles'):
            path = fs.save('files/{}'.format(file.name), file)
            path = 'media/' + path
            analyze(path, options)

        name = request.POST['project-name']
        report_txt = BASE_DIR + '/media/report.txt'
        report_pdf = BASE_DIR + '/media/reports/' + name + '.pdf'
        media_path = 'media/files/'
        make_pdf(report_txt, report_pdf, media_path, name)

        os.remove('media/report.txt')
        #save report to database
        report = Report()
        report.name = name
        report.file = '/media/reports/' + name + '.pdf'
        if request.user.is_authenticated:
            report.user = request.user
        report.save()

        print(Report.objects.all())
        #clear python files Storage
        for file in request.FILES.getlist('pyfiles'):
            fs.delete('files/{}'.format(file.name))


        return render(request, 'analyzer/upload.html', {
                'report': report.file
            })

    return render(request, 'analyzer/upload.html')


def register_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                reports_list = Report.objects.filter(user=request.user)
                return render(request, 'analyzer/reports.html', {'reports_list': reports_list})
    return render(request, 'analyzer/register.html', {"form": form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                reports_list = Report.objects.filter(user=request.user).order_by('-date')
                return render(request, 'analyzer/reports.html', {'reports_list': reports_list})
            else:
                return render(request, 'analyzer/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'analyzer/login.html', {'error_message': 'Invalid login'})
    return render(request, 'analyzer/login.html')


def logout_user(request):
    logout(request)

    return render(request, 'analyzer/upload.html')