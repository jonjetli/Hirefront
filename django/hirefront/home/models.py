from django.db import models
from django.core.urlresolvers import resolve

# Create your models here.

class postulantes(models.Model):
    Fullname = models.CharField(max_length=150)
    #last_name = models.CharField(max_length=150)
    id = models.CharField(max_length=150)
    number = models.IntegerField(max_length=50)
    country = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    #direction = models.CharField(max_length=200)
    email = models.EmailField(max_length=150, unique=True, primary_key=True)
    password = models.CharField(max_length=150)
    status = models.SmallIntegerField(max_length=2, default=0)
    code_validation = models.CharField(max_length=150, default='Null')
    cv = models.FileField(upload_to='CVs')

    def __unicode__(self):
        return "%s %s" % (self.Fullname, self.email)


class reqlutadores(models.Model):
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    number = models.IntegerField()
    direction = models.CharField(max_length=200)
    email = models.EmailField(max_length=150, unique=True,primary_key=True)
    password = models.CharField(max_length=150)
    #image = models.ImageField(upload_to='LogosEnterprise')

    def __unicode__(self):
            return "%s %s" %(self.name, self.last_name)

class calendar_interviewed_enterprise(models.Model):
    email_interviewed = models.EmailField(max_length=150)
    code_unique_interview = models.CharField(max_length=200)
    email_enterprise = models.EmailField(max_length=150)
    date_interview = models.CharField(max_length=150)
    time_interview = models.CharField(max_length=150)
    observations = models.CharField(max_length=200)
    status =models.CharField(max_length=150, default='Off Air')
