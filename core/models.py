from django.db import models
from django.utils.translation import gettext_lazy as _


class States(models.Model):
    '''
        It contains all the states for verdicts 
        and languages
    '''
    ### languages
    C = 1
    CPP = 2
    JAVA = 3
    PYTHON = 4
    #### Verdicts 
    WA = 1
    AC = 2
    TLE = 3
    MLE = 4
    RUNNING = 5
    IN_QUEUE = 6
    RE = 7
    CE = 8    

    languages = (
        (C, _('C')),
        (CPP, _('CPP')),
        (JAVA,_('JAVA')),
        (PYTHON,_('PYTHON')),
    )
    
    VERDICT_STATES = (
        (WA, _('WRONG ANSWER')),
        (AC, _('ACCEPTED')),
        (TLE,_('TLE')),
        (MLE,_('MLE')),
        (RE,_('RUNTIME ERROR')),
        (RUNNING,_('RUNNING')),
        (IN_QUEUE,_('IN QUEUE')),
        (CE,_('COMPILATION ERROR')),
    )
    
    class Meta :
        abstract = True


    