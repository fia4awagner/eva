from django.shortcuts import HttpResponse

def is_user_login(func, user=None):
    '''
    func (request, *)
    check if Usre is logt in 
    '''
    
    def nested_func(*args):
        user_from_request = args[0].session.get('user', None)
        if not user:
            if not user_from_request:
                return HttpResponse('Sie muessen angemeldte sein.')
        else:
            if user_from_request != user:
                return HttpResponse('nicht berechtig!')
        return func(*args)
    
    return nested_func

def is_user_owner(get_model):
    '''
    func(request, header_id, *)
    get_model(header_id) will be called to get header_instance 
    check is passed if header_instance.owner == request.session['user']
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

def does_user_owne_model(model, user):
    '-> HttpResponse'
    if model.autor == user:
        return None
    else:
        return HttpResponse('Sie sind nicht Berechtig!')
        
        
        