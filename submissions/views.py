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
        return models.Submission.objects.select_related('problem').filter(submitted_by__username=self.request.user.username).order_by('-submission_time')

    
    def get_allow_empty(self):
        """
        Should load the page even when 
        the user has no submission
        """
        return True


    def get_context_data(self,**kwargs):
        """
        Do the table joins in view to get problem testcases count
        """
        context = super().get_context_data(**kwargs)
        
        for submission in context['submission_list'] :
            problem = submission.problem
            submission.problem_title = problem.title 
            submission.problem_test_count = problem.testcases.count()
        
        return context


class SubmissionDetailView(LoginRequiredMixin,DetailView):
    """
    Detail with test case output and input
    """

    model = models.Submission
    template_name = 'submissions/submission_detail.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['code'] = self.object.get_code()

        qset = models.SubmissionHistory.objects.select_related('testcase').filter(submission_id = self.object.id).order_by('testcase_id')

        test_list = [(q.get_user_output(), q.testcase.get_output_file_for_rendering()) 
                    for q in qset]

        context['test_list'] = test_list
        return context



class StatusView(ListView):
    template_name = 'submissions/status.html'
    model = models.Submission

    def get_queryset(self):
        return models.Submission.objects.select_related('submitted_by').order_by('-submission_time')




    

