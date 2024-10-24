from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from students.models import User, Student


class BusinessUserSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-12'}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-12'}))
    # cell_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_(
        'Password verification'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    field_order = ['username', 'first_name', 'last_name',
                   'email', 'company_name', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'company_name', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        cleaned_data = super(BusinessUserSignupForm, self).clean()
        user = super().save(commit=False)
        user.is_student = False
        user.is_teacher = False
        user.is_super = False
        user.is_business = True
        user.username = user.email
        user.set_password(cleaned_data['password1'])
        user.save()
        return user
