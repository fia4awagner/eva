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
    
    url(r'^$', view.get_login),
    url(r'^login$', view.login),
    
    url(r'^config/menu$', view.menu),

    #####################################
    ## draft
    
    # header
        url(r'^config/draft$', view.draft_header), # name.html
        url(r'^config/draft/add$', view.draft_header_add),
        url(r'^config/draft/(\d+)$', view.draft_header_details),
        url(r'^config/draft/(\d+)/update$', view.draft_header_update),
        url(r'^config/draft/(\d+)/delete$', view.draft_header_delete),
    # group
        url(r'^config/draft/(\d+)/add$', view.draft_group_add),
        url(r'^config/draft/(\d+)/(\d+)/update$', view.draft_group_update),
        url(r'^config/draft/(\d+)/(\d+)/delete$', view.draft_group_delete),
    # question 
        url(r'^config/draft/(\d+)/(\d+)/add$', view.draft_question_add),
        url(r'^config/draft/(\d+)/(\d+)/(\d+)/update$', view.draft_question_update),
        url(r'^config/draft/(\d+)/(\d+)/(\d+)/delete$', view.draft_question_delete),
        
        url(r'^config/draft/(\d+)/(\d+)/pool$', view.pool_header),
        url(r'^config/draft/(\d+)/(\d+)/pool/(\d+)$', view.pool_header_details),
        url(r'^config/draft/(\d+)/(\d+)/pool/(\d+)/(\d+)/(\d+)add$', view.draft_question_add_from_pool),
    ## end edit
    #####################################
    
    url(r'^config/start$', view.start_header),
    url(r'^config/start/(\d+)$', view.start_header_details),
    url(r'^config/start/(\d+)/update$', view.start_header_update),
    
    url(r'^config/running$', view.running_header),
    
    url(r'^config/finished$', view.finished_header),
    url(r'^config/finished/(\d+)/csv$', view.get_survey_as_scv),
    url(r'^config/finished/(\d+)$', view.finished_header_details),
    url(r'^config/finished/(\d+)/(\d+)/(\d+)$' , view.finished_question_details),
    
    url(r'^survey/(\d+)/(\w+)$', view.enter_survey),
    url(r'^survey/(\d+)/(\w+)/hand_over$', view.hand_over_survey),
    
]
