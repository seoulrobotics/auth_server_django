import re
from django.core import exceptions

from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .forms import LoginForm, SignupForm, EnableAuthForm
from .models import ProductAuth, Product


# signup

def get_user_with_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/login_redirect/')

    else:
        if request.method == "POST":
            form = SignupForm(request.POST)
            if form.is_valid():
                if get_user_with_email(form.cleaned_data['email']) is not None:
                    error = 'Email already exists. Try again with another email'
                    context = {
                        'form': form,
                        'error': error
                    }
                    return render(request, 'sr_auth/signup.html', context)
                new_user = User.objects.create_user(**form.cleaned_data)
                new_user.is_active = True
                return HttpResponseRedirect(reverse('login'))
                # return render(request, 'sr_auth/signup.html', context)
            return render(request, 'sr_auth/signup.html', {'form': form})
        # get
        else:
            form = SignupForm()
            context = {
                'form': form
            }
            return render(request, 'sr_auth/signup.html', context)

# login


def login_user(request):
    """Checks logged in status"""
    if request.user.is_authenticated:
        next_url = request.GET.get('next')
        if next_url:
            response = HttpResponseRedirect(next_url)
            response.set_cookie('username', request.user.username)
            return response
        else:
            response = HttpResponseRedirect('/login_redirect/')
            response.set_cookie('username', request.user.username)
            return response
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            id = request.POST['username']
            pw = request.POST['password']
            user = authenticate(username=id, password=pw)
            if user is not None:
                login(request, user=user)
                next_url = request.GET.get('next')
                if next_url:
                    response = HttpResponseRedirect(next_url)
                    response.set_cookie('username', user.username)
                    return response
                else:
                    response = HttpResponseRedirect(reverse('login_redirect'))
                    response.set_cookie('username')
                    return response
            else:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    if not user.is_active:
                        error = 'Email is not verified. Please check your email'
                    else:
                        error = 'Password is incorrect'
                except:
                    error = 'We cannot find an account with that ID'

                context = {
                    'form': form,
                    'error': error
                }
                return render(request, 'sr_auth/login.html', context)

        # get
        else:
            form = LoginForm()

        return render(request, 'sr_auth/login.html', {'form': form})


@login_required(login_url="/login")
def logout_user(request):
    if request.GET.get('clicked'):
        logout(request)
        next_url = request.GET.get('next')
        if next_url:
            response = HttpResponseRedirect(next_url)
            response.delete_cookie('username')
            return response
        else:
            response = HttpResponseRedirect('/login/')
            response.delete_cookie('username')
            return response
    else:
        return render(request, 'sr_auth/logout.html')


@login_required(login_url="/login")
def login_redirect(req):
    return render(req, 'sr_auth/login_redirect.html')




def enable_auth_impl(product_name, user,  is_enable):
    product = Product.objects.get(name=product_name)
    product_auth = ProductAuth.objects.get(
        product=product)
    if user.has_perm('can_enable_auth', product_auth):
        changed = product_auth.enabled != is_enable
        if changed:
            product_auth.enabled = is_enable
            product_auth.save()
    else:
        raise Exception("User do not have permission")


@login_required(login_url="/login")
def enable_auth(request, product_name):
    try:
        is_enable = request.POST.get('enable') == 'true'
        enable_changed = enable_auth_impl(product_name, request.user, is_enable)
        return Response(enable_changed)
    except:
        pass
    return Response(status=status.HTTP_404_NOT_FOUND)


@login_required(login_url="/login")
def auth_status(request, product_name):
    product = Product.objects.get(name=product_name)
    product_auth = ProductAuth.objects.get(
        product=product)
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = EnableAuthForm(
            request.POST, current_val=product_auth.enabled, product_name=product_name)
        # Check if the form is valid:/
        if form.is_valid():
            is_enabled = form.cleaned_data['enable']
            try:
                enable_auth_impl(
                    product_name, request.user, is_enabled)
                form = EnableAuthForm(
                    current_val=is_enabled, product_name=product_name)
                context = {
                    'form': form,
                    'product': product.name,
                    'product_auth_enabled': is_enabled,
                    'auth_enable_permission': request.user.has_perm('can_enable_auth', product_auth),
                }
                return render(request, 'sr_auth/enable_auth.html', context)
            except Exception as e:
                print(e)
        context = {
            'permission_info': f'get status of {product.name} authentication'
        }
        return render(request, 'sr_auth/error_no_permission.html', context)
    # If this is a GET (or any other method) create the default form.
    else:

        is_enable = product_auth.enabled
        form = EnableAuthForm(current_val=product_auth.enabled, product_name=product_name)
        context = {
            'form': form,
            'product': product.name,
            'product_auth_enabled': is_enable,
            'auth_enable_permission': request.user.has_perm('can_enable_auth', product_auth),
        }
        return render(request, 'sr_auth/enable_auth.html', context)


@require_GET
@login_required(login_url="/login")
def can_use(request, product_name):
    """Checks is user is authorized for this product."""
    try:
        product = Product.objects.get(name=product_name)
        product_auth = ProductAuth.objects.get(
            product=product)
        if request.user.has_perm('can_enable_auth', product_auth):
            return Response("can use product")
    except:
        pass
    return Response(status=status.HTTP_404_NOT_FOUND)
