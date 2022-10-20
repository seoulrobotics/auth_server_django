from django.core import exceptions

from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, SignupForm
from django.conf import settings




from django.contrib.admin.views.decorators import staff_member_required



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
                    return render(request, 'auth_test/signup.html', context)
                new_user = User.objects.create_user(**form.cleaned_data)
                new_user.is_active = True
                return HttpResponseRedirect(reverse('login'))
                # return render(request, 'auth_test/signup.html', context)
            return render(request, 'auth_test/signup.html', {'form': form})
        #get
        else:
            form = SignupForm()
            context = {
                'form': form
            }
            return render(request, 'auth_test/signup.html', context)


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
                return render(request, 'auth_test/login.html', context)

        #get
        else:
            form = LoginForm()
        
        return render(request, 'auth_test/login.html', {'form': form})


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
        return render(request, 'auth_test/logout.html')


@login_required(login_url="/login")
def login_redirect(req):
    return render(req, 'auth_test/login_redirect.html')




