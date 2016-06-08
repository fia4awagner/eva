from django.shortcuts import HttpResponse

import view     # only import get_login

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

        
        