from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

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

