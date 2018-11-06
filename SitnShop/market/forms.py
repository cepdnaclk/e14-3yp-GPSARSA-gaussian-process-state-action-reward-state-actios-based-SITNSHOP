from .models import Customer, Shop, Advertisement
from django import forms
from django.db import transaction
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ShopLogInForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']

class AdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['Advertisement_text', 'Advertisement_data']

class UpdateAdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['Advertisement_text']


class ShopSignUpForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = ['ShopOwner', 'ShopName', 'Address', 'NumOfAds', 'ProfilePic']



class CustomerSignUp(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        customer = Customer.objects.create(user=user)
        return user