from django.shortcuts import HttpResponse

def is_user_login(func, user=None):
    '''
    check if Usre is logt in 
        func (request, ...)
    '''
    
    def nested_func(*args):
        user_from_request = args[0].sessoin.get('user', None)
        if not user:
            if not user_from_request:
                 return HttpResponse('Sie müssen angemeldte sein.')
        else:
            if user_from_request != user:
                return HttpResponse('nicht berechtig!')
        return func(*args)
    
    return nested_func

def does_user_owne_model(func,model_cls):
    '''
    can be used to check if model is owned by session['user']
        func(request, model_id, ...)
    '''
    def nested_func(*args):
        request, model_id = args[2:]
        model_instance = model_cls.objects.get(id=model_id)
        if model_instance.owner == request.session['user']:
            return func(*args)
        else:
            return HttpResponse('Sie sind nicht Berechtig!')
        
    return nested_func
        
        