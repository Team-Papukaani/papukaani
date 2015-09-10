from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

def public(request):
    return render(request, 'public.html')

def upload(request):
    if request.method == 'POST':
        file =request.FILES['file'].read()
        return render(request, 'index.html', {"file" : file})
        ##parse
        


    return redirect(index)