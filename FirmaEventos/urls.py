"""FirmaEventos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import (
    password_reset_confirm, password_reset_complete
    )

from users.forms import SetPasswordForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^sources/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'users_confirm_reset.html',
         'post_reset_redirect': '/user/password/done/',
         'set_password_form': SetPasswordForm},
        name='password_reset_confirm'),
    url(r'^password/done/$', password_reset_complete,
        {'template_name': 'users_pass_done.html'}),
    url(r'^', include('base.urls', namespace="base")),
    url(r'^', include('users.urls', namespace="users")),
    url(r'^', include('eventos.urls', namespace="events")),
]
