from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import DeleteView


class DeleteMixin(LoginRequiredMixin, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
