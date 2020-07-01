from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                DetailView,
                                CreateView, UpdateView)

from problem.models import Problem,TestCase

from .forms import ProblemUpdateForm,CreateTestCaseForm

class ProblemCreateView(LoginRequiredMixin,CreateView):
    model = Problem
    template_name = 'newProblems/create_problem.html'
    fields = ['title','statement',
        'input_specification','output_specification',
        'time_limit','memory_limit','is_public',
        'judge_solution'
    ]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProblemUpdateView(LoginRequiredMixin,UpdateView):
    model = Problem
    form_class = ProblemUpdateForm
    template_name = 'newProblems/update_problem.html'

    
class ProbleAddTestCaseView(LoginRequiredMixin,CreateView):
    model = TestCase
    form_class = CreateTestCaseForm
    template_name = 'newProblems/create_testcase.html'


    def form_valid(self,form):
        form.instance.problem = get_object_or_404(Problem,pk= self.kwargs['pid'])
        return super().form_valid(form)