from django.shortcuts import redirect

def redirect_with_param(to, param):
    response = redirect(to)
    response['Location'] += param
    return response
