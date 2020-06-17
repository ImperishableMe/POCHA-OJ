from django.shortcuts import render,redirect,get_object_or_404, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                DetailView,
                                CreateView)

from problem.models import Problem

from . import models 
from . import tasks


class SubmitView(LoginRequiredMixin,CreateView):

    model = models.Submission
    fields = ['problem','code','language']
    template_name = 'submissions/submission_form.html'

    def get_form(self):
        form = super(SubmitView,self).get_form()
        initial_base = self.get_initial() 
        initial_base['problem'] = get_object_or_404(Problem,id=self.kwargs['pid'])

        if not initial_base['problem'].is_submitable :
            raise Http404

        form.initial = initial_base
        #form.fields['name'].widget = forms.widgets.Textarea()
        return form

    def form_valid(self, form):

        form.instance.submitted_by = self.request.user ### setting the current user as the owner of the submission
        submission = form.save()
        tasks.submission_evaluate(submission.pk) ### dump the submission into task_queue 
        
        return redirect(submission.get_absolute_url())


class SubmissionListView(LoginRequiredMixin,ListView):
    model = models.Submission
    template_name = 'submissions/submission_list.html'

    def get_queryset(self):
        return models.Submission.objects.filter(submitted_by__username=self.request.user.username).order_by('-submission_time')



    

