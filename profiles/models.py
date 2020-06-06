from django.db import models
from django.conf import settings



def get_profile_pic_path(instance, filename):
    return 'images/user_{0}/{1}'.format(instance.user.username, filename)


class Profile(models.Model):
    """
        will have user informations(profile_pic, stats and so on)
        but will use the default authentication method defined by the AUTH_USER_MODEL

        ### Need to handle if the uploaded file is actually an image
            
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = 'profile')
        
    profile_pic = models.ImageField(
        upload_to = get_profile_pic_path,
        blank = True)



    def __str__(self):
        return self.user.username

