from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template import loader
import datetime
import json
from .rigor import RigorForm

# Create your views here.
class_list = []
total_data = []
cookies_list = []

def index(request):
    page_title = "Grades Calculator!"
    return render(request, 'grades/index.html',
                  context={'page_title': page_title})

def cookies(request) :
   dico_cookies = request.COOKIES
   visit_nbr = 0
   if 'visit_nbr' in dico_cookies:
       try:
           visit_nbr = int(dico_cookies['visit_nbr']) + 1
       except:
           visit_nbr = 1
   else:
       visit_nbr = 1

   response = render(request, "grades/cookies.html",
                     context={'visit_nbr': visit_nbr})
   response.set_cookie(key="visit_nbr", value=visit_nbr, 
                       expires=datetime.datetime(2024, 10, 20, 20, 23), samesite="LAX")
   return response

def instructions(request):
    return render(request, 'grades/instructions.html')
       
def forms(request): 
   global total_data
   if request.method== "POST" and "submit_form" in request.POST:
      total=0
      if 'grade' not in request.POST or 'level' not in request.POST or 'class_name' not in request.POST:
         messages.add_message(request, messages.ERROR, "The form sent is incomplete")
         return render(request, "grades/forms.html")
      else: 
         add_dic = json.dumps({
            'grade': request.POST['grade'],
            'level': request.POST['level'],
            'class_name':request.POST['class_name']
            # 'form' : 'forms/',
            # 'index' : len(class_list)
            })
         res = json.loads(add_dic)
         class_list.append({"grade": request.POST['grade'], 
                            "level": request.POST['level'], 
                            "class_name": request.POST["class_name"] })
         cookies_list.append({"grade": request.POST['grade'], 
                            "level": request.POST['level'], 
                            "class_name": request.POST["class_name"]})
          
         # request.POST['grades_average'],
         #    'level': request.POST['grades_level'],
         #    'class':request.POST['grades_class'],
         #    })
         response = redirect('grades:new_score_report')
         response.set_cookie(key="grades_data", value=json.dumps(
            {'grade': request.POST['grade'],
            'level': request.POST['level'],
            'class_name':request.POST['class_name'],
            }), samesite = "LAX", expires=datetime.datetime(2024, 10, 20, 20, 23))
         scores=[]
         for e_class in class_list:
            if request.POST['level']=="Regular":
               scores.append(int(request.POST['grade']))
               total+=1
            if request.POST['level']=="Honors":
               scores.append(int(request.POST['grade'])*1.1)
               total+=1.1
            if request.POST['level']=="AP":
               scores.append(int(request.POST['grade'])*1.2)
               total+=1.2
         #GPA= (sum(scores))/total
         #response.set_cookie(key="gpa", value=GPA)
      return response
   return render(request, "grades/forms.html",) #{'class_list': class_list})


def new_forms(request):
   if request.method == "POST":
      form = RigorForm(request.POST)
      if form.is_valid():
         # process the data
         response = redirect('grades:new_score_report')
         add_dic = json.dumps({
            'grade': request.POST['grade'],
            'level': request.POST['level'],
            'class_name':request.POST['class_name']
            # 'form' : 'new_forms/',
            # 'index' : len(class_list)
            })
         res = json.loads(add_dic)
         class_list.append({"grade": request.POST['grade'], 
                            "level": request.POST['level'], 
                            "class_name": request.POST["class_name"]
                           })
         cookies_list.append({"grade": request.POST['grade'], 
                            "level": request.POST['level'], 
                            "class_name": request.POST["class_name"]})
         print(class_list)
         print(cookies_list)

         total=0
         scores_d=[]
         for e_class in class_list :
            if form.cleaned_data['level']=="Regular":
               scores_d.append(int(form.cleaned_data['grade']))
               total+=1
            if form.cleaned_data['level']=="Honors":
               scores_d.append(int(form.cleaned_data['grade']))*1.1
               total+=1.1   
            if form.cleaned_data['level']=="AP":
               scores_d.append(average1=int(form.cleaned_data['grade']))*1.2
               total+=1.2
            else:
               scores_d.append(int(form.cleaned_data['grade']))
               total+=1  
               
         #GPA_d=sum(scores_d)/total

         response.set_cookie(key="data", value=json.dumps(
               {'level': request.POST['level'],
               'grade': request.POST['grade'],
               'class_name' : request.POST['class_name'],
               }), samesite = "LAX", expires=datetime.datetime(2024, 10, 20, 20, 23))
         #response.set_cookie(key="gpa_d",value=GPA_d)
         return response
   else:
      form = RigorForm()
   return render(request, "grades/new_forms.html", {'RigorForm': form }, )#{'class_list': class_list} )

def new_score_report(request):
   # dico_cookies = request.COOKIES
   # dico_context = {}
   # if 'data' in dico_cookies:
   #    try:
   #       dico_grades_data = json.loads(dico_cookies['data'])
   #       dico_context['data'] = dico_grades_data
   #       # dico_gpa_data = json.loads(dico_cookies['gpa_d'])
   #       # dico_context['gpa_d'] = dico_gpa_data
   #    except:
   #       messages.add_message(request, messages.ERROR, "There is an error on your grades data")
   #    return render(request, "grades/new_score_report.html",context=dico_context)
   if request.method == "POST":
        class_name = request.POST.get('class_name')
        grade = request.POST.get('grade')
        level = request.POST.get('level')
        print({"class": class_name, "grade": grade, "level": level})
        cookies_list.remove({"grade": grade, "level": level, "class_name": class_name})
   return render(request, "grades/new_score_report.html", context={"cookies_list": cookies_list})

def load_class_list(request):
   return {'class_list': class_list}

def finder (request):
   if request.method == "POST":
        if 'classname' not in request.POST:
            messages.add_message(request, messages.ERROR, "The form sent is incomplete")
            return render(request, "grades/finder.html")
        response = render(request, "grades/finder_result.html", context={
                'class_last': class_list,
                'classname': request.POST['classname']
            })
        response.set_cookie(key="data", value=json.dumps(
            {'classname': request.POST['classname']}))
        return response
   return render(request, "grades/finder.html")


def edit(request):
   if request.method == "POST":
        class_list.insert({"class": request.COOKIES['class_name'], 
                           "grade": request.COOKIES['grade'], 
                           "level": request.COOKIES['level']})
        response = render(request, "grades/new_score_report.html", 
                          context={'class_list': class_list,})
        return response
   return render(request, "grades/edit.html")

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

