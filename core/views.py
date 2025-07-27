from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Subreddit, Post, Comment, Vote
from django.urls import reverse_lazy
from django.db.models import F
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/kazreddit')

class ProfileView(TemplateView):
    template_name = 'core/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userName'] = self.request.user.username
        return context

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('core:login')

class SubredditView(generic.ListView):
    context_object_name = 'subreddits'
    template_name = 'core/subreddits.html'
    def get_queryset(self):
        return Subreddit.objects.all()

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('core:login')

        title = request.POST.get('title')
        desc = request.POST.get('desc')

        if title and desc:
            Subreddit.objects.create(name=title, detail=desc)
            return redirect('core:index')


class PostView(generic.ListView):
    context_object_name = 'posts'

    template_name = 'core/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subreddit_name'] = self.kwargs['subreddit_name']
        context['subreddit_object'] = Subreddit.objects.get(name=self.kwargs['subreddit_name'])

        return context

    def get_queryset(self):
        subreddit_name = self.kwargs.get('subreddit_name')

        try:
            subreddit = Subreddit.objects.get(name=subreddit_name)
        except Subreddit.DoesNotExist:
            raise Http404("Subreddit does not exist")

        return Post.objects.filter(subreddit=subreddit.id)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')

        subreddit_name = self.kwargs.get('subreddit_name')
        try:
            subreddit = Subreddit.objects.get(name=subreddit_name)
        except Subreddit.DoesNotExist:
            raise Http404("Subreddit does not exist")

        title = request.POST.get('title')
        desc = request.POST.get('desc')

        if title and desc:
            Post.objects.create(
                subreddit=subreddit,
                title=title,
                text=desc,
                author=request.user.username
            )
            return redirect('core:posts', subreddit_name=subreddit_name)

        return self.get(request, *args, **kwargs)

class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'core/post_comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subreddit_name'] = self.kwargs.get('subreddit_name')
        context['comments'] = Comment.objects.filter(post=self.object, parent=None)
        return context

    def get_object(self, queryset=None):
        subreddit_name = self.kwargs.get('subreddit_name')
        post_id = self.kwargs.get('post_id')
        subreddit = get_object_or_404(Subreddit, name=subreddit_name)
        return get_object_or_404(Post, subreddit=subreddit, id=post_id)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')

        subreddit_name = kwargs.get('subreddit_name')
        post_id = kwargs.get('post_id')
        post = self.get_object()


        if 'likesNdis' in request.POST:
            return self.handle_vote(request, post, subreddit_name, post_id)

        if 'delete_comment_id' in request.POST:
            return self.handle_delete_comment(request, subreddit_name, post_id)

        return self.handle_add_comment(request, post, subreddit_name, post_id)

    def handle_vote(self, request, post, subreddit_name, post_id):
        vote_type = request.POST.get('likesNdis')
        comment_id = request.POST.get('comment_id')

        if not comment_id:
            return redirect('core:post', subreddit_name=subreddit_name, post_id=post_id)

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise Http404("Comment does not exist")

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            comment=comment
        )

        if not created and vote.vote_type == vote_type:
            vote.delete()
            self.update_comment_count(comment, vote_type, increment=False)
        elif not created:
            old_vote_type = vote.vote_type
            vote.vote_type = vote_type
            vote.save()
            self.update_comment_count(comment, old_vote_type, increment=False)
            self.update_comment_count(comment, vote_type, increment=True)
        else:
            vote.vote_type = vote_type
            vote.save()
            self.update_comment_count(comment, vote_type, increment=True)

        return redirect('core:post', subreddit_name=subreddit_name, post_id=post_id)

    def update_comment_count(self, comment, vote_type, increment):
        change = 1 if increment else -1
        if vote_type == 'like':
            Comment.objects.filter(id=comment.id).update(like=F('like') + change)
        else:
            Comment.objects.filter(id=comment.id).update(dislike=F('dislike') + change)

    def handle_delete_comment(self, request, subreddit_name, post_id):
        delete_comment_id = request.POST.get('delete_comment_id')
        comment = get_object_or_404(Comment, id=delete_comment_id)

        if comment.author == request.user.username:
            comment.delete()

        return redirect('core:post', subreddit_name=subreddit_name, post_id=post_id)

    def handle_add_comment(self, request, post, subreddit_name, post_id):
        text = request.POST.get('comment')
        parent_id = request.POST.get('parent')

        if text:
            comment = Comment(
                post=post,
                text=text,
                author=request.user.username
            )

            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment

            comment.save()

        return redirect('core:post', subreddit_name=subreddit_name, post_id=post_id)