from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from .constants import NUMBER_OF_POSTS
from .forms import CommentForm, PostForm
from .mixins import DeleteMixin
from .models import Category, Comment, Post


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = NUMBER_OF_POSTS
    queryset = Post.objects.filter_posts_for_users()


class PostDetailView(ListView):
    model = Comment
    template_name = 'blog/detail.html'
    paginate_by = NUMBER_OF_POSTS

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if self.request.user == post.author:
            return post
        return get_object_or_404(Post.objects.filter_posts_for_users(),
                                 pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_object()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if self.request.user != post.author:
            return HttpResponseRedirect(
                reverse('blog:post_detail',
                        kwargs={'post_id': self.kwargs['post_id']})
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class PostDeleteView(DeleteMixin):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(DeleteMixin):
    template_name = 'blog/comment.html'
    model = Comment
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class CategoryDetailView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = NUMBER_OF_POSTS
    slug_url_kwarg = 'category_slug'

    def get_category(self):
        return get_object_or_404(
            Category, slug=self.kwargs['category_slug'], is_published=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context

    def get_queryset(self):
        return self.get_category().posts.filter_posts_for_users()


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = NUMBER_OF_POSTS

    def get_profile(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        posts = self.get_profile().posts
        if self.request.user.username == self.kwargs['username']:
            return posts.filter_posts_for_author(self.request.user)
        return posts.filter_posts_for_users()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('first_name', 'last_name', 'email')
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})
