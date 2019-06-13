# coding=utf-8
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect


def logout_view(request):
    """
    Logout
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect("/user/login")


def login_view(request):
    """
    Login page
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            print("User {} has login.".format(form.get_user()))
            try:
                next_page = request.GET["next"]
            except:
                next_page = "/"
            return redirect(next_page)
        else:
            print("User {} login failed.".format(form.get_user()))
    try:
        token = request.COOKIES['csrftoken']
    except:
        token = get_token(request)
    return render(
        request,
        'login.html', context={
            "csrf_token": token
        }
    )
