
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from ..models import Shop, Customer, User,Follow
from django.http import JsonResponse

from el_pagination.decorators import page_template
from el_pagination.views import AjaxListView


def checkFollowStatus(request):


    shop_id = request.POST.get('id', None)
    print("shop id", shop_id)
    if request.user.is_anonymous:
        return JsonResponse({
            'action': 'follow',
            'message': 'log in to follow'}
        )

    try:
        user = User.objects.get(id=shop_id)
        print(" request id ", request.user.id)
        if Follow.objects.filter(following=request.user, follower=user).exists():
            return JsonResponse({
                'action': 'unfollow',
                'message': 'unfollow on'}
            )
        else:
            return JsonResponse({
                'action': 'follow',
                'message': 'follow on'}
            )

    except User.DoesNotExist:
        return JsonResponse({
            'action': 'follow',
            'message': 'unidentified user'}
        )

def shop_follow(request):
    user_id = request.POST.get('id', None)
    action = request.POST.get('action', '')

    FOLLOW_ACTION = 'follow'
    UNFOLLOW_ACTION = 'unfollow'

    if request.user.is_anonymous:
        return JsonResponse({
            'status':'ko',
            'action': 'follow',
            'message': 'You must login'}
        )

    if action not in [FOLLOW_ACTION, UNFOLLOW_ACTION]:
        return JsonResponse({
            'status': 'action not defined',
            'message': 'Unknown action {}'.format(action)}
        )

    try:
        user = User.objects.get(id=user_id)
        if action == UNFOLLOW_ACTION:
            Follow.objects.filter(following=request.user, follower=user).delete()
            return JsonResponse({
                'status':'ok',
                'action':'follow'
                })
        else:
            contact, created = Follow.objects.get_or_create( following=request.user, follower=user)
            return JsonResponse({
                'status':'ok',
                'action': 'unfollow',
                'message': 'Following id : {}'.format(contact.id)
            })


    except User.DoesNotExist:
        return JsonResponse({
            'status': 'ko',
            'message': 'user id: does not exist: {}'.format(user_id)
        })



# new function 1
def LoginINAs(request):
    if request.method == "GET":

        template_name = "market/logInAs.html"
        context = {}

        return render(request, template_name, context)

# def Profile(request):
#     user = request.user
#     c = Shop.objects.filter(user=user)
#     if user.is_anonymous or len(c) == 0:
#         print("hey you are not you")
#         return redirect('market:homepage')
#
#     else:
#
#         ad_list = [["1","a"],  ["2", "b"], ["3", "c"]]
#         template_name = "market/profile_index.html"
#         pk = str(c[0].pk)
#         context = {"user" : user, "ad_list": ad_list, "pk": pk}
#         return render(request, template_name, context)


# def public_profile(request, pk):
#
#     u = Shop.objects.filter(pk = pk)
#
#
#     if len(u) == 0:
#         return redirect('market:homepage')
#
#     else:
#         c = u[0]
#         ad_list = [["1","a"],  ["2", "b"], ["3", "c"]]
#         template_name = "market/profile_public.html"
#         pk = str(c.pk)
#         context = {"user" : c, "ad_list": ad_list, "pk": pk}
#         return render(request, template_name, context)



def LogOUT(request):
    user = request.user
    if user is not None:
        logout(request)
    return redirect('market:loginAs')
