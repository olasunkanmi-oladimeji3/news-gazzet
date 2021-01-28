from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Category,Post

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import PostForm 
# Create your views here.
def homeview(request,category_slug=None):
    category=None
    post =Post.objects.all()
    catalog= Category.objects.all()
    
    
    #category
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        post=post.filter(category=category)
    

    #Archives
    post_lists = post.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #post
    post_list = post.filter(published_date__lte=timezone.now()).order_by('-published_date')

    #pagination
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 9)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            queryset = (Q(context__icontains=query)|Q(title__icontains=query))
            #I assume "text" is a field in your model
            #i.e., text = model.TextField()
            #Use | if searching multiple fields, i.e., 
            #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
            results = Post.objects.filter(queryset).distinct()
    else:
       results = []

    context= {
        'category':category,
        'users': users,
        'post_lists':post_lists,
        'catalog':catalog,
        'results':results,
        'query':query
        
        
    }

    return render(request,'core/home.html',context)


def postview(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post_lists = Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(post_lists, 10)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    context={'post':post,'items':items}
    
    return render(request,'core/posts.html',context)


def aboutview(request):
    return render(request,'core/about.html')

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'core/posts.html'

    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'core/posts.html'
    template_name ='core/edit.html'
    form_class = PostForm

    model = Post


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('zenithal:post_draft_list')


class DraftListView(LoginRequiredMixin,ListView):
    model = Post

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('zenithal:post_detail', pk=pk)