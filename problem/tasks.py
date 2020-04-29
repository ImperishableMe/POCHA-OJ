from background_task import background
from .models import Submission,Problem,TestCase
import subprocess,resource



@background(schedule=0)
def submission_evaluate(submission_id):
    # lookup user by id and send them a message
    submission = Submission.objects.get(pk=submission_id)
    problem = submission.problem
    code = submission.code

    compilation_code = compilation_handler(submission_id)

    print("Compiled with {}".format(compilation_code))
    
    execution_handler(submission_id)
    

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
    p = subprocess.check_output(args = script_args+language_args,universal_newlines=True) 
    # guarantees to return a integer that is the return code of the processs
    return int(p)


def execution_handler(s_id):
    submission = Submission.objects.get(pk=s_id)
    testcases = submission.problem.testcases.all()
    script_args = ["python","problem/runner.py"]
    language_args = []
    fileIO_args = []
    for test_num,cur_test in enumerate(testcases):
        # update the submission database as running on testcase i 

        input_txt = cur_test.case_input
        with open('problem/input.txt','w') as fw :
            fw.write(input_txt)

        if submission.language == Submission.CPP :
            language_args.append("./a.out")
        #### handle other language

        fileIO_args.append('problem/input.txt')
        fileIO_args.append('problem/output.txt')

        time,memory = each_case_handler(script_args+language_args+fileIO_args)
        print("test_num {} time lagse: {}sec \n memory lagse: {}KB".format(test_num,time,memory))    

def each_case_handler(cmd_args_to_run):
    p = subprocess.check_output(cmd_args_to_run,universal_newlines=True)
    st = p.split('\n')

    return float(st[1]),int(st[2])