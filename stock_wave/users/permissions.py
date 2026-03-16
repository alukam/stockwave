from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

# A Mixin for Class-Based Views
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

# A Decorator for function-based views
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper_func