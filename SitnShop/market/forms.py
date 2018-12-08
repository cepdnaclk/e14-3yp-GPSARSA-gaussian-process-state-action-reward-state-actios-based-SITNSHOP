from .models import Customer, Shop, Advertisement, HashTag, ShopCategory, QuickAdd
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

class CreateAdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['Advertisement_text', 'Advertisement_data']


class CreateQuickAdvertisementForm(forms.ModelForm):

    class Meta:
        model = QuickAdd
        fields = ['QuickAdd_text', 'QuickAdd_data']



class UpdateAdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['Advertisement_text']

class UpdateQuickAdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement
        fields = ['Advertisement_text']



class ShopSignUpForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = ['ShopOwner', 'ShopName', 'shop_category', 'Address', 'NumOfAds', 'NumOfQuickAds', 'ProfilePic']




# class HashTagSet(forms.ModelForm):
#     # hst = forms.ModelMultipleChoiceField(queryset=HashTag.get(shop))
#     hash_tags = forms.ModelMultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         queryset=ShopCategory.objects.get(category_name='Salon').allowed_hash_tags.all()
#     )
#
#     class Meta:
#         model = Shop
#         fields = ['hash_tags']
#
#     # def __init__(self, *args, **kwargs):
#     #     shop_category = kwargs.pop('shop_category')
#     #     super(ShopSignUpForm, self).__init__(*args, **kwargs)
#     #     choices = forms.getChoices(shop_category)
#     #     self.fields['hash_tags'].queryset = choices


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

