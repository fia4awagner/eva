from django.shortcuts import render
from models import User
import securety
import context_builder
from eva.models import DraftHeader

def login(request):
    if User.autenticate(request.GET['name'], request.GET['pwd']):
        return render(request, 'success.html', {'success' : True,})
    return render(request, 'success.html', {'fail' : True})


def get_login(request):
    return render(request, 'login.html', {})

@securety.is_user_login
def get_menu(request):
    user = request.sission['user']
    context = {
            'count_running' : ActiveHeader.get_running_cnt(user),
            'count_ready' : ActiveHeader.get_ready_cnt(user),
    }
    
    return render(request, 'index.html', context)

@securety.is_user_login
def get_draft_over_view(request):
    user = request.sission['user']
    context = {
               'back' : context_builder.get_back('conf/menu', 'Uebersicht der eigenen Vorlagen'),
               ## TODO 
               'table' : context_builder.build_table(DraftHeader, 
                        ['id', 'name', '...'], ['...'], {'owner' : user}, '...')
    }