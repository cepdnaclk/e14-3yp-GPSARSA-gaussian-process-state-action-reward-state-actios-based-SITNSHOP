from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from ..forms import ShopSignUpForm, ShopLogInForm
from ..models import Shop, Advertisement, Follow

from ..forms import UserForm, AdvertisementForm, UpdateAdvertisementForm
import datetime

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

class ShopIndexView(generic.ListView):

    template_name = 'market/shop_profile.html'
    context_object_name = 'shop'
    def get_queryset(self):
        # print(self.kwargs['pk'])
        shop = Shop.objects.get(pk=self.kwargs['pk'])
        # print(Advertisement.objects.filter(shop=shop))
        # print("@ shopindexview")
        # print(shop.id)
        n_followers = Follow.objects.filter(follower=shop.user).count()
        print("num of followers  ",n_followers)
        data = {'adds': Advertisement.objects.filter(shop=shop),
                'shop': shop,
                'n_followers': n_followers}

        return data


class IndexView(generic.ListView):
    template_name = 'market/home.html'
    context_object_name = 'adds'
    def get_queryset(self):
        return Advertisement.objects.all()

class DetailView(generic.DetailView):
    model = Shop
    template_name = 'market/profile_public.html'

def loginShop(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and Shop.objects.filter(user=user).exists() is True:
            if user.is_active:
                login(request, user)
                print('came here')
                return render(request, 'market/shop_profile_editable.html')
                # shop = Shop.objects.get(user=request.user)
                # adds = Advertisement.objects.filter(shop=shop)
                # return render(request, 'market/shop_profile_editable.html', {'shop': shop, 'adds': adds})
            else:
                return render(request, 'market/shop_login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'market/shop_login.html', {'error_message': 'Invalid login'})
    print("hey not a post")
    return render(request, 'market/shop_login.html')


def checkFileType(file_type):
    if file_type not in IMAGE_FILE_TYPES:
        return False
    return True


def signupShop(request):
    form = ShopSignUpForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # print(username + " " + password + " " + user.username)

        if user is not None and form.is_valid() and Shop.objects.filter(user=user).exists() is False:
            if user.is_active:
                login(request, user)
                user.is_shop = True
                shop = form.save(commit=False)
                shop.user = request.user
                user.save()
                user.profile.is_shop = True
                user.save()
                # shop.Advertisement = request.FILES['Advertisement']
                shop.ProfilePic = request.FILES['ProfilePic']
                correct_type = True
                # correct_type = checkFileType(shop.Advertisement.url.split('.')[-1]) and correct_type
                correct_type = checkFileType(shop.ProfilePic.url.split('.')[-1]) and correct_type

                if correct_type is False:
                    context = {
                        'shop': shop,
                        'form': form,
                        'error_message': 'Image file must be PNG, JPG, or JPEG',
                    }

                    return render(request, 'market/shop_signup.html', context)

                shop.timestamp = datetime.datetime.now()
                # shop = Shop.objects.get(user=request.user)
                shop.save()
                edit_shop(request)
                # return render(request, 'market/edit_shop_profile.html', {'shop': shop})
            else:
                return render(request, 'market/shop_signup.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'market/shop_signup.html', {"form": form, 'error_message': 'Invalid login'})
    return render(request, 'market/shop_signup.html', {"form": form})



#
# def edit_shop(request):
#
#     shop = Shop.objects.get(user=request.user)
#     adds = Advertisement.objects.filter(shop=shop)
#
#     updateForm = UpdateAdvertisementForm(request.POST or None, request.FILES or None)
#     form = AdvertisementForm(request.POST or None, request.FILES or None)
#     # shop = get_object_or_404(Shop, pk=shop_id)
#     shop = Shop.objects.get(user=request.user)
#     if form.is_valid():
#         advertisement = form.save(commit=False)
#         advertisement.shop = shop
#         advertisement.Advertisement_data = request.FILES['Advertisement_data']
#         correct_type = True
#         correct_type = checkFileType(advertisement.Advertisement_data.url.split('.')[-1]) and correct_type
#         if correct_type is False:
#             context = {
#                 'advertisement': advertisement,
#                 'form': form,
#                 'updateForm': updateForm,
#                 'shop': shop,
#                 'adds': adds,
#                 'error_message': 'Image file must be PNG, JPG, or JPEG',
#             }
#             return render(request, 'market/shop_profile_editable.html', context)
#         advertisement.save()
#         # redirect('market:homepage')
#         # return render(request, 'market:homepage', {'shop': album})
#     numberOfAdds = Advertisement.objects.filter(shop=shop).count()
#     withinAddLimit = numberOfAdds < shop.NumOfAds
#     context = {
#         'form': form,
#         'updateForm': updateForm,
#         'shop': shop,
#         'adds': adds,
#         'withinAddLimit': withinAddLimit
#     }
#
#     return render(request, 'market/shop_profile_editable.html', context)


def edit_shop(request):

    shop = Shop.objects.get(user=request.user)
    adds = Advertisement.objects.filter(shop=shop)

    updateForm = UpdateAdvertisementForm(request.POST or None, request.FILES or None)
    createform = AdvertisementForm(request.POST or None, request.FILES or None)
    # shop = get_object_or_404(Shop, pk=shop_id)
    shop = Shop.objects.get(user=request.user)
    numberOfAdds = Advertisement.objects.filter(shop=shop).count()
    withinAddLimit = numberOfAdds < shop.NumOfAds
    context = {
        'form': createform,
        'updateForm': updateForm,
        'shop': shop,
        'adds': adds,
        'withinAddLimit': withinAddLimit
    }

    return render(request, 'market/shop_profile_editable.html', context)




class AdvertisementDelete(DeleteView):
    model = Advertisement
    success_url = reverse_lazy('market:edit_shop')


class AdvertisementUpdate(UpdateView):
    model = Advertisement
    fields = ['Advertisement_text']
    # form_class = AdvertisementForm
    success_url = reverse_lazy('market:edit_shop')


class AdvertisementCreate(CreateView):
    model = Advertisement
    # fields = ['Advertisement_text']
    form_class = AdvertisementForm

    def get_success_url(self):
        return 'market:edit_shop'

    def form_valid(self, form):
        advertisement = form.save(commit=False)
        shop = Shop.objects.get(user=self.request.user)
        print(self.get_context_data())
        advertisement.shop = Shop.objects.get(user=self.request.user)
        advertisement.Advertisement_data = self.request.FILES['Advertisement_data']
        correct_type = True
        correct_type = checkFileType(advertisement.Advertisement_data.url.split('.')[-1]) and correct_type
        if correct_type is False:
            return redirect(self.get_success_url())
        advertisement.save()
        return redirect(self.get_success_url())


