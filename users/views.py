from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    return render(request, 'users/register.html')


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def LoginUserView(request):
    form = AuthenticationForm()
    
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.changed_data['email']
            password = form.changed_data['password']
            user = authenticate(request, username=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                form.add_error(None, "Invalid email or password")
               
        
    return render(request, "users/login.html", {"form":form})
   
