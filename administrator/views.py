from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_admin

@user_passes_test(is_admin, login_url='no_permission_page')
def Dashboard(request):
    return HttpResponse("<h1>Dashboard from admin panel</h1>")

@user_passes_test(is_admin, login_url='no_permission_page')
def Users(request):
    return HttpResponse("<h1>view or edit Users</h1>")

@user_passes_test(is_admin, login_url='no_permission_page')
def CreateUser(request):
    return HttpResponse("<h1>CreateUsers in admin</h1>")

@user_passes_test(is_admin, login_url='no_permission_page')
def Profile(request):
    return HttpResponse("<h1>view or edit profile</h1>")

@user_passes_test(is_admin, login_url='no_permission_page')
def Recruiters(request):
    return HttpResponse("<h1>Recruiters request</h1>")

@user_passes_test(is_admin, login_url='no_permission_page')
def Logs(request):
    return HttpResponse("<h1>Admin logs</h1>")


