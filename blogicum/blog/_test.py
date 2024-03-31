class PostListView(ListView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/index.html'
    ordering = 'id'

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})