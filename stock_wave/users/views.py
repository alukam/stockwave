from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import AttendantRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

class IMSLoginView(LoginView):
    """
    Handles user login and checks if the Admin has approved the account.
    """
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # If already logged in, skip login page

    def form_valid(self, form):
        user = form.get_user()
        
        # Check if the custom 'is_approved' flag is True
        if not user.is_approved:
            messages.error(
                self.request, 
                "Your account is pending Admin approval. Please contact the supervisor."
            )
            return redirect('login')
            
        return super().form_valid(form)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # <--- Locked until you approve in Admin
            user.save()
            messages.success(request, "Registration successful! Please ask the Manager to activate your account.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})