from django import forms
from django.forms import Textarea, ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Comments, CustomUser, Arcticle, Profile
from django.contrib.auth.models import User


class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign up'))


class ArcticleForm(forms.ModelForm):
    class Meta:
        model = Arcticle
        fields = ('name', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def __init__(self, *args, **kwargs): # nfhb jfhbdfb dj
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget= Textarea(attrs={'rows':3})
        

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput)
    first_name=forms.CharField(max_length=40)
    last_name=forms.CharField(max_length=40)
    
    class Meta:
        model = User
        fields=['username', 'first_name', 'last_name',  'email']



class ProfileForm(ModelForm):
    
    class Meta:
        model = Profile
        fields=['bio', 'profile_pic', 'city','facebook', 'twitter', 'instagram']