from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
import datetime
from django.contrib.auth.models import User

# from ..decorators import student_required
# from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm
from ..models import Customer
from ..forms import UserForm


class CustomerSignUpView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'market/customer_signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            print(user.profile.is_shop)
            user.profile.is_customer = True
            user.save()
            customer = Customer.objects.create(user=user, timestamp=datetime.datetime.now())
            user = authenticate(username=username, password=password)
            # print(user.profile.is_shop)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('market:profile')
            print("um here")

        return render(request, self.template_name, {'form': form, 'error_message': 'something went wrong'})

def loginCustomer(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and Customer.objects.filter(user=user).exists() is True:
            if user.is_active:
                login(request, user)
                customer = Customer.objects.get(user=request.user)
                # print(customer.user)
                return redirect('market:homepage')
                # return render(request, 'market:homepage', {'customer': customer})
            else:
                return render(request, 'market/customer_login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'market/customer_login.html', {'error_message': 'Invalid login'})
    return render(request, 'market/customer_login.html')




def edit_customer(request):
    return redirect('market:homepage')