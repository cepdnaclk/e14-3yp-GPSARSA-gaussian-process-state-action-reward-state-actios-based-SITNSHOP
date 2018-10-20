
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
import datetime
from django.contrib.auth import logout
from .models import Client, Viewer
import os

from el_pagination.decorators import page_template
from el_pagination.views import AjaxListView

@page_template('pages/index_page.html')



def HomePage(request, extra_context = None):
    template_name = "pages/index.html"
    page_template = "pages/index_page.html"

    if request.method == "GET":
        user = request.user
        c = Client.objects.filter(pk = 2)
        print(c[0].pk)
        entries = [c[0] for i in range(1000)]


        context = {"entries": entries, "page_template": page_template, "user" : user}
        if extra_context is not None:
            context.update(extra_context)


        return render(request, template_name, context)

    elif request.method == "POST":
        user = request.user
        s = request.POST["search"]

       
        u = User.objects.filter(username = s)




        if len(u) == 0:
            return redirect("/home/")
        else:
            c = Client.objects.filter(user = u[0])
            if len(c) == 0:
                return redirect("/home/")
            else:
                if user == c[0].user:
                    return redirect("/home/profile/")
                else:
                    url  = "/home/public/" + str(c[0].pk) + "/"
                    return redirect(url)



def SignUP(request):
    if request.method == "GET":

        template_name = "pages/signup_page.html"
        context = {}

        return render(request, template_name, context)

    elif request.method == "POST":


        username = request.POST["username"]
        password = request.POST["password"]
        r_password = request.POST["r_password"]

        if(password == r_password):
            user = User.objects.create_user(username=username, password= password)

            c = Client()
            c.user = user
            c.timestamp = datetime.datetime.now()
            path = os.getcwd()
            new_path = path + "\client\static\Images\i" + str(c.pk)
            if os.path.isdir(new_path):
                pass
            else:
                os.mkdir(new_path)

            c.save()



            return redirect("/home/login/")


        else:
            template_name = "pages/signup_page.html"
            context = {'error' : "Please type the correct authentication details"}

            return render(request, template_name, context)

def SignUP_User(request):

    if request.method == "GET":

        template_name = "pages/signup_page_user.html"
        context = {}

        return render(request, template_name, context)

    elif request.method == "POST":


        username = request.POST["username"]
        password = request.POST["password"]
        r_password = request.POST["r_password"]

        if(password == r_password):
            user = User.objects.create_user(username=username, password= password)

            v = Viewer()
            v.user = user
            v.timestamp = datetime.datetime.now()
            v.save()

            return redirect("/home/login/")

        else:

            template_name = "pages/signup_page_user.html"
            context = {'error' : "Please type the correct authentication details"}




def LoginIN(request):
    if request.method == "POST":

        user = request.user

        if user.is_anonymous:
            logout(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)



            return redirect("/home/profile/")

        else:

            template_name = "pages/login_page.html"
            context = {'error' : "Please type the correct authentication details"}

            return render(request, template_name, context)
    else:
        template_name = "pages/login_page.html"
        context = {}

        return render(request, template_name, context)

def Profile(request):



    user = request.user
    c = Client.objects.filter(user = user)
    if user.is_anonymous or len(c) == 0:

        return redirect("/home/")

    else:

        ad_list = [["1","a"],  ["2", "b"], ["3", "c"]]
        template_name = "pages/profile.html"
        pk = str(c[0].pk)
        context = {"user" : user, "ad_list": ad_list, "pk": pk}
        return render(request, template_name, context)


def public_profile(request, pk):

    u = Client.objects.filter(pk = pk)


    if len(u) == 0:
        return redirect("/home/")

    else:
        c = u[0]
        ad_list = [["1","a"],  ["2", "b"], ["3", "c"]]
        template_name = "pages/profile_public.html"
        pk = str(c.pk)
        context = {"user" : c, "ad_list": ad_list, "pk": pk}
        return render(request, template_name, context)



def LogOUT(request):

    user = request.user
    
    if user is not None:
        logout(request)

    return redirect("/home/login/")
