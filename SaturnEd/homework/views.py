from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import datetime
import json
from django.template import loader

# Create your views here.

homework_list = []   
cookies_list = []

# index home page
def index(request):
    page_title = "Home Page"
    return render(request, 'homework/index.html',
                  context={'page_title': page_title})

# homework list 
def hw_list(request):
    page_title = "Homework List"
    return render(request, 'homework/hw_list.html',
                  context={'page_title': page_title,
                           'homework_list': homework_list})

# cookies page
def cookies(request):
    dico_cookies = request.COOKIES
    visit_nbr = 0
    if 'visit_nbr' in dico_cookies:
        try:
            visit_nbr = int(dico_cookies['visit_nbr']) + 1
        except:
            visit_nbr = 1
    else:
        visit_nbr = 1
    response = render(request, "homework/cookies.html",
                    context={'visit_nbr': visit_nbr})
    response.set_cookie(key="visit_nbr", value=visit_nbr,
                        max_age=datetime.timedelta(seconds=1800),
                        samesite="LAX")
    return response

# html form
def forms(request):
    if request.method == "POST":
        if 'hw_class' not in request.POST or 'hw_date' not in request.POST or 'hw_name' not in request.POST:
            messages.add_message(request, messages.ERROR, "Form Incomplete")
        else: 
            response = render(request, "homework/add_success.html", context={
                'homework_list': homework_list
            })
            response.set_cookie(samesite="LAX", max_age=datetime.timedelta(seconds=1800), key='hw_data', value=json.dumps(
                {'hw_class': request.POST['hw_class'],
                 'hw_name': request.POST['hw_name'],
                 'hw_date': request.POST['hw_date']}
            ))
            homework_list.append({"class": request.POST['hw_class'], "name": request.POST['hw_name'], "date": request.POST["hw_date"]})
            cookies_list.append({"class": request.POST['hw_class'], "name": request.POST['hw_name'], "date": request.POST["hw_date"]})
        return response
    return render(request, "homework/forms.html")

# django forms
from .django_forms import DjangoForm

def django_forms(request):
    if request.method == "POST":
        form = DjangoForm(request.POST)
        if form.is_valid():
            # response = redirect('homework:add_success')
            response = render(request, "homework/add_success.html", context={
                'homework_list': homework_list
            })
            response.set_cookie(samesite="LAX", key="hw_data", value=json.dumps(
            {'hw_class': request.POST['hw_class'],
            'hw_name': request.POST['hw_name'],
            'hw_date': request.POST['hw_date']}))
            homework_list.append({"class": request.POST['hw_class'], "name": request.POST['hw_name'], "date": request.POST["hw_date"]})
            cookies_list.append({"class": request.POST['hw_class'], "name": request.POST['hw_name'], "date": request.POST["hw_date"]})
        return response
    else:
        form = DjangoForm()
    return render(request, "homework/django_forms.html", {'django_form': form})

# import pdb; pdb.set_trace() 

def search_form(request):
    if request.method == "POST":
        if 'hw_class' not in request.POST:
            messages.add_message(request, messages.ERROR, "The form sent is incomplete")
            return render(request, "homework/search_forms.html")
        response = render(request, "homework/class_hw.html", context={
                'homework_list': homework_list,
                'hw_class': request.POST['hw_class']
            })
        response.set_cookie(key="hw_data", value=json.dumps(
            {'hw_class': request.POST['hw_class']}))
        return response
    return render(request, "homework/search_form.html")

# list view
def list_view(request):
    if request.method == "POST":
        # edit button
        if 'edit_hw' in request.POST:
            index = cookies_list.index({"class": request.POST.get('class'), "name": request.POST.get('name'), "date": request.POST.get('date')})
            return render(request, "homework/edit_hw.html", context={'index': index})
        # remove button
        if 'remove_hw' in request.POST:
            cookie_class = request.POST.get('class')
            cookie_name = request.POST.get('name')
            cookie_date = request.POST.get('date')
            cookies_list.remove({"class": cookie_class, "name": cookie_name, "date": cookie_date})
            homework_list.remove({"class": cookie_class, "name": cookie_name, "date": cookie_date})
    return render(request, "homework/list_view.html", context={
                  "cookies_list": cookies_list})
    
def edit_hw(request):
    if request.method == "POST":
        if 'update_hw' in request.POST:
            cookies_list.pop(request.POST.get('index'))
            cookies_list.insert(request.POST.get('index'), {"class": request.POST.get('class'), "name": request.POST.get('name'), "date": request.POST.get('date')})
        return render(request, "homework/list_view.html", context={
                    "cookies_list": cookies_list})
      
# import pdb; pdb.set_trace()

# import pdb; pdb.set_trace()

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
