from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from users.models import User, Company
from services.models import Service


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request):
    pass


def company_profile(request):
    if not hasattr(request.user, 'company'):
        return HttpResponseForbidden("you do not currently have services or acces to this page")
    # fetches the company user and all of the services available by it
    #if name is None:
     #   return HttpResponse("Company name is required",status=400)
    company = request.user.company
    services = Service.objects.filter(company=company).order_by("-date")
   # services = Service.objects.filter(
    #    company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/company_profile.html', {'company': company, 'services': services})
