from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings



from problem.models import Problem,TestCase
from core.models import States



def submission_directory_path(instance,filename):
    return "submission/problem_id{0}/userid_{1}/{2}".format(instance.problem.id,instance.submitted_by.id, filename)


class Submission(models.Model):
    
    problem = models.ForeignKey(Problem,
            related_name='submissions',
            on_delete=models.CASCADE)   
            
    submission_time = models.DateTimeField(auto_now_add=True)
    code = models.FileField(upload_to=submission_directory_path)
    time_required = models.FloatField(blank=True,null=True)
    memory_required = models.IntegerField(blank=True,null=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='my_submissions')

    language = models.SmallIntegerField(
        default = States.CPP,
        choices = States.languages
    )

    verdict = models.SmallIntegerField(
        default = States.IN_QUEUE,
        choices = States.VERDICT_STATES    
    )
    
    on_test_case = models.SmallIntegerField(default=0)     
        

    def __str__(self):
        return "SID:{},Problem:{},time:{}".format(self.pk,self.problem,self.submission_time)


    def get_code(self):
        """
        Get the code as strings
        """
        lines = None
        with self.code.open('r') as f :
            lines = f.read()
        return lines


    def get_absolute_url(self):
        return reverse('submissions:submission_list')



class SubmissionHistory(models.Model):
    
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='submssion_history')
    testcase = models.ForeignKey(TestCase,on_delete=models.CASCADE,related_name='tested_upon')
    user_output = models.FileField()
    
    verdict = models.SmallIntegerField(
        default = States.IN_QUEUE,
        choices = States.VERDICT_STATES    
    )


    def get_user_output(self):

        lines = None
        with self.user_output.open('r') as f:
            lines = f.read()
        return lines
    