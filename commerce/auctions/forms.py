from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.fields import CharField, DecimalField, IntegerField, TextField
from django.forms import widgets
from django.forms.fields import ImageField
from django.forms.widgets import HiddenInput, Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import views, models



class NewListing(forms.Form):
    title = forms.CharField(label="Title: ")
    description = forms.CharField(label="Description: ", widget=forms.Textarea)
    start_bid = forms.CharField(label="Starting bid: ")
    img_url = forms.URLField(label="Image: ", required=False)
    category = forms.ModelChoiceField(label="Category: ", queryset=models.Category.objects.all(), required=False)

class BidForm(forms.Form):
    bid = forms.DecimalField(label="Your bid:")

class CommentForm(forms.Form):
    comment_txt = forms.CharField(label="", widget=forms.Textarea, required=False)
    
