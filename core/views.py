from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, Http404
from django.views.generic import ListView, View, CreateView, DeleteView, DetailView, UpdateView
from django.db.models import Sum
from django.template import loader
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, UpdateProfileForm
from .models import Post, Comment, Profile


class IndexView(ListView):
    model = Post
    template_name = 'core/index.html'
    context_object_name = 'popular_posts'

    def get_queryset(self):
        return self.model.objects.annotate(likes_count=Sum('likes')).order_by('-likes_count')


class FeedView(View):
    template_name = 'core/feed.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            friends = request.user.user_profile.friends.all()
            feed_posts = Post.objects.filter(author__in=friends)
            context = {
                'feed_posts': feed_posts
            }
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)


class CreatePostView(CreateView):
    form_class = PostForm
    template_name = 'core/post_create.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            context['form'] = self.form_class
            context['post_was_created'] = True
        else:
            context['post_was_created'] = False
            context['form'] = form

        return render(request, self.template_name, context)    


class DeletePostView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_delete.html'

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('core:post-delete-success', args=(post_id, ))


class PostView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'
    pk_url_kwarg = 'post_id'
    comment_form = CommentForm

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comments'] = Comment.objects.filter(in_post__id=post_id).order_by('-date_pub')
        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form
        return self.render_to_response(context)
    
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        form = self.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.in_post = post
            comment.save()
            return render(request, self.template_name, context={
                'comment_form': self.comment_form,
                'post': post,
                'comments': Comment.objects.filter(in_post__id=post_id).order_by('-date_pub')
            })
        else:
            return render(request, self.template_name, context={
                'comment_form': form,
                'post': post,
                'comments': Comment.objects.filter(in_post__id=post_id).order_by('-date_pub')
            })


class EditPostView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_edit.html'
    form_class = PostForm

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('core:post-detail', args=(post_id, ))
    
    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            raise Http404()
        return super().get(self, request, post_id, args, kwargs)


class ProfileView(DetailView):
    model = Profile
    template_name = 'core/profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user__id=self.kwargs['user_id'])


class AddRemoveFriend(View):

    def post(self, request, user_id, *args, **kwargs):
        profile = get_object_or_404(Profile, user__id=user_id)
        
        if profile.friends.filter(id=request.user.id).exists():
            friend = profile.friends.get(id=request.user.id)
            profile.friends.remove(friend)
            request.user.user_profile.friends.remove(profile.user)
        else:
            profile.friends.add(request.user)
            request.user.user_profile.friends.add(profile.user)

        return redirect(request.META.get('HTTP_REFERER'), request)


class EditProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'core/edit_profile.html'
    slug_field = 'user_id'
    slug_url_kwarg = 'user_id'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise Http404("Это не Ваш профиль")
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user_id = self.kwargs['user_id']
        return reverse(EditProfileView. self).dispatch(request, *args, **kwargs)

def post_edit(request, post_id):
    response = 'Редактирование поста №{}'.format(post_id)
    return HttpResponse(response)


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.save()

    return redirect(request.META.get('HTTP_REFERER'), request)