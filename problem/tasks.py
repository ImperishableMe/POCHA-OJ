from background_task import background
from .models import Submission,Problem,TestCase
import subprocess
import itertools


@background(schedule=0)
def submission_evaluate(submission_id):
    # lookup user by id and send them a message
    submission = Submission.objects.get(pk=submission_id)
    problem = submission.problem
    code = submission.code

    compilation_code = compilation_handler(submission_id)

    ### 0 if succesfully compiled
    if not compilation_code:
        execution_handler(submission_id)
    else :
        submission.verdict = Submission.CE
        submission.save()
    
    

def compilation_handler(s_id):
    submission = Submission.objects.get(pk=s_id)
    code = submission.code
    script_args = ["python","problem/compileScript.py"] #,"g++","-std=c++17","backcheck/foo.cpp"]
    language_args = []

    if submission.language == Submission.CPP :
        with open('problem/foo.cpp','w') as fc:
            fc.write(code)
        language_args.append("g++")
        language_args.append("-std=c++17")
        language_args.append("problem/foo.cpp")

    #### Handle the rest of the languages
    p = subprocess.check_output(args = script_args+language_args,stderr=subprocess.DEVNULL,universal_newlines=True) 
    # guarantees to return a integer that is the return code of the processs
    return int(p)


def execution_handler(s_id):
    submission = Submission.objects.get(pk=s_id)
    testcases = submission.problem.testcases.all().order_by('id')
    script_args = ["python","problem/runner.py"]
    language_args = []
    fileIO_args = []

    max_time, max_memory = 0,0

    for test_num,cur_test in enumerate(testcases):
        # update the submission database as running on testcase i 

        submission.on_test_case = test_num + 1
        submission.verdict = Submission.RUNNING
        submission.save()

        input_txt = cur_test.case_input

        with open('problem/input.txt','w') as fw :
            fw.write(input_txt)

        if submission.language == Submission.CPP :
            language_args = ["./a.out"]
        #### handle other language

        fileIO_args= ['problem/input.txt']
        fileIO_args.append('problem/output.txt')

        return_code,time,memory = each_case_handler(script_args+language_args+fileIO_args)
        
        is_more_itr_needed = 0

        # print("code: {}, time: {} sec , memory {} KB ".format(return_code,time,memory))
        
        ''' If we have non-zero return-code, the code fails on this case
            So we have to update the database givig the verdict and stop 
            furthur test case execution
        '''
        if return_code :
            ### non-zero return code means time_limit_exceeded , memory_limit_exceeded, runtime_error
            if memory > submission.problem.memory_limit*1024 :
                submission.verdict = Submission.MLE

            elif time > submission.problem.time_limit*1000:
                submission.verdict = Submission.TLE

            else :
                submission.verdict = Submission.RE
            
            ### saves the verdict
        else :
            '''
            return code 0, means code ran smoothly within the fixed time_limit and 
            memory limit (limit is set more than actual TL and ML ), so we again 
            need to check the limit 
            '''
            if memory > submission.problem.memory_limit*1024 :
                submission.verdict = Submission.MLE


            elif time > submission.problem.time_limit*1000 :
                submission.verdict = Submission.TLE
                
            else :
                is_wa = wrong_answer_checker(cur_test.id)
                
                if is_wa :
                    submission.verdict = Submission.WA
                else :
                    is_more_itr_needed = 1 # 0 if AC 
                

        max_time = max(max_time,time)
        max_memory = max(max_memory,memory)

        if not is_more_itr_needed :
            submission.time_required = max_time
            submission.memory_required = max_memory
            submission.save()

            return ### evalutation complete 
        
        #print("test_num {} time required: {}sec \n memory required: {}KB".format(test_num,time,memory))    

    '''
        code passed all the cases 
        otherwise it would have been caught in is_more_itr_needed check
    '''    
    submission.verdict = Submission.AC
    submission.time_required = max_time
    submission.memory_required = max_memory
    submission.save()
    return 


def each_case_handler(cmd_args_to_run):
    p = subprocess.check_output(cmd_args_to_run,stderr=subprocess.DEVNULL,universal_newlines=True)
    st = p.split('\n')

    return int(st[0]),float(st[1]),int(st[2])

def wrong_answer_checker(test_id):
    cur_test = TestCase.objects.get(id=test_id)
    
    with open('problem/expected_output.txt','w') as fout :
        fout.write(cur_test.expected_output)
        fout.write('\n') #### added new line to make it same as output

    try:
        ## '--strip-trailing-cr' to ignore the carriage return at the end 

        cmd = ["diff",'--strip-trailing-cr','problem/output.txt','problem/expected_output.txt']

        __ = subprocess.check_output(cmd,stderr=subprocess.DEVNULL)
        return 0 ## accepted
    except subprocess.CalledProcessError :
        return 1 ## WA


    