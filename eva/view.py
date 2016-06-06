from django.shortcuts import render
from models import User
import securety
import context_builder


def login(request):
    if User.autenticate(request.GET['name'], request.GET['pwd']):
        return render(request, 'success.html', {'success' : True,})
    return get_login(request, 'fail')


def get_login(request, msg=None):
    context = {}
    if msg:
        context['login_label'] = msg
    return render(request, 'login.html', context)

def get_design(request):
    pass


def get_design_detail(request, header_id):
    pass


def show_pool_header(request, header_id, group_id):
    pass


def show_pool_header_details(request, header_id, group_id, pool_header_id):
    pass


def start_header(request):
    pass


def start_header_details(request, header_id):
    pass


def running_header(request):
    pass


def finished_header(request):
    pass


def finished_header_details(request, header_id):
    pass


def design_header(request):
    pass


def design_header_details(request, header_id):
    pass


def pool_header(request, header_id, group_id):
    pass


def pool_header_details(request, header_id, group_id, pool_header_id):
    pass


def menu(request):
    pass

def finished_question_details(request,header_id,group_id, question_id):
    pass


def enter_survey(request,header_id,token):
    pass


def hand_over_survey(request,header_id,token):
    pass


