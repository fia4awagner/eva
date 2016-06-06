"""eva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
import view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^login', view.login),
    url(r'^$', view.get_login),
    
    url(r'^confic/menu$', view.menu),
    
    url(r'^confic/design$', view.design_header),
    url(r'^confic/design/(\d+)$', view.design_header_details),
    url(r'^confic/design/(\d+)/(\d+)/pool$', view.pool_header),
    url(r'^confic/design/(\d+)/(\d+)/pool/(\d+)$', view.pool_header_details),
    
    url(r'^confic/start$', view.start_header),
    url(r'^confic/start/(\d+)$', view.start_header_details),
    
    url(r'^confic/running$', view.running_header),
    
    url(r'^confic/finished$', view.finished_header),
    url(r'^confic/finished/(\d+)$', view.finished_header_details),
    url(r'^confic/finished/(\d+)/(\d+)/(\d+)$' , view.finished_question_details),
    
    url(r'^survey/(\d+)/(\w+)$', view.enter_survey),
    url(r'^survey/(\d+)/(\w+)/hand_over$', view.hand_over_survey),
    
]
