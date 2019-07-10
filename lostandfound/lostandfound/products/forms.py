from django import forms
from django.db import models
from products.models import Lost_Product, ProductImage

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class LostForm(forms.ModelForm):

    class Meta:
        model=Lost_Product
        fields=('title','description','lostlocation','contact','active','slug',)

class ProductForm(forms.ModelForm):

    class Meta:
        model=ProductImage
        fields=('product','image','featured',)


class RegisterationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=(
                'username',
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2',
                )

    def save(self,commit=True):
        user=super(RegisterationForm,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']


        if commit:
            user.save()
        return user

class EditProfileForm(UserChangeForm):

    class Meta:
        model=User
        fields=(
                'email',
                'first_name',
                'last_name',
                )
