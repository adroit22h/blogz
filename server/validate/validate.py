import re



def validateUsername(fieldname,request):
    if checkforEmpty(request[fieldname]):
        return False
    if checkforInvalidLength(request[fieldname]):
        return False
    if checkforWhiteSpaces(request[fieldname]):
        return False
    
    return 'validating username'

def validatePassword(fieldname,request):
    if checkforEmpty(request[fieldname]):
        return False
    if checkforInvalidLength(request[fieldname]):
        return False
    if checkforWhiteSpaces(request[fieldname]):
        return False
    
    return 'validating Password'

def verifyPassword(fieldname,request):
    if checkforEmpty(request[fieldname]):
        return False
    if request[fieldname]!=request['password']:
        return False

def validateEmail(fieldname,request):
   
    if checkforEmpty(request[fieldname]):
        print(2)
        return False
    

def validateTitle(fieldname,request):

   
    if checkforEmpty(request[fieldname]):
        print(2)
        return False



def validateBody(fieldname,request):
    if checkforEmpty(request[fieldname]):
        print(2)
        return False
    


def checkforEmpty(field):

    if field=='':
        return True
    else:
        return False

def checkforInvalidLength(field,validlength=3,maxlength=20):
    if len(field)<validlength or len(field)>maxlength:
        return True

def checkforWhiteSpaces(field):
    reg= re.compile('\s') 
    
    if  len(reg.findall(field))>0:
        return True
    else:
        return False    
    

def validationDictionary():
    return {
        'username': validateUsername,
        'password': validatePassword,
        'password_verify': verifyPassword,
        'email':  validateEmail,
        'title': validateTitle,
        'body':validateBody
        }

def validation(parameters):
    error={}
    for index, field in enumerate(parameters.form):
        
        if field in validationDictionary():
            if (validationDictionary()[field](field,parameters.form))==False:
                error[field]= False
        
       
    if len(error)>0:
        return error
    
    return True