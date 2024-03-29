from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse

from blog.forms import PostForm, CommentForm
from blog.models import Comment, Post


class AuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class PostMixin(AuthorMixin, LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect('blog:post_detail',
                        self.kwargs[self.pk_url_kwarg])

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class CommentMixin(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})
