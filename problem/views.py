from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery

from django.views.generic import (ListView,
                                DetailView,
                                CreateView)

from submissions.models import Submission
from core.models import States

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


class RankView(ListView):
    model = Submission
    template_name = 'problem/problem_rank.html'

    def get_queryset(self):
        
        problem_id = self.kwargs['pid']

        accepted_qs = Submission.objects.filter(verdict = States.AC, problem_id = problem_id)

        best_submission = accepted_qs.filter(submitted_by_id = OuterRef('submitted_by_id')).\
                        order_by('time_required','memory_required') \
                            [:1]

        return accepted_qs.filter(pk = Subquery(best_submission.values('pk'))). \
            order_by('time_required','memory_required')