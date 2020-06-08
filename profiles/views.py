from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView

from accounts.models import CustomUser

from .models import Profile
from .forms import UserForm,ProfileForm


class UserProfileDetailView(DetailView):
    """
        CustomUser is used, not the Profile class
    """
    model = CustomUser
    template_name = 'profiles/profile_detail.html'


@login_required
def profile_update_view(request,pk):
    """
        You need to deny the permission when someone is trying to edit someone else's profile
    """

    # If this is not the actual user, then raise permissionDenied
    want_to_change_user = get_object_or_404(CustomUser,pk=pk)
    if want_to_change_user.pk != request.user.pk :
        raise PermissionDenied()

    if request.method == 'POST':
        user_form = UserForm(request.POST,request.FILES, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return HttpResponseRedirect(reverse('profiles:profile_detail', kwargs={'pk': str(request.user.pk)}))
        # else:
        #     messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profiles/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

    