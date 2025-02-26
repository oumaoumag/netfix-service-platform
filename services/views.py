from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service
from .forms import CreateNewService, RequestServiceForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


@login_required
def create(request):
    try:
        company = Company.objects.get(user = request.user)
    except Company.DoesNotExist:
        redirect('/')
        
    services_offered = Company.objects.filter(user = request.user).values_list('field', flat=True).distinct()
    choices = [(field, field) for field in services_offered]
    
    if any(choices[0]=='All in One' for choice in choices):
        choices = [(field, field) for field, _ in Company._meta.get_field("field").choices if field != 'All in One']
        
        
    form = CreateNewService(choices=choices)
    
    
    if request.method == "POST":
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            service = form.save(commit = False)
            service.company = company
            service.save()
            return redirect(f'/services/{service.id}')
    else:
        form = CreateNewService(choices=Service.choices)  # Pass choices

    return render(request, 'services/create.html', {'form': form})



def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    service = get_object_or_404(Service, id=id)
    user = get_object_or_404(Customer, user = request.user)
    form = RequestServiceForm()
    if request.method == "POST":
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            request_service = form.save(commit=False)
            request_service.service = service
            request_service.user = user
            request_service.save()
            return redirect(f'/customer/{request.user.username}')
    else:
        form = RequestServiceForm()
    return render(request, 'services/request_service.html', {'form': form})
