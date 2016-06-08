from django.shortcuts import HttpResponse

from eva.models import SurveyMember
import view     # only import get_login

def is_token_validate(func):
    def nested_func(*args):
        header_id, token = args[1:3] 
        
        if SurveyMember.check_if_exists(token, header_id):
            return func(*args) 
        
        return HttpResponse('keine abgabe moeglich')
    
    return nested_func

def is_user_login(func):
    '''
    func (request, *)
    check if Usre is logt in 
    '''
    def nested_func(*args):
        user_from_request = args[0].session.get('user', None)
        if not user_from_request:
            return view.get_login(args[0], 'Melden Sie sich an um diese Funktion zu nutzen.')
        
        return func(*args)
    
    return nested_func

def is_user_owner(get_model):
    '''
    checkes if header_instance.owner == request.session['user']
    args:
    func(request, header_id, *)
    get_model(header_id) will be called to get header_instance 
    '''
    def decorator(func):
        def nested_func(*args):
            request, header_id = args[2:]
            header = get_model(header_id)
            if header.owner == request.session['user']:
                return func(*args)
            else:
                return HttpResponse('stop')
            
    return decorator

        
        