from django import forms
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from courses.models import Course
from students.models import (
    Answer,
    Question,
    #Student,
    StudentAnswer,
    Tag,
    User
)

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)


class TeacherSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=_('Password verification'), widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    cell_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
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
        return user


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text',)


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.all(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None
    )

    class Meta:
        model = StudentAnswer
        fields = ('answer',)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args,**kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
