from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Problem(models.Model):
    '''
        Attributes:
        title = problem title
        statement = for the time being using textField
        time_limit = 0 <= time_limit <= 5.0 
        memery_limit = in MB ( max value 1024MB )

    '''
    title = models.CharField(blank = False, null = False, max_length=25)
    statement = models.TextField()
    time_limit = models.FloatField(default = 3.0, validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
    memory_limit = models.PositiveSmallIntegerField(default = 256, validators = [MaxValueValidator(1024)] )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='created_problems')
    is_public = models.BooleanField(default=False)
    adding_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + "-" + self.title
    

    
class TestCase(models.Model):
    '''
        is_sample = True : sample testcase
                    False : not
        
    '''
    problem = models.ForeignKey(Problem, related_name = 'testcases',on_delete = models.CASCADE)
    case_input = models.TextField(blank=False,null = False)
    expected_output = models.TextField(blank=False,null=False)
    is_sample = models.BooleanField(default=False)

    def __str__(self):
        return str(self.problem.pk) + '-' + str(self.pk) 


class Submission(models.Model):
    C = 1
    CPP = 2
    JAVA = 3
    PYTHON = 4
    ####
    WA = 1
    AC = 2
    TLE = 3
    MLE = 4
    RUNNING = 5
    IN_QUEUE = 6
    RE = 7
    CE = 8

    languages = (
        (C, _('C')),
        (CPP, _('CPP')),
        (JAVA,_('JAVA')),
        (PYTHON,_('PYTHON')),
    )
    VERDICT_STATES = (
        (WA, _('WRONG ANSWER')),
        (AC, _('ACCEPTED')),
        (TLE,_('TLE')),
        (MLE,_('MLE')),
        (RE,_('RUNTIME ERROR')),
        (RUNNING,_('RUNNING')),
        (IN_QUEUE,_('IN QUEUE')),
        (CE,_('COMPILATION ERROR')),
    )

    problem = models.ForeignKey(Problem,related_name='submissions',on_delete=models.CASCADE)   
    time = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    time_required = models.FloatField(blank=True,null=True)
    memory_required = models.IntegerField(blank=True,null=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='my_submissions')

    language = models.SmallIntegerField(
        default = CPP,
        choices = languages
    )

    verdict = models.SmallIntegerField(
        default = IN_QUEUE,
        choices = VERDICT_STATES    
    )
    on_test_case = models.SmallIntegerField(default=0)     
        

    def __str__(self):
        return "SID:{},LAN:{},time:{}".format(self.pk,self.language,self.time)

    def get_absolute_url(self):
        return reverse('problem:submission_list')


#class SubmissionHistory