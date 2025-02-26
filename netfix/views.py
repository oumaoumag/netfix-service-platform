from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from users.models import User, Company
from services.models import Service


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request):
    pass


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")
    return render(request, 'users/profile.html', {'user': user, 'services': services})