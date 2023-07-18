from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views import View
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy


# Create your views here.
class View(View):
    def get(self, request):
        post = Post.objects.all()
        context = {
            'posts': post
        }
        return render(request,'blog/post_list.html', context)
    

class Write(CreateView):
    model = Post #모델
    form_class = PostForm #어떤 폼을 사용할건지
    success_url = reverse_lazy('blog:list') #성공할 경우 보내줄 url


class Detail(DetailView):
    model = Post
    template_name ='blog/post_detail.html'
    context_object_name='post'


class Update(UpdateView):
    model = Post
    template_name='blog/post_edit.html'
    fields = ['title', 'content']
    def get_initial(self):
        initial = super().get_initial()
        post = self.get_object()
        initial['title'] = post.title
        initial['content'] = post.content
    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('blog:detail', kwargs={'pk':post.pk})