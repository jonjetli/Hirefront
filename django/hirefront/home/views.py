# Create your views here.
#from django.http import HttpResponse
#from django.template import loader, Context
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from home.models import postulantes , reqlutadores, calendar_interviewed_enterprise
from django.utils.datastructures import MultiValueDictKeyError
from hirefront.forms import PostulantesForm
from django.core import mail
import random
import string

def index(request):
    result=''
    if request.method == 'POST':
        log = request.POST['login']
        if log == 'loginP':
            try:
                username = request.POST['usernameP']
                password = request.POST['passwordP']
                user = postulantes.objects.get(pk=username)
                if user.password == password:
                    return HttpResponseRedirect("/")
                else:
                    result = 'Password Incorrect'
            except postulantes.DoesNotExist:
                result = 'Not exist Interviewed'
        else:
             if log == 'loginR':
                 try:
                     username = request.POST['usernameR']
                     password = request.POST['passwordR']
                     user = reqlutadores.objects.get(pk=username)
                     if user.password == password:
                         #return HttpResponseRedirect('Perfil/calendario')
                         perfil = Perfil_calendario(request, username)
                         return perfil
                     else:
                         result = 'Password Incorrect'
                 except reqlutadores.DoesNotExist:
                     result = 'Not exist Enterprise'
    return render_to_response("index.html",{"result":result},context_instance = RequestContext(request))

def Perfil_calendario(request, email):
    estado = ''
    email_interviewed = request.POST['email']
    fecha = request.POST['fecha']
    hora = request.POST['hora']
    obs = request.POST['obs']
    if request.method == 'POST':
        objeto = calendar_interviewed_enterprise(request.POST, MultiValueDictKeyError)
        objeto.email_enterprise = email
        objeto.email_interviewed = email_interviewed
        objeto.date_interview = fecha
        objeto.time_interview = hora
        objeto.observations = obs
        #confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(32))
        #objeto.code_unique_interview = confirmation_code
        objeto.save()
    try:
        Data = reqlutadores.objects.get(pk=email)
        typeUser = 'Enterprise'
        try:
            Entrevistas = calendar_interviewed_enterprise.objects.get(email_enterprise = email)
        except (calendar_interviewed_enterprise.DoesNotExist, MultiValueDictKeyError):
            estado = 'You Dont Have Interviews'
        return render_to_response("viewEnterprise.html",{'Data':Data,"typeUser": typeUser, "estado":estado}, context_instance = RequestContext(request))
    except reqlutadores.DoesNotExist:
        Data = postulantes.objects.get(pk=email)
        typeUser = 'Interviewed'
        return render_to_response("viewInterviewed.html",{'Data': Data,"typeUser": typeUser}, context_instance = RequestContext(request))


def detalle(request, email):
    try:
        Data = reqlutadores.objects.get(pk=email)
        typeUser = 'Enterprise'
        return render_to_response("detalle.html",{'typeUser': typeUser}, context_instance = RequestContext(request))
    except reqlutadores.DoesNotExist:
        Data = postulantes.objects.get(pk=email)
        typeUser = 'Interviewed'
        return render_to_response("detalle.html",{"typeUser": typeUser}, context_instance = RequestContext(request))

def signup_interviewed(request):
    result = ''
    connection  =  mail.get_connection()
    if request.method == 'POST':
        fullname=request.POST['fullname']
        email = request.POST['email']
        id = request.POST['ID']
        cellphone = request.POST['cellphone']
        cv = request.FILES['cv']
        if( fullname == '' or email == '' or  id == '' or cellphone == ''):
            result = 'Please complete all field'
        else:
            objeto = postulantes(request.POST, request.FILES)
            objeto.Fullname = fullname
            objeto.id = id
            objeto.email = email
            objeto.number = cellphone
            objeto.cv = cv
            confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(32))
            objeto.code_validation = confirmation_code
            objeto.save()
            email_confirmation = mail.EmailMessage('Welcome', ' Welcome http://127.0.0.1/joininterviewed/' + confirmation_code , 'jonathan@hirefront.com',[email],connection=connection)
            email_confirmation.send()
            return HttpResponseRedirect("/")
    return render_to_response("signup_interviewed.html",{'result':result},context_instance=RequestContext(request))

def viewEnterprise(request):

    return render_to_response("viewEnterprise.html",context_instance=RequestContext(request))

def view_interviewed(request):
    return HttpResponseRedirect('')

def joinInterview(request):
    return HttpResponseRedirect('')