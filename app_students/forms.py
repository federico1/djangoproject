from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import transaction

from students.models import Student, User


class StudentSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    cell_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    image = forms.CharField(widget=forms.HiddenInput(), required=False)
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=_('Password verification'), widget=forms.PasswordInput(attrs={'class':'form-control'}))

    field_order = ['username', 'email', 'first_name', 'last_name', 'cell_number', 'image', 'password1', 'password2']

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'cell_number', 'image', 'password1', 'password2', )

    @transaction.atomic
    def save(self, commit=True):
        cleaned_data = super(StudentSignupForm, self).clean()
        user = super().save(commit=False)
        user.is_student = True
        user.username = user.email
        user.set_password(cleaned_data['password1'])
        user.save()
        student = Student.objects.create(user=user)
        return user