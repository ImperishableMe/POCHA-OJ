from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                DetailView,
                                CreateView)


from . import models 



class ProblemListView(ListView):
    model = models.Problem
    template_name = 'problem/problem_list.html'


class ProblemDetailView(DetailView):
    model = models.Problem
    template_name = 'problem/problem_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['statement'] = self.object.get_problem_statement_for_rendering()
        samples = self.object.testcases.filter(is_sample=True).all()

        files = [ (sample.get_input_file_for_rendering, sample.get_output_file_for_rendering) for sample in samples]
        context['samples'] = files
        return context

