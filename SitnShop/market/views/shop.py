from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from ..forms import ShopSignUpForm, ShopLogInForm
from ..models import Shop, Advertisement, Follow, QuickAdd, ShopCategory, HashTag

from ..forms import UserForm, CreateAdvertisementForm, UpdateAdvertisementForm, CreateQuickAdvertisementForm, UpdateQuickAdvertisementForm
import datetime



import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

def collect_stories():
    shops = Shop.objects.all()
    stories = []
    for shop in shops:
        if QuickAdd.objects.filter(shop=shop).exists() is True:
            q_adds = QuickAdd.objects.filter(shop=shop)
            items = []
            for add in q_adds:
                item = {
                    'id': add.pk,
                    'type': 'photo',
                    'length': '3',
                    'src': add.QuickAdd_data.url,
                    'preview': add.QuickAdd_data.url,
                    'link': '',
                    'linkText': add.QuickAdd_text,
                    'seen': 'false',
                    'time': ''
                }
                items.append(item)
            story = {
                'id': shop.pk,
                'photo': shop.ProfilePic.url,
                'name': shop.ShopName,
                'link': '',
                'lastUpdated': '',
                'items': items
            }
            stories.append(story)
    return stories

def getQuickAdds(request):
    stories = collect_stories()
    print(stories)
    url_test = Advertisement.objects.get(pk=2).Advertisement_data.url
    # stories = [
    #     {
    #         "id": "ramon",
    #         'photo': "https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/users/1.jpg",
    #         'name': "Ramon",
    #         'link': "https://ramon.codes",
    #         'lastUpdated': '',
    #         'items': [{
    #             'id': 'ramon-1',
    #             'type': 'photo',
    #             'length': '3',
    #             'src': url_test,
    #             'preview': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/1.jpg',
    #             'link': '',
    #             'linkText': 'false',
    #             'seen': 'false',
    #             'time': ''
    #         }]},
    #     {
    #         'id': "gorillaz",
    #         'photo': "https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/users/2.jpg",
    #         'name': "Gorillaz",
    #         'link': "",
    #         'lastUpdated': '',
    #         'items': [{
    #             'id': 'gorillaz-1',
    #             'type': 'video',
    #             'length': '0',
    #             'src': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/4.mp4',
    #             'preview': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/4.jpg',
    #             'link': '',
    #             'linkText': 'false',
    #             'seen': 'false',
    #             'time': ''
    #
    #         },
    #             {
    #                 'id': 'gorillaz-2',
    #                 'type': 'photo',
    #                 'length': '3',
    #                 'src': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/5.jpg',
    #                 'preview': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/5.jpg',
    #                 'link': '',
    #                 'linkText': 'false',
    #                 'seen': 'false',
    #                 'time': '52'
    #             }
    #         ]
    #     },
    #     {
    #         'id': "ladygaga",
    #         'photo': "https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/users/3.jpg",
    #         'name': "Lady Gaga",
    #         'link': "",
    #         'lastUpdated': 52,
    #         'items': [{
    #             'id': 'ladygaga-1',
    #             'type': 'photo',
    #             'length': '5',
    #             'src': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/6.jpg',
    #             'preview': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/6.jpg',
    #             'link': '',
    #             'linkText': 'false',
    #             'seen': 'false',
    #             'time': '52'
    #         },
    #             {
    #                 'id': 'ladygaga-2',
    #                 'type': 'photo',
    #                 'length': '3',
    #                 'src': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/7.jpg',
    #                 'preview': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/7.jpg',
    #                 'link': 'http://ladygaga.com',
    #                 'linkText': 'false',
    #                 'seen': 'false',
    #                 'time': '52'
    #             }
    #         ]
    #     },
    #     {
    #         'id': "starboy",
    #         'photo': "https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/users/4.jpg",
    #         'name': "The Weeknd",
    #         'link': "",
    #         'lastUpdated': 52,
    #         'items': [
    #             {
    #                 'id': 'starboy-1',
    #                 'type': 'photo',
    #                 'length': '5',
    #                 'src': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/8.jpg',
    #                 'preview': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/8.jpg',
    #                 'link': '',
    #                 'linkText': 'false',
    #                 'seen': 'false',
    #                 'time': '52'
    #             }
    #         ]
    #     },
    #
    #     {
    #         'id': "riversquomo",
    #         'photo': "https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/users/5.jpg",
    #         'name': "Rivers Cuomo",
    #         'link': "",
    #         'lastUpdated': 27,
    #         'items': [
    #             {
    #                 'id': 'riverscuomo',
    #                 'type': 'photo',
    #                 'length': '10',
    #                 'src': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/9.jpg',
    #                 'preview': 'https://raw.githubusercontent.com/ramon82/assets/master/zuck.js/stories/9.jpg',
    #                 'link': '',
    #                 'linkText': 'false',
    #                 'seen': 'false',
    #                 'time': '52'
    #             }
    #         ]
    #     }
    # ]

    return JsonResponse({
        'quick_adds': stories})


class IndexView(generic.ListView):
    template_name = 'market/home.html'
    paginate_by = 2
    context_object_name = 'adds'
    model = Advertisement
    # def get_queryset(self):
    #
    #     data = {'adds': Advertisement.objects.all()}
    #     print(Advertisement.objects.all())
    #     return data

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
                # hash_tags = form.cleaned_data.get('hash_tags')
                # print(hash_tags)
                # shop.hash_tags.set(hash_tags)
                # shop.save()
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
    quick_adds = QuickAdd.objects.filter(shop=shop)
    updateform = UpdateAdvertisementForm(request.POST or None, request.FILES or None)
    createform = CreateAdvertisementForm(request.POST or None, request.FILES or None)

    quickupdateform = UpdateQuickAdvertisementForm(request.POST or None, request.FILES or None)
    quickcreateform = CreateQuickAdvertisementForm(request.POST or None, request.FILES or None)

    # shop = get_object_or_404(Shop, pk=shop_id)
    shop = Shop.objects.get(user=request.user)
    numberOfAdds = Advertisement.objects.filter(shop=shop).count()
    withinAddLimit = numberOfAdds < shop.NumOfAds

    numberOfQuickAdds = QuickAdd.objects.filter(shop=shop).count()
    withinQuickAddLimit = numberOfQuickAdds < shop.NumOfQuickAds

    context = {
        'createform': createform,
        'updateform': updateform,
        'quickcreateform': quickcreateform,
        'quickupdateform': quickupdateform,
        'shop': shop,
        'adds': adds,
        'quick_adds': quick_adds,
        'withinAddLimit': withinAddLimit,
        'withinQuickAddLimit': withinQuickAddLimit
    }

    return render(request, 'market/shop_profile_editable.html', context)




class AdvertisementDelete(DeleteView):
    model = Advertisement
    success_url = reverse_lazy('market:edit_shop')


class QuickAdvertisementDelete(DeleteView):
    model = QuickAdd
    success_url = reverse_lazy('market:edit_shop')


class AdvertisementUpdate(UpdateView):
    model = Advertisement
    fields = ['Advertisement_text']
    # form_class = AdvertisementForm
    success_url = reverse_lazy('market:edit_shop')


class AdvertisementCreate(CreateView):
    model = Advertisement
    # fields = ['Advertisement_text']
    form_class = CreateAdvertisementForm

    def get_success_url(self):
        return 'market:edit_shop'

    def form_valid(self, form):
        advertisement = form.save(commit=False)
        shop = Shop.objects.get(user=self.request.user)
        print(self.get_context_data())
        advertisement.shop = Shop.objects.get(user=self.request.user)
        advertisement.Advertisement_data = self.request.FILES['Advertisement_data']
        # correct_type = True
        # correct_type = checkFileType(advertisement.Advertisement_data.url.split('.')[-1]) and correct_type
        # if correct_type is False:
        #     return redirect(self.get_success_url())
        advertisement.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print("form is invalid")
        return redirect(self.get_success_url())


class QuickAdvertisementCreate(CreateView):
    model = QuickAdd
    # fields = ['Advertisement_text']
    form_class = CreateQuickAdvertisementForm

    def get_success_url(self):
        return 'market:edit_shop'

    def form_valid(self, form):
        quick_advertisement = form.save(commit=False)
        shop = Shop.objects.get(user=self.request.user)
        print(self.get_context_data())
        quick_advertisement.shop = Shop.objects.get(user=self.request.user)
        quick_advertisement.QuickAdd_data = self.request.FILES['QuickAdd_data']
        # correct_type = True
        # correct_type = checkFileType(advertisement.Advertisement_data.url.split('.')[-1]) and correct_type
        # if correct_type is False:
        #     return redirect(self.get_success_url())
        quick_advertisement.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print("form is invalid")
        return redirect(self.get_success_url())




def get_hash_tags(request):
    print("loading hash tags..")
    shop_id = request.POST.get('id', None)
    category_name = Shop.objects.get(pk=shop_id).shop_category
    shop_hash_tags = Shop.objects.get(pk=shop_id).hash_tags.all().values('pk', 'tag_name')
    shop_hash_tags_ = Shop.objects.get(pk=shop_id).hash_tags.all().values('pk')

    pending_tags = ShopCategory.objects.get(category_name=category_name).allowed_hash_tags.exclude(id__in=shop_hash_tags_).values('pk', 'tag_name')
    pending_tags = list(pending_tags)
    shop_hash_tags = list(shop_hash_tags)

    return JsonResponse({
        'pending_tags': pending_tags,
        'shop_hash_tags': shop_hash_tags
    })

def set_hash_tags(request):
    print("setting hash tags..")
    shop_id = request.POST.get('id', None)
    print(request.POST)
    tags = request.POST.get('tags', None)
    tags = json.loads(tags)

    shop = Shop.objects.get(pk=shop_id)
    Shop.hash_tags.through.objects.filter(pk=shop_id).delete()
    hash_tags = []
    for t in tags:
        tag = tags[t]
        hash_tag = HashTag.objects.get(pk=tag)
        print(hash_tag)
        hash_tags.append(hash_tag)
    shop.hash_tags.set(hash_tags)
    return JsonResponse({
        'message': 'success',
    })






