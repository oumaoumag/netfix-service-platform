from django.shortcuts import render, redirect
from django.db.models import Count

from django.contrib.auth import logout as auth_logout
from services.models import Service, RequestService



def home(request):
    most_requested_services = Service.objects.annotate(
        request_count=Count('requestservice')
    ).order_by('-request_count')[:3]  # Get top 5 most requested services
    print(most_requested_services)
    return render(request, 'main/home.html', {
        'most_requested_services': most_requested_services
    })
    #return render(request, "main/home.html", {})


def logout(request):
    auth_logout(request)
    return render(request, "main/logout.html")
