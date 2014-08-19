from threading import Thread
import time
import urllib2
import urllib
import os
import json
from config import *
from logger import *
Logger.init(Logger.CONSOLE)

from Modules.any import *
from Modules.flash import *

class CAgent(Thread):             
    def __init__(self):
        Thread.__init__(self)
        self.__busy = False
        #TODO: add auto modules loader
        self.__modules = {"any": CAny(),
                          "flash": CFlash(),
                          "IE": CAny()
                          }
        #additional initialization
        self.__modules["IE"].pairFinder.addSpecifiedFiles(["mshtml.dll"])
        
                       
    def run(self):
        Logger.log("Waiting for task....")
        while True:
            task = self.getTask()
            Logger.log(repr(task))
            
            if not self.__busy and isinstance(task,dict):
                self.__busy = True
                #depends on product type launch different module to handle this pair of patches
                module = self.__modules[task["product"]];                
                module.initialize(Config.WORK_DIR,task)                
                module.run()
            
            time.sleep(1)
    
    def getTask(self):
        try:
            data   = urllib.urlencode( {"id": self.getAgentID()} )
            result = urllib2.urlopen("%s/Task/getTask" % Config.HOST, data).read()
            return json.loads(result)
        except Exception as e:
            return []
    
    def getAgentID(self):
        return os.getenv("COMPUTERNAME")
    
if __name__ == "__main__":
    Logger.log("Launching agent")
    agent = CAgent()
    agent.start()               