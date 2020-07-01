from django.forms import ModelForm

from problem.models import Problem,TestCase

class ProblemUpdateForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['title','statement',
            'input_specification','output_specification',
            'time_limit','memory_limit','is_public',
            'judge_solution'
        ]


class CreateTestCaseForm(ModelForm):

    class Meta:
        model = TestCase
        fields = [
            'input_file','output_file',
            'is_sample','description'
        ]
