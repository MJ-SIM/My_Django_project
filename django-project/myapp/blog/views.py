from django.shortcuts import render, redirect 
from typing import Any
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Post, Comment, HashTag
from .forms import PostForm, CommentForm, HashTagForm



# Create your views here.
class Index(View):
    
    def get(self, request):
        posts = Post.objects.all()
        context = {
            "posts": posts,
            "title": "Blog"
        }
        return render(request, 'blog/post_list.html', context)


class Write(LoginRequiredMixin, View):
    redirect_field_name='next'
    def get(self, request):
        next_path = request.GET.get('next')
        form = PostForm()
        context = {
            'form':form,
            'title': 'Blog'
        }
        return render(request, 'blog/post_form.html', context)
    def post(self, request):
        form = PostForm(request.POST) 
        if form.is_valid(): 
            post=form.save(commit=False)
            post.writer= request.user 
            post.save()
            return redirect('blog:list')
        form.add_error(None, '폼이 유효하지 않습니다')
        context={
            'form': form
        }
        return render(request, 'blog/post_form.html')


class DetailView(View):
    def get(self, request, pk): 
        post = Post.objects.prefetch_related('comment_set', 'hashtag_set').get(pk=pk)
        comments = post.comment_set.all()
        hashtags = post.hashtag_set.all()
        comment_form = CommentForm()
        hashtag_form = HashTagForm()
        context = {
            "title": "Blog",
            'post_id': pk,
            'post_title': post.title,
            'post_content': post.content,
            'post_writer': post.writer,
            'post_created_at': post.created_at,
            'comments': comments,
            'hashtags': hashtags,
            'comment_form': comment_form,
            'hashtag_form': hashtag_form,
        }
        return render(request, 'blog/post_detail.html', context)


class Update(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(initial={'title':post.title, 'content':post.content})
        context={
            'form':form,
            'post':post,
            'title': 'Blog'
        }
        return render(request, 'blog/post_edit.html', context)
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('blog:detail', pk=pk)
        context = {
            'form': form,
            "title": "Blog"
        }
        return render(request, 'blog/post_edit.html',context)


class Delete(View):
    def post(self, request, pk): # post_id
        ## try, except
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        
        post.delete()
        return redirect('blog:list')


class CommentWrite(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        try:
            post = Post.objects.get(pk=pk) 
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        if form.is_valid(): 
            content = form.cleaned_data['content']
            writer=request.user
            try:
                comment = Comment.objects.create(post=post, content=content, writer=writer)
            except ObjectDoesNotExist as e:
                print('Post does not exist', str(e))
            except ValidationError as e:
                print('Validation error occurred', str(e))
            return redirect('blog:detail', pk=pk)
        hashtag_form = HashTagForm()
        context = {
            "title": "Blog",
            'post_id': pk,
            'comments': post.comment_set.all(),
            'hashtags': post.hashtag_set.all(),
            'comment_form': form,
            'hashtag_form': hashtag_form
        }
        return render(request, 'blog/post_detail.html', context)


class CommentDelete(View):
    def post(self, request, pk): 
        try:
            comment = Comment.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Comment does not exist.', str(e))
        post_id = comment.post.id
        comment.delete()
        return redirect('blog:detail', pk=post_id)


class HashTagWrite(View):
    def post(self, request, pk):
        form = HashTagForm(request.POST)
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Comment does not exist.', str(e))
        if form.is_valid():
            name = form.cleaned_data['name']
            writer=request.user
            try:
                hashtag = HashTag.objects.create(post=post, name=name, writer=writer)    
            except ObjectDoesNotExist as e:
                print('Post does not exist.', str(e))
            except ValidationError as e:
                print('Valdation error occurred', str(e))
            return redirect('blog:detail', pk=pk)
        comment_form = CommentForm()
        context={
            'title': 'Blog',
            'post_id':pk,
            'comments':post.comment_set.all(),
            'hashtags':post.hashtag_set.all(),
            'comment_form':comment_form,
            'hashtag_form': form
        }
        return render(request, 'blog/post_detail.html', context)


class HashTagDelete(View):
    def post(self, request, pk):
        try:
            hashtag = HashTag.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('HashTag does not exist.', str(e))
        post_id = hashtag.post.id
        hashtag.delete()
        return redirect('blog:detail', pk=post_id)