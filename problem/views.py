from django.shortcuts import render
from . import models 
from django.views.generic import (ListView,DetailView)
# Create your views here.

class ProblemListView(ListView):
    model = models.Problem
    template_name = 'problem/problem_list.html'


class ProblemDetailView(DetailView):
    model = models.Problem
    template_name = 'problem/problem_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample_test_cases'] = self.object.testcases.filter(is_sample=True).all()
        
        return context
