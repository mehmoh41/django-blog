from typing import List
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import Post
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from .forms import CommentForm




# Create your views here.
class IndexView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset =  super().get_queryset()
        data = queryset[:3]
        return data
    

# def index(request) :
#     posts = Post.objects.all().order_by("-date")[:3]
#     return render(request , "blog/index.html" , {
#         "posts" : posts
#     })
class PostsView(ListView) :
    template_name = "blog/posts.html"
    model = Post
    context_object_name = "all_posts"

# def posts(request) : 
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request , "blog/posts.html" , {
#         "all_posts" : all_posts
#     })

class SingleView(View) :
    # here we extended View because not only we are getting the data but also posting it
    # template_name = "blog/single-post.html"
    # model = Post
    def is_stored_post(self , request , post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later
    def get(self , request, slug):
        post = Post.objects.get(slug = slug)
        context = {
            "post" : post,
            "post_tags" : post.tags.all(),
            "comment_form" : CommentForm(),
            "comments" : post.comments.all().order_by("-id"),
            "saved_for_later" : self.is_stored_post(request , post.id)
        }
        return render(request , "blog/single-post.html" , context) 
    def post(self , request , slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug = slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("single" , args=[slug]))

        context = {
            "post" : post,
            "post_tags" : post.tags.all(),
            "comment_form" : comment_form,
            "comments" : post.comments.all().order_by("-id"),
            "saved_for_later" : self.is_stored_post(request , post.id)


        }
        return render(request , "blog/single-post.html" , context) 


    
    # this has been used when we extended the DetailView

    # def get_context_data(self, **kwargs):
    #     context =  super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"] =  CommentForm()
    #     return context



# def single(request , slug) :
#     postsWithSlug  = get_object_or_404(Post, slug=slug)

#     return render(request , "blog/single-post.html" , {
#         "post" : postsWithSlug,
#         "post_tags" : postsWithSlug.tags.all()
#     })

class ReadLaterView(View):
    def get(self , request):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request , "blog/store-post.html" , context)


    def post(self , request) :
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])
        
        if post_id is not stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")


