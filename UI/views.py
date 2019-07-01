import math
import datetime
import threading
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import TruncDay
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import CvForm, UserForm, UserProfileForm
from .ijorms.final import main
from .ijorms.ranking import ranking
from .models import Applicant, Job, JobApplicant
import numpy as np

# For plotting and visualizations
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.models.widgets import Panel, Tabs


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        availJobs = Job.objects.filter(deadline__gt=timezone.now())
        finishedJobs = Job.objects.filter(deadline__lt=timezone.now())
        applicants = Applicant.objects.all()

        jobs = Job.objects.all()
        now = datetime.datetime.now()
        applicant = Applicant.objects.get(applicant=request.user)

        applWithResume = []
        for i in Applicant.objects.all():
            if i.resume:
                applWithResume.append(i)

        context = {
            'user': request.user,
            'jobs': jobs,
            'availJobs': availJobs,
            'finishedJobs': finishedJobs,
            'applicants': applicants,
            'now': now,
            'applicant' : applicant,
            'applWithResume': applWithResume,
        }
        return render(request, 'home.html', context)


def search(request):
    applicant = Applicant.objects.get(applicant=request.user)
    query = request.POST.get('q', '')
    if query:
        qset = (
            Q(company__icontains=query)|
            Q(title__icontains=query)|
            Q(category__icontains=query)|
            Q(skills__icontains=query)
        )
        print(qset)

        jobs = Job.objects.filter(qset)

    else:
        jobs = []
    now = timezone.now()
    return render(request, 'search.html', {'jobs': jobs, 'query': query, 'now' : now, 'applicant' : applicant})


def logout_user(request):
    logout(request)
    return redirect('index')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'error_message':'Account Deactivated'})
        else:
            return render(request, 'login.html', {'error_message':'Login Invalid'})
    return render(request, 'login.html')



def register(request):
    form1 = UserForm(request.POST or None, request.FILES or None)
    form2 = UserProfileForm(request.POST or None, request.FILES or None)
    if form1.is_valid() and form2.is_valid:
        user = form1.save(commit=False)
        username = form1.cleaned_data['username']
        password = form1.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = form2.save(commit=False)
        profile.applicant = user
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                profile.save()
                return redirect('index')
    context = {'form1': form1, 'form2': form2}
    return render(request, 'register.html', context)



def vitae(request, update):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        instance = Applicant.objects.get(applicant=request.user)
        form = CvForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.resume = request.FILES['resume']
            file_type = cv.resume.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in ['pdf','doc','docx']:
                context = {
                    'form': form,
                    'error_message': 'File must in PDF or doc or docx',
                }
                return render(request, 'submit_cv.html', context)
            cv.save()
            t = threading.Thread(target=populateResumetoDb, args=(request,))
            t.daemon = True
            t.start()
            return redirect('index')

        applicant = Applicant.objects.get(applicant = request.user)
        if applicant.resume:
            if update == '0':
                resume_data = open(applicant.resume.path, 'rb').read()
                return HttpResponse(resume_data, content_type="application/pdf")
            else:
                context = {
                    'form': form,
                    'applicant': applicant
                }
                return render(request, 'submit_cv.html', context)
        else:
            context = {
                'form': form,
                'applicant': applicant
            }
            return render(request, 'submit_cv.html', context)


def details(request,id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        applied = False
        job = Job.objects.get(id=id)

        appliers = JobApplicant.objects.filter(job=job)

        byDate = JobApplicant.objects.filter(job=job).annotate(date=TruncDay('appliedAt'))
        final = byDate.values('date').annotate(appCount=Count('applicant'))

        x = []
        y = []

        for i in final:
            x.append(str(i['date'].date()))
            y.append(i['appCount'])

        title = "Applier's Trends"

        p = figure(x_range=x,
                   plot_width=760,
                   plot_height=400,
                   title="Applier's Trend",
                   x_axis_label="Time",
                   y_axis_label="No. of Appliers")

        p.title.text_font_size = "18px"
        p.circle(x, y, size=10, color="navy", alpha=0.5)

        script, div = components(p)

        applicant = Applicant.objects.get(applicant=request.user)
        try:
            alappliers = JobApplicant.objects.get(job=job, applicant=applicant)
            if applicant == alappliers.applicant:
                applied = True
        except:
            print("jpt")


        allapp = JobApplicant.objects.filter(job=job).order_by('rank')
        now = timezone.now()

    context = {
            'user':request.user,
            'job': job,
            'applicant' : applicant,
            'appliers': appliers,
            'applied' : applied,
            'allapp' : allapp,
            'script':script,
            'div':div,
            'now':now,
        }
    return render(request, 'details.html', context)


def add(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        user = request.user
        if request.method == 'POST':
            if request.is_ajax():
                cuser = request.POST.get('cuser',False)
                if user == User.objects.get(username=cuser):
                    applied_job_id = request.POST.get('job',False)
                    applied_job = Job.objects.get(id=applied_job_id)
                    applic = Applicant.objects.get(applicant=user)
                    currentStatus = JobApplicant.objects.filter(job=applied_job)
                    currentApplicants = []
                    for pp in currentStatus:
                        currentApplicants.append(pp.applicant.id)
                    if applic.id not in currentApplicants:
                        jobapplicant = JobApplicant(job=applied_job, applicant=applic)
                        t = threading.Thread(target=ranking, args=(jobapplicant, applic, applied_job))
                        t.daemon = True
                        t.start()
                    return JsonResponse({'data':applied_job_id})
                return JsonResponse({'data':"users not same"})
        return JsonResponse({'data':"not post"})



def stats(request):
    jobs = Job.objects.all()
    users = Applicant.objects.all()

    x = np.arange(0,10,0.1)
    y = [math.sin(x) for x in np.arange(0,10,0.1)]

    source = ColumnDataSource(data=dict(
        x = x,
        y = y))   
    
    title = 'y = f(x)'

    hover1 = HoverTool(tooltips=[
        ("(x,y)","($x, $y)"),
    ])

    hover2 = HoverTool(tooltips=[
        ("(x,y)","($x, $y)"),
    ])

    p1 = figure(title = title, 
                  x_axis_label="X",
                  y_axis_label="Y", 
                  tools=[hover1,"pan,wheel_zoom,box_zoom,reset,save"],
                  plot_width=800,
                  plot_height=500,
                  responsive=False,
                  toolbar_location='below',
                  logo=None)
    
    p2 = figure(title = title, 
                  x_axis_label="X",
                  y_axis_label="Y", 
                  tools=[hover2,"pan,wheel_zoom,box_zoom,reset,save"],
                  plot_width=800,
                  plot_height=500,
                  responsive=False,
                  toolbar_location='below',
                  logo=None)



    p1.circle('x', 'y', line_width=2, source=source,)
    tab1 = Panel(child=p1, title='circle')

    p2.line('x', 'y', line_width=2, source=source,)
    tab2 = Panel(child=p2, title='line')

    tabs = Tabs(tabs=[tab1, tab2],)

    script, div = components(tabs)

    return render(request, 'stats.html', {'jobs':jobs, 'users':users, 'script':script, 'div':div,})


def populateResumetoDb(request, ):
    user = request.user
    applicant = Applicant.objects.get(applicant = user)
    resume = applicant.resume

    extractedSkills, ontologySkill, extractedWorkExp, ontologyWorkExperience, extractedEducation, extractedCert, linksCertification = main(resume.path)
    applicant_skills = ''
    for skills in extractedSkills:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_skills += temp[:-2]+'\n'
    applicant_workExp = ''
    for skills in extractedWorkExp:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_workExp += temp[:-2] + '\n'

    applicant_certs = ''
    for skills in extractedCert:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_certs += temp[:-2] + '\n'

    link_cert = ''
    for li in linksCertification:
        link_cert += li + ' '
    link_cert = link_cert[:-1]

    applicant_Edu = ''
    for skills in extractedEducation:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_Edu += temp[:-2] + '\n'

    applicant.applicant_Skill = applicant_skills
    applicant.skill_ontology = str(ontologySkill)
    applicant.applicant_WorkExp = applicant_workExp
    applicant.work_experience_ontology = str(ontologyWorkExperience)
    applicant.applicant_Cert = applicant_certs
    applicant.certification_link = link_cert
    applicant.applicant_Edu = applicant_Edu

    applicant.save()


def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        cuser = request.user
        applicant = Applicant.objects.get(applicant = cuser)
        jobs_applied_remain = JobApplicant.objects.filter(applicant__applicant = cuser, job__deadline__gt = timezone.now())
        jobs_applied_finished = JobApplicant.objects.filter(applicant__applicant = cuser, job__deadline__lt = timezone.now())
        for job in jobs_applied_finished:
            print(job.skillScore, job.educationScore, job.workExpScore, job.certificationScore)
        context = {
            'jobs_applied_remain':jobs_applied_remain,
            'jobs_applied_finished':jobs_applied_finished,
            'applicant' : applicant,
        }
        return render(request, 'dashboard.html', context)