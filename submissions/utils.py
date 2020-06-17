import os
import subprocess
import itertools
from problem.models import Problem,TestCase
from core.models import States


from datetime import datetime
from django.conf import settings

from .models import Submission,SubmissionHistory

def get_today_directory():
    """
    returns the directory of today in '%Y/%m/%d' format added by MEDIA_ROOT, 
    also creates the directory if not exists 
    """
    today = datetime.now()
    today_path = today.strftime("%Y/%m/%d") ## this will create something like "2011/08/30"

    today_dir = os.path.join(settings.MEDIA_ROOT,today_path)
    if not os.path.exists(today_dir):
        os.makedirs(today_dir)
    return today_dir


def get_executable_path(submission_id):
    """
    returns the absolute path name executable should be saved (Sends it to MEDIA_ROOT obviously)
    """
    today_dir = get_today_directory()    
    tmp_dir = os.path.join(today_dir,"executables")

    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    return os.path.join(tmp_dir,str(submission_id) + ".out")


def get_output_file_path(submission_id,testcase_id):
    """
    returns absolute path for output file for a testcase
    """

    today_dir = get_today_directory()
    
    # write file will be created automatically if not present,
    # so no need to check existence
    tmp_dir = os.path.join(today_dir,str(submission_id)
        + "_" + str(testcase_id) + ".txt")
    

    return tmp_dir


def compilation_handler(submission):
    """
    Takes the submission object, compiles it according to the language
    return: tuple(compilation_status, executable_file_path)
    """

    code = submission.code
    script_args = ["python","submissions/evaluator/compileScript.py"] #,"g++","-std=c++17","backcheck/foo.cpp"]
    language_args = []
    output_path = get_executable_path(submission.id)


    if submission.language == States.CPP :
        language_args.append("g++")
        language_args.append("-std=c++17")
    
    elif submission.language == States.C :
        language_args.append("gcc")

    else :
        # may need to handle other languages, but keeping it simple for the time being
        pass

    language_args.append(submission.code.path) ### gives the absolute path from the root 
    ### create unique executables
    language_args.append("-o")
    language_args.append(output_path)
    #### Handle the rest of the languages
    p = subprocess.check_output(args = script_args+language_args,stderr=subprocess.DEVNULL,universal_newlines=True) 
    # guarantees to return a integer that is the return code of the processs
    return int(p),output_path
