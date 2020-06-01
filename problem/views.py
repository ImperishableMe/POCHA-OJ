from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                DetailView,
                                CreateView)


from . import models 
from . import tasks


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


class SubmitView(LoginRequiredMixin,CreateView):

    model = models.Submission
    fields = ['problem','code','language']
    template_name = 'problem/submission_form.html'

    def get_form(self):
        form = super(SubmitView,self).get_form()
        initial_base = self.get_initial() 

        if(not 'pid' in self.kwargs) :
            return form 
        
        initial_base['problem'] = get_object_or_404(models.Problem,id=self.kwargs['pid'])
        form.initial = initial_base
        #form.fields['name'].widget = forms.widgets.Textarea()
        return form

    def form_valid(self, form):

        form.instance.submitted_by = self.request.user ### setting the current user as the owner of the submission
        submission = form.save()
        tasks.submission_evaluate(submission.pk) ### dump the submission into task_queue 
        
        return redirect(submission.get_absolute_url())


class SubmissionListView(ListView):
    model = models.Submission
    template_name = 'problem/submission_list.html'

    def get_queryset(self):
        return models.Submission.objects.filter(submitted_by__username=self.request.user.username).order_by('-time')