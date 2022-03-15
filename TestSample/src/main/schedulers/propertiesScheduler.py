'''
Created on 24 Oct 2021

@author: pakala
'''
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from importlib import import_module
import os.path 
import sys

try:
    from config import aasxconfig as aasxconfig
except ImportError:
    from main.config import aasxconfig as aasxconfig

data_dir = os.path.join(aasxconfig.script_dir, "data")


class Scheduler(object):
    """
    The scheduler of the Administration Shell
    """

    def __init__(self, pyAAS, msgHandler):
        self.pyAAS = pyAAS
        self.f_modules = {}

        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(20),
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }

        # initialize the scheduler
        self.scheduler = BackgroundScheduler(
            jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        self.triggers = {}

    def configure(self, aasxconfig):
        """Configures the triggers and jobs out of the given configuration

        :param lxml.etree.ElementTree configuration: XML DOM tree of
        the configuration

        """
        
        # add each trigger of the configuration to the scheduler
        propertydict = self.pyAAS.tdProperties
        for key in propertydict:
            propertyData = propertydict["key"]
            updateFunction = import_module("f_propertyUpdate").function
            params = [self.pyAAS,propertyData]
            propertyName = propertyData["propertyName"]
            updateFunction.scheduler.add_job(updateFunction, trigger=propertyData["updateFrequency"], args=params, id=propertyName, replace_existing=True)

    def start(self):
        """Runs the scheduler.

        After the scheduler has been started, we can no longer alter
        its settings.

        """
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()
