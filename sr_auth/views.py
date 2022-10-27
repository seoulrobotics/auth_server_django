from cmath import exp
import json
import re
from django.core import exceptions
import datetime
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse

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
        print("logged in")
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
        print("trying logged in")

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


# auth

#invalidates all login session cookies, useful when auth have changed
def remove_all_sessions():
    all_sessions = Session.objects.filter(
        expire_date__gte=timezone.now())
    for session in Session.objects.all():
        session.delete()


def enable_auth_impl(product_name, user, is_enable):
    product = Product.objects.get(name=product_name)
    product_auth = ProductAuth.objects.get(
        product=product)
    if user.has_perm('can_enable_auth', product_auth):
        changed = product_auth.enabled != is_enable
        if changed:
            product_auth.enabled = is_enable
            product_auth.save()
            remove_all_sessions()
    else:
        raise Exception("User do not have permission")


@login_required(login_url="/login")
@api_view(['POST'])
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
            'error_msg': f'Sorry, you do not have permission for {product_name}.'
        }
        return render(request, 'sr_auth/error.html', context)
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



@login_required(login_url="/login")
@api_view(['GET'])
def can_use_redirect(request, product_name):
    """Checks is user is authorized for this product. Redirect to login if needed."""
    reply, tkn_key, tkn_val = can_use_impl(request, product_name)
    next_url = request.GET.get('next')
    manual_cookie_expires = datetime.datetime.now() + datetime.timedelta(days=365)
    if reply["result"] == True:

        if next_url:
            response =  HttpResponseRedirect(next_url)
            response.set_cookie(
                tkn_key, value=tkn_val, expires=manual_cookie_expires)
            return response
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        logout(request)
        context = {
            'error_msg': f'Error code: {reply["cause"]}.',
        }
        if next_url:
            context['return_addr'] = next_url
        return render(request, 'sr_auth/error.html', context)


@api_view(['GET'])
def can_use(request, product_name):
    """Checks is user is authorized for this product."""
    reply, tkn_key, tkn_val =  can_use_impl(request, product_name)
    manual_cookie_expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response = JsonResponse(reply)
    response.set_cookie(
        tkn_key, value=tkn_val, expires=manual_cookie_expires)
    return response


def can_use_impl(request, product_name):
    """Checks is user is authorized for this product."""
    reply = {"result": False, "cause": "unknown"}
    cookie_val = "disabled"
    prod_auth_found = False
    try:
        product = Product.objects.get(name=product_name)
    except:
        reply["cause"] = "unknown_product"
    try:
        product_auth = ProductAuth.objects.get(product=product)
        prod_auth_found = True
    except:
        reply["cause"] = "auth_not_setup"
    
    if prod_auth_found:
        if not product_auth.enabled:
            reply["result"] = True
            reply["cause"] = "auth_disabled"

        elif not request.user.is_authenticated:
            reply["result"] = False
            reply["cause"] = "user_not_logged_in"

        elif request.user.has_perm('can_enable_auth', product_auth):
            reply["result"] = True
            reply["cause"] = "has_use_permission"
            #TODO: Contents of auth success cookie does not matter for now, in future, this is value given to SENSR to be cross checked with auth server again
            # auth server -> WebFE -> SENSR -> auth server(cross check)
            cookie_val = request.session.session_key
    
    print(reply)
    return reply, f'use_authorization_{product_name}', cookie_val




@api_view(['GET'])
def get_auth_enabled(request, product_name):
    """Checks is user is authorized for this product."""
    try:
        product = Product.objects.get(name=product_name)
        product_auth = ProductAuth.objects.get(
            product=product)
        return Response(product_auth.enabled)
    except:
        return Response(False)
