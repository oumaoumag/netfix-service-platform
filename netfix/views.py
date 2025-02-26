from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from users.models import User, Company, Customer
from services.models import Service, RequestService
from datetime import date


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    user = User.objects.get(username=name)
    requested_services = []
    today = date.today()

    dob = user.customer.date_of_birth
    user_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    requested_services = RequestService.objects.filter(
        user=Customer.objects.get(user=user)
    ).order_by("-date")  

    for service in requested_services:
        service.price = service.service.price_hour * service.hours

    return render(request, 'users/profile.html', {
        'user': user,
        'services': requested_services,
        'user_age': user_age
    })


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")
    return render(request, 'users/profile.html', {'user': user, 'services': services})