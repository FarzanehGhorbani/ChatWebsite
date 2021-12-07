from django import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.forms import fields
from .models import Profile

class ChangeProfileImage(forms.Form):
    image= forms.ImageField()

class EditUserForm(forms.Form):

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'} ), required=False
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Location', 'class': 'form-control'} ), required=False
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),required=False
    )

    # image = forms.ImageField(required=False)




class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput())

    password = forms.CharField(widget=forms.PasswordInput())

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربری با مشخصات وارد شده ثبت نام نکرده است')

        return user_name


class RegisterForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(),
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(3, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(),
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')

        return email

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user_by_username = User.objects.filter(username=user_name).exists()

        if is_exists_user_by_username:
            raise forms.ValidationError('این کاربر قبلا ثبت نام کرده است')

        return user_name

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password

    