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
from django.core.mail import EmailMultiAlternatives
from django.core.context_processors import request
from django.middleware.csrf import get_token
import MySQLdb
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
                    return HttpResponseRedirect(username + "/Perfil_Interviewed")
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
                         return HttpResponseRedirect(username + '/Perfil_Enterprise')
                     else:
                         result = 'Password Incorrect'
                 except reqlutadores.DoesNotExist:
                     result = 'Not exist Enterprise'
    return render_to_response("index.html",{"result":result},context_instance = RequestContext(request))

def Perfil_calendario(request, email):
    estado = ''
    token = ''
    user = ''
    if request.method == 'POST':
        connection  =  mail.get_connection()
        token = get_token(request)
        email_interviewed = request.POST['email']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        obs = request.POST['obs']
        objeto = calendar_interviewed_enterprise()
        objeto.email_enterprise = email
        objeto.email_interviewed = email_interviewed
        objeto.date_interview = fecha
        objeto.time_interview = hora
        objeto.observations = obs
        confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(32))
        objeto.code_unique_interview = confirmation_code
        objeto.save()
        Subjetc = 'Date of Interviewed with' + email
        html_content = '<p> The Date for your Interview is: <br> DATE: '+ fecha + '<br> TIME: '+ hora + '<br><br>\
        This day you have go to this link: <a href="http://www.hirefront.com/joinInterview/'+ confirmation_code +'">'\
        + 'http://www.hirefront.com/joinInterview/'+ confirmation_code + '</a> <br><br> Regards'+ '<p>'
        msg = EmailMultiAlternatives(Subjetc,'',email, [email_interviewed])
        msg.attach_alternative(html_content,"text/html")
        msg.send()

    try:
        Data = reqlutadores.objects.get(pk=email)
        Entrevistas = calendar_interviewed_enterprise.objects.filter(email_enterprise = email)
        estado = 'Entrevistas designadas'
        user= 'Enterprise'
        return render_to_response("Perfil_Calendario.html",{"token":token,"user":user,"Entrevistas":Entrevistas,"Enterprise":Data,"estado":estado}, context_instance = RequestContext(request))
    except calendar_interviewed_enterprise.DoesNotExist:
        estado = 'You Dont have Interviewss'
    except reqlutadores.DoesNotExist:
        try:
            Data = postulantes.objects.get(pk=email)
            Entrevistas = calendar_interviewed_enterprise.objects.filter(email_interviewed = email)
            estado = ' Entrevistas designadas'
            user = 'Interviewed'
            return render_to_response("Perfil_Calendario.html",{"token":token,"user":user,"Entrevistas":Entrevistas,"Interviewed":Data,"estado":estado}, context_instance = RequestContext(request))
        except calendar_interviewed_enterprise.DoesNotExist:
            estado = 'You Dont have Interviews'
        #return render_to_response("viewEnterprise.html")
    return render_to_response("Perfil_Calendario.html",{"estado":estado,"user":user,"Entrevistas":Entrevistas,"Enterprise":Data} ,context_instance = RequestContext(request))
#    try:
#        Data = reqlutadores.objects.get(pk=email)
#        typeUser = 'Enterprise'
#        try:
#            Entrevistas = calendar_interviewed_enterprise.objects.get(email_enterprise = email)
#        except (calendar_interviewed_enterprise.DoesNotExist, MultiValueDictKeyError):
#            estado = 'You Dont Have Interviews'
#        return render_to_response("viewEnterprise.html",{'Data':Data,"typeUser": typeUser, "estado":estado}, context_instance = RequestContext(request))
#    except reqlutadores.DoesNotExist:
#        Data = postulantes.objects.get(pk=email)
#        typeUser = 'Interviewed'
#        return render_to_response("viewInterviewed.html",{'Data': Data,"typeUser": typeUser}, context_instance = RequestContext(request))


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
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if( fullname == '' or email == '' or  id == '' or cellphone == '' or pass1=='' or pass2==''):
            result = 'Please complete all field'
        else:
            if pass1 == pass2:
                cv = request.FILES['cv']
                objeto = postulantes(request.POST, request.FILES)
                objeto.Fullname = fullname
                objeto.id = id
                objeto.email = email
                objeto.number = cellphone
                objeto.cv = cv
                confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(32))
                objeto.code_validation = confirmation_code
                objeto.password = pass1
                objeto.save()
                email_confirmation = mail.EmailMessage('Welcome', ' Welcome http://127.0.0.1:8000/'+ email +'/'+ confirmation_code , 'jonathan@hirefront.com',[email],connection=connection)
                email_confirmation.send()
                return HttpResponseRedirect("/")
            else:
                result = 'Please verify the same password in the two inputs'
    return render_to_response("signup_interviewed.html",{'result':result},context_instance=RequestContext(request))

def viewEnterprise(request, email):
    enterprise = reqlutadores.objects.get(pk=email)
    return render_to_response("viewEnterprise.html",{"enterprise":enterprise},context_instance=RequestContext(request))


def view_interviewed(request, email):
    postulante = postulantes.objects.get(pk=email)
    return render_to_response("viewInterviewed.html",{"postulante":postulante},context_instance=RequestContext(request))


def joinInterview(request):
    return HttpResponseRedirect('')

def interviewed_validation(request, email, code_validation):
    postulante = postulantes.objects.get(pk=email)
    result = ''
    if postulante.code_validation == code_validation and postulante.status==0:
        result = 'Activation Satisfactory, Please come back to login'
        postulant = postulantes(email=email)
        postulant.code_validation = postulante.code_validation
        postulant.Fullname = postulante.Fullname
        postulant.id = postulante.id
        postulant.number = postulante.number
        postulant.city = postulant.city
        postulant.country = postulante.country
        postulant.cv = postulante.cv
        postulant.password = postulante.password
        postulant.status = 1;
        postulant.save()
        #return render_to_response("viewValidationUser.html",{"result":result},context_instance = RequestContext(request))
    else:
        if postulante.status == 1:
            result = 'The activation was performed before. This code is disable.'
            #return render_to_response("viewValidationUser.html",{"result":result},context_instance = RequestContext(request))
        else:
            if postulante.code_validation != code_validation:
                result = 'Verify your code Activation in your email'
    return render_to_response("viewValidationUser.html",{"result":result},context_instance = RequestContext(request))