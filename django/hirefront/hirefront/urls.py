from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hirefront.views.home', name='home'),
    # url(r'^hirefront/', include('hirefront.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'home.views.index'),
    url(r'^Perfil/calendario$', 'home.views.Perfil_calendario'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^interviewed/new$','home.views.new_interviewed'),
    url(r'^signup','home.views.signup_interviewed'),
    url(r'^joinInterview/email_enterprise','home.views.detalle'),
    url(r'^joinInterview/email_interviewed/codigo_unico', 'home.views.joinInterview'),
    #(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/
)
