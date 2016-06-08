from django.shortcuts import render
from models import User, DraftHeader, get_draft_model, get_survey_model, SurveyMember

import securety 
import models

from django.http import HttpResponse

import csv

@securety.is_user_login
@securety.is_user_owner(get_survey_model)
def get_survey_as_scv(reqest, survey_header_id):
    response = HttpResponse(content_type='text/csv')

    header = get_survey_model(survey_header_id)
    
    csv_writer = csv.writer(response)
    for row in header.get_csv_table():
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
        context['msg'] = msg
    return render(request, 'index.html', context)

@securety.is_user_login
def menu(request):
    context = {
        'cnt_running' : models.ActiveDraftHeader.get_cnt_running(),
        'cnt_ready' : models.ActiveDraftHeader.get_cnt_ready(),
    }
    return render(request, 'menu.html', context)

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
    header = DraftHeader.getHeader(header_id)
    
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
def draft_group_delete(request, header_id, group_id):
    header = get_draft_model(header_id)
    header.delete_group(group_id)
    return draft_header_details(request, header_id)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_group_add(request, header_id):
    header = get_draft_model(header_id)
    header.add_group()
    return draft_header_details(request, header_id)

@securety.is_user_login
@securety.is_user_owner(get_draft_model)
def draft_group_update(request, header_id, group_id):
    header = get_draft_model(header_id)
    header.update_from_request(request)
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

@securety.is_token_validate
def enter_survey(request,header_id,token):
    
    header = get_survey_model(header_id)
    groups = []
    for group in header.getGroups():
        qus = []
        for qu  in group.getQuestions():
            qus.append({'id' : qu.questionID, 'text' : qu.questionText, 'type' : qu.answerType,}) 
        groups.append({'id' : group.groupID, 'name' : group.groupName, 'question' : qus})
    
    context = {
               'name_survey' : header.headerName,
               'group' : groups
    }
    return render(request, 'survey.html', context)


@securety.is_token_validate
def hand_over_survey(request,header_id,token):
    header = get_survey_model(header_id)
    header.create_answers(request)
    
    SurveyMember.objects.get(header=header_id, token=token).delete()
    return HttpResponse('abgegeben!')





