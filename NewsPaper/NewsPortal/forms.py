from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['name', 'text', 'author', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        name = cleaned_data.get("name")

        if name == text:
            raise ValidationError(
                "Текст не должен быть идентичен названию."
            )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
