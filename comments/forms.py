# -*- coding: utf-8 -*-
from django import forms
from .models import Comment

# Create your models here.


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

