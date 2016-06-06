

def get_back(href, title):
    return {
            'href' : href,
            'title' : title,
    }
    
def build_table(model, fields, fields_for_filter, filter, href_header):
    '''
    ***
    '''
    filter_for_context = [field for name, field in model.to_fields().items() if name in fields]
    for field in filter:
        if field['name'] in fields_for_filter:
            field['is_filter'] = True
    
    rows = [value for name, value in model.objects.get(**filter) if name in fields]
     
    return {
        'header' : {'href' : href_header, 'fields' : filter_for_context},
        'rows' : rows,
        
    }


