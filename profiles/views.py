from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from followers.models import Follower
from django .views.generic import DetailView,View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponseBadRequest
from feed.models import Post
# Create your views here.

class ProfileDeytailView(DetailView):
    http_method_names=["get"]
    template_name="profiles/detail.html"
    model=User
    context_object_name="user"
    slug_field="username"
    slug_url_kwarg="username"

    def dispatch(self, request, *args, **kwargs) :
        self.request=request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        user=self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        
        if self.request.user.is_authenticated:
            context['you_following']=Follower.objects.filter(following=user,followed_by=self.request.user).exists
        
        return context

class FollowView(LoginRequiredMixin, View):
    http_method_names=["post"]

    def post(self,request,*args, **kwargs):
        data = request.POST.dict()
        if "action" not in data or "username" not in data:

            return HttpResponseBadRequest("missing data")
        try:
            other_user=User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("missing user")
        
        if data['action']=="follow":
            #follow
            follower,created=Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user,
            )
        else:
            #unfollow
            try:
                follower=Follower.objects.get(
                    followed_by=request.user,
                    following=other_user,
                )
            except follower.DoesNotExist:
                follower=None
            if follower:
                follower.delete()
                
        return JsonResponse({
            'success' :True,
            'wording': "unfollow" if data['action']=="follow" else "follow"
        })
        
class FollowerPage(TemplateView):
    http_method_names=["get"]
    template_name="profiles/followers.html"

    def dispatch(self, request, *args, **kwargs):
        self.request=request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self,*args ,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        if self.request.user.is_authenticated:
            following=list(Follower.objects.filter(followed_by=self.request.user).values_list('following',flat=True))
            post=Post.objects.filter(author__in=following).order_by('-id')[0:60]
            context['posts']=post
        else:
            
           pass
       
        return context