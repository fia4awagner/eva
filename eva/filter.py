EMPTY_FILTER = ['<...>', None,] # has to be filled

def from_request_to_filter(request_query):
    return {
        field_name : value 
            for field_name, value in request_query.items() 
        if EMPTY_FILTER.has_key(value)
    }
