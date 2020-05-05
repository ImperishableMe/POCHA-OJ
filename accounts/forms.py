from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from . import models

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = models.CustomUser
        #fields = UserCreationForm.Meta.fields + ('age',)
        fields = ('username','first_name','last_name','email','age')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = models.CustomUser
        fields = ('username','first_name','last_name','email','age')

