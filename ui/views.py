from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def search_page(request: HttpRequest) -> HttpResponse:
    return render(request, "ui/search.html")


@login_required
def detail_page(request: HttpRequest) -> HttpResponse:
    return render(request, "ui/detail.html", context={
        "key": request.GET["key"]
    })
