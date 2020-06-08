from django.forms import ModelForm

from accounts.models import CustomUser

from .models import Profile


class UserForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name',
            'email')        


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('profile_pic',)
