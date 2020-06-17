import subprocess
import os
import itertools

from background_task import background
from django.conf import settings
from django.core.files import File

from problem.models import Problem,TestCase
from core.models import States

from .utils import (get_today_directory,get_executable_path,
                get_output_file_path, compilation_handler)

from .models import Submission,SubmissionHistory

@background(schedule=0)
def submission_evaluate(submission_id):
    # lookup user by id and send them a message
    submission = Submission.objects.get(pk=submission_id)
    problem = submission.problem
    code = submission.code

    compilation_code, executable = compilation_handler(submission)

    print(compilation_code)
    ### 0 if succesfully compiled
    if not compilation_code:
        #exc_1()
        execution_handler(submission,executable_name= executable)
    else :
        submission.verdict = States.CE
        submission.save()

    print("compilation shesh!")


def execution_handler(submission, executable_name = None):
    
    testcases = submission.problem.testcases.all().order_by('id')
    submitted_problem = submission.problem


    max_time, max_memory = 0,0

    for test_num,cur_test in enumerate(testcases):
        # update the submission database as running on testcase i 

        submission.on_test_case = test_num + 1
        submission.verdict = States.RUNNING
        submission.save()
        # set up submission History entry for this testcase run
        submission_history = SubmissionHistory()
        submission_history.submission = submission
        submission_history.testcase = cur_test

        # execute for this case and get the attributes
        return_code,time,memory = each_case_processor(submission,
            cur_test,submission_history, executable_name)

        is_more_itr_needed = 0
        max_time = max(max_time,time)
        max_memory = max(max_memory,memory)
        
        # update verdict on the submission_history tables
        update_verdict(submission_history,return_code,time,memory, submitted_problem)

        
        
        if submission_history.verdict != States.AC :
            # Did not pass this test case, so 
            # no need to go furthur

            submission.verdict = submission_history.verdict 
            submission.time_required = max_time
            submission.memory_required = max_memory
            submission.save()
            return ### evalutation complete 
        
    
    
    # code passed all the cases 
    # otherwise it would have been caught earlier
    
    submission.verdict = States.AC
    submission.time_required = max_time
    submission.memory_required = max_memory
    submission.save()
    return 


def update_verdict(submission_history,return_code,time,memory, submitted_problem):
    #  If we have non-zero return-code, the code fails on this case
    
    
    if return_code :
        ### non-zero return code means time_limit_exceeded , memory_limit_exceeded, runtime_error
        if memory > submitted_problem.memory_limit*1024 :
            submission_history.verdict = States.MLE

        elif time > submitted_problem.time_limit*1000:
            submission_history.verdict = States.TLE

        else :
            submission_history.verdict = States.RE
        
        ### saves the verdict
    else :
        
        # return code 0, means code ran smoothly within the fixed time_limit and 
        # memory limit (limit is set more than actual TL and ML ), so we again 
        # need to check the limit 
        
        if memory > submitted_problem.memory_limit*1024 :
            submission_history.verdict = States.MLE

        elif time > submitted_problem.time_limit*1000 :
            submission_history.verdict = States.TLE
            
        else :
            is_wa = wrong_answer_checker(submission_history)
            
            if is_wa :
                submission_history.verdict = States.WA
            else :
                submission_history.verdict = States.AC
    
    submission_history.save()


def each_case_processor(submission,cur_test,submission_history,executable_name):

    script_args = ["python","submissions/evaluator/runner.py"]
    language_args = []
    fileIO_args = []
    input_file = cur_test.input_file

    if submission.language == States.CPP or submission.language == States.C :
        language_args = [executable_name]
    #### handle other language

    fileIO_args= [input_file.path]
    output_file_path = get_output_file_path(submission.id,cur_test.id)
    fileIO_args.append(output_file_path)

    return_code,time,memory = execution_script_runner(script_args+language_args+fileIO_args)

    with open(output_file_path) as f :
        myfile = File(f)
        relative_path = os.path.relpath(output_file_path,settings.MEDIA_ROOT)

        print("relative_path: {} , output_path: {}".format(relative_path, output_file_path))

        submission_history.user_output.save(relative_path,myfile)

    return (return_code,time,memory)
    
    
def execution_script_runner(cmd_args_to_run):
    p = subprocess.check_output(cmd_args_to_run,stderr=subprocess.DEVNULL,universal_newlines=True)
    st = p.split('\n')
    return int(st[0]),float(st[1]),int(st[2])


def wrong_answer_checker(submission_history):
    
    #get the testcase
    cur_test = submission_history.testcase
    file1 = cur_test.output_file.path
    file2 = submission_history.user_output.path

    try:
        ## '--strip-trailing-cr' to ignore the carriage return at the end 

        cmd = ["diff",'--strip-trailing-cr',file1,file2]

        __ = subprocess.check_output(cmd,stderr=subprocess.DEVNULL)
        return 0 ## accepted
    except subprocess.CalledProcessError :
        return 1 ## WA


    