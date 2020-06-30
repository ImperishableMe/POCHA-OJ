from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                DetailView,
                                CreateView)

from problem.models import Problem,TestCase


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