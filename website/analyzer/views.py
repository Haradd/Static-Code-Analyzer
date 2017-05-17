from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from .models import Report
from .functions import analyze, make_pdf

import os




def reports(request):
    reports_list = Report.objects.all()
    context = {'reports_list': reports_list}
    return render(request, 'analyzer/reports.html', context)


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
        print(maccabe_complexity)
        options = ['--count', '--max-complexity={}'.format(maccabe_complexity), '--select C,{}'.format(checker_options), '--statistics', '--format=pylint']
        print(request.POST.getlist('checker_option'))

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
        report.save()

        print(Report.objects.all())
        #clear python files Storage
        for file in request.FILES.getlist('pyfiles'):
            fs.delete('files/{}'.format(file.name))


        return render(request, 'analyzer/upload.html', {
                'report': report_pdf
            })

    return render(request, 'analyzer/upload.html')
