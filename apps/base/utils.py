from datetime import datetime

#funcion para validar el campo imagen cuando del front viene vacio como un undefine
# el __delitem__ y el __setitem__ son funcionalidades del codigo fuente que permiten modificar el request, mutarlo
def validate_files(request, field, update=False):
    """ 
    :params
    :request: request.data
    :field: key of file    
    """
    
    request = request.copy() # este metodo copia el request para poder mutarlo

    if update:
        if type(request[field]) == str: request.__delitem__(field)
    else:
        if type(request[field]) == str: request.__setitem__(field, None)        

    return request

def format_date(date):
    date = datetime.strptime(date, '%d/%m/%Y')
    date = f"{date.year}-{date.month}-{date.day}"
    return date
