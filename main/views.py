from django.shortcuts import render, redirect
from django.db.models import Count, OuterRef, Subquery

from django.contrib.auth import logout as auth_logout
from services.models import Service, RequestService



def home(request):
    service_counts = (
    RequestService.objects
    .values("service_id")
    .annotate(request_count=Count("id"))
    .order_by("-request_count")
)

# Step 2: Get the latest RequestService entry for each service_id
    latest_service = (
    RequestService.objects
    .filter(service_id=OuterRef("service_id"))
    .order_by("-date")  # Get latest entry for each service_id
    .values("id")[:1]
)

# Step 3: Get full model instances & related service info
    services = (
    RequestService.objects
    .filter(id__in=Subquery(latest_service))
    .annotate(request_count=Subquery(
        service_counts.filter(service_id=OuterRef("service_id")).values("request_count")[:1]
    ))
    .order_by("-request_count")
    .select_related("service")  # Fetch related service details
)

    for service in services:
        service.price = service.service.price_hour * service.hours  


    return render(request, "main/home.html", {'services':services})

    #return render(request, "main/home.html", {})


def logout(request):
    auth_logout(request)
    return render(request, "main/logout.html")
