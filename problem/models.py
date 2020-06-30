from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from ckeditor.fields import RichTextField





class Problem(models.Model):
    '''
        title : problem title
        statement : FileField
        time_limit : 0 <= time_limit <= 5.0 ( default 3.0)
        memery_limit: in MB ( max value 1024MB ,default : 256MB)
        author : problem author
        is_public : boolean to trace the problems visibility
        judge_solution : FileField containing the intended soln(assumed to have no errors)
        creation_time : duh !
    '''

    title = models.CharField(blank = False, max_length=25)
    statement = RichTextField(blank=False)
    input_specification = RichTextField(blank=False)
    output_specification = RichTextField(blank=False)
    time_limit = models.FloatField(default = 3.0, validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])
    memory_limit = models.PositiveSmallIntegerField(default = 256, validators = [MaxValueValidator(1024)] )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='created_problems')
    is_public = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    judge_solution = models.FileField(upload_to='judge_soln/%Y/%m/%d',blank=True)

    
    def is_submitable(self):
        """
        If users can submit to this problem, the problem may not be public yet
        """
        return self.is_public

    def get_absolute_url(self):
        return reverse('problem:problem_detail', kwargs = {'pk' : self.pk});

    def __str__(self):
        return str(self.pk) + "-" + self.title


def get_testcase_path(instance,filename):
    ''' 
        gives path to store the testcase. 
        For the time being problem_id/filename is used
    '''
    return 'testcases/{0}/{1}'.format(instance.problem.id,filename)

    
class TestCase(models.Model):
    '''
        is_sample : Sample visibility 
        input_file : input as a file 
        problem : the owner problem
        output_file : expected output
    '''
    problem = models.ForeignKey(Problem, related_name = 'testcases',on_delete = models.CASCADE)
    input_file = models.FileField(upload_to=get_testcase_path, blank=True)
    output_file = models.FileField(upload_to=get_testcase_path,blank=True)
    is_sample = models.BooleanField(default=False)
    description = models.TextField(blank=True)


    def get_input_file_for_rendering(self):
        
        lines = None
        with self.input_file.open('r') as f :
            lines = f.read()
        return lines
    
    def get_output_file_for_rendering(self):

        lines = None
        with self.output_file.open('r') as f :
            lines = f.read()
        return lines

    def __str__(self):
        return str(self.problem.pk) + '-' + str(self.pk) 

