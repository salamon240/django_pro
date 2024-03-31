#from django.shortcuts import render waen we use function 
from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.shortcuts import render
# Create your views here.

class HomePage(ListView):
    http_method_names=["get"]
    template_name="feed/homepage.html"
    model=Post
    context_object_name="posts"
    queryset=Post.objects.all().order_by('-id')[0:30]

class PostDetailView(DetailView):
    http_method_names=["get"]
    template_name="feed/detail.html"
    model=Post
    context_object_name="post"
    
class CreatNewPost(LoginRequiredMixin,CreateView):
    template_name="feed/create.html"
    model=Post
    fields=['text']
    success_url="/"
    def dispatch(self, request, *args, **kwargs):
        self.request=request
        return super().dispatch(request, *args, **kwargs)
    
    
    def form_valid(self, form):
        obj=form.save(commit=False)
        obj.author=self.request.user
        obj.save()
        return super().form_valid(form)
    
    #wean you creat a new post 
    def post(self, request, *args, **kwargs):
        post=Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )
        
        return render(
            request,
            "include/post.html",
            {
                "post":post,
                "show_detail_link":True,
            },
            content_type="application/html"
        )
    