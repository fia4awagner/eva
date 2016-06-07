from django.shortcuts import render
from models import User, DraftHeader, get_draft_model
import securety 
import context_builder
from django.template.context_processors import request

from django.http import HttpResponse

import csv

def get_survey_as_scv(reqest, survey_header_id):
    response = HttpResponse(content_type='text/csv')
    
    list = ['a', 'b']
    csv_table = [list] * 2
    
    csv_writer = csv.writer(response)
    for row in csv_table:
        csv_writer.writerow(row)
         
    return response

def login(request):
    name = request.POST.get('user', None)
    pwd = request.POST.get('pwd', None)
    if User.autenticate(name, pwd):
        request.session['user'] = name
        return menu(request)
    return get_login(request, 'fail')

def get_login(request, msg=None):
    context = {}
    if msg:
        context['login_label'] = msg
    return render(request, 'index.html', context)

@securety.is_user_login
def menu(request):
    return render(request, 'index.html', {'login_label' : request.session['user']})

#########################################################
## start
@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def start_header(request):
    pass

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def start_header_details(request, header_id):
    pass

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def start_header_update(request, header_id):
    draft_header = get_draft_model(header_id)
    draft_header.create_survey(request)
    return start_header(request)
## end start
#########################################################


@securety.is_user_login
def running_header(request):
    pass

@securety.is_user_login
def finished_header(request):
    pass

@securety.is_user_login
def finished_header_details(request, header_id):
    pass

#########################################################
## draft header
@securety.is_user_login
def draft_header(request):
    
    context = {
        DraftHeader.get_tabel_dict({'autor' : request.session['user']})
    }
    return render(request, '', context) 

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_header_details(request, header_id):
    header = get_draft_model(header_id)
    
    context = {
        
    }
    
    return render (request, 'draft_header_details.html', context)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_header_update(request, header_id):
    header = DrafHeader.getHeader(header_id)
    http_response = securety.does_user_owne_model(header, request.session['user'])
    if http_response:
        return http_response
    
    header.update_from_request(request)
    return draft_header_details(request, header_id)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_header_delete(request, header_id):
    header = get_draft_model(header_id)
    header.delete()
    return draft_header(request)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_header_add(request):
    new_header = DraftHeader.objects.create()
    return draft_header_details(request, new_header.id)
## end draft header
#########################################################


#########################################################
## draft group

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_group_delete(requset, header_id, group_id):
    header = get_darft_model(header_id)
    header.delete_group(group_id)
    return draft_header_details(request, header_id)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_group_add(requset, header_id):
    header = get_darft_model(header_id)
    header.add_group()
    return draft_header_details(request, header_id)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_group_update(requset, header_id, group_id):
    header = get_draft_model(header_id)
    header.update_from_request(requset)
    return draft_header_details(request, header_id)
## draft group
#########################################################

######################################################
## questions
@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_question_add(request, header_id, group_id):
    group = get_draft_model(header_id, group_id)
    group.add_qusetion()
    return draft_header_details(request, header_id)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_question_update(request, header_id, group_id, questeion_id):
    question = get_draft_model(header_id, group_id, questeion_id)
    question.update_from_request(request)
    return draft_header_details(request, header_id) 


@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_question_delete(request, header_id, group_id, question_id):
    group = get_draft_model(header_id, group_id)
    group.delete_question(question_id)
    return draft_header_details(request, header_id)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_question_delete(request, header_id, group_id, question_id):
    group = get_draft_model(header_id, group_id)
    group.delete_question(question_id)
    return draft_header_details(request, header_id)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_question_add_from_pool(request, header_id, group_id, 
            pool_header_id, pool_group_id, pool_question_id):
    
    pool_question = get_draft_model(pool_header_id, pool_group_id, pool_question_id)
    
    draft_group = get_draft_model(header_id, group_id)
    draft_group.add_question_from_pool(pool_question)
    return draft_header_details(request, header_id)
## questions
######################################################


#########################################################
## pool
@securety.is_user_login
def pool_header(request, header_id, group_id):
    pass

@securety.is_user_login
def pool_header_details(request, header_id, group_id, pool_header_id):
    pass
## end pool
#########################################################


def finished_question_details(request,header_id,group_id, question_id):
    pass


def enter_survey(request,header_id,token):
    pass


def hand_over_survey(request,header_id,token):
    pass





