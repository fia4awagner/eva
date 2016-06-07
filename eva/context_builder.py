

def get_back(href, title):
    return {
            'href' : href,
            'title' : title,
    }
    

def to_header_fields(model, included_fields, filter_fields):
    '''
    
    '''
    fields = model.to_fields(included_fields)
    
    for filter_elm in fields:
        if filter_elm['name'] in filter_fields:
            filter_elm['is_filter'] = True
        
    return fields


def to_table_rows(query, included_fields):
    rows = []
    for qu_elm in query.items():
        cells = []
        for fld_name in included_fields:
            cells.append(qu_elm[fld_name])
        rows.append(cells)
        
    return rows


