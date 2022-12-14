import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, HTML



class LoginForm(forms.Form):
    username = forms.CharField(label='ID')
    password = forms.CharField(label=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        initial_username = "admin"
        if 'user_initial' in kwargs:
            initial_username = kwargs.pop('user_initial')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('username', css_class='form-control mb-4'),
                    css_class='sr_hidden_input'
                ),
                Column(
                    Field('password', css_class='sr_input mb-4 sr_text'),
                    css_class="w-100"
                ),
                css_class='form-row sr_text'
            ),
            Row(
                Submit('submit', 'Access', css_class='sr_button w-100'),
                css_class='form-row'
            )
        )
        self.fields['username'].initial = initial_username


class SignupForm(forms.ModelForm):
    username = forms.CharField(label='ID')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                 Column(
                    Field('email', css_class='form-control mb-4'),
                    css_class='col-sm-12'
                ),
                css_class='form-row'
            ),
            Row(
                Column(
                    Field('username', css_class='form-control mb-4'),
                    css_class='col-sm-6'
                ),
               
                Column(
                    Field('password', css_class='form-control mb-4'),
                    css_class='col-sm-6'
                ),
                css_class='form-row'
            ),
            HTML('<input type="hidden" id="g-recaptcha-response" name="g-recaptcha-response">'),
            Row(
                Submit('submit', 'Sign up', css_class='btn btn-primary w-100 m-1'),
                css_class='form-row'
            )
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class EnableAuthForm(forms.Form):
    enable = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        current_val = kwargs.pop('current_val')
        product_name = kwargs.pop('product_name')


        super(EnableAuthForm, self).__init__(*args, **kwargs)
        self.fields['enable'].initial = not current_val
        self.fields['enable'].label = f"Enable {product_name} authentication."


