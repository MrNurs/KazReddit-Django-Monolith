from django.http import Http404, HttpResponse
from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

from .models import Subreddit, Post, Comment
from django.urls import reverse_lazy

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('core:login')

class SubredditView(generic.ListView):
    context_object_name = 'subreddits'
    template_name = 'core/subreddits.html'
    def get_queryset(self):
        return Subreddit.objects.all()

class PostView(generic.ListView):
    context_object_name = 'posts'

    template_name = 'core/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subreddit_name'] = self.kwargs['subreddit_name']
        return context

    def get_queryset(self):
        subreddit_name = self.kwargs.get('subreddit_name')

        try:
            subreddit = Subreddit.objects.get(name=subreddit_name)
        except Subreddit.DoesNotExist:
            raise Http404("Subreddit does not exist")

        return Post.objects.filter(subreddit=subreddit.id)



class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'core/post_comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subreddit_name'] = self.kwargs.get('subreddit_name')
        comment_id = self.kwargs['post_id']
        context['comments'] = Comment.objects.filter(post_id=comment_id, parent=None)
        return context


    def get_object(self, queryset=None):
        subreddit_name = self.kwargs.get('subreddit_name')
        post_id = self.kwargs.get('post_id')

        try:
            subreddit = Subreddit.objects.get(name=subreddit_name)
        except Subreddit.DoesNotExist:
            raise Http404("Subreddit does not exist")

        try:
            post = Post.objects.get(subreddit=subreddit, id=post_id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")
        return post
