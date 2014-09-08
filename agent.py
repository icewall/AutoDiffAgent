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
        #safe in somehow here runned tasks and their ID's ?
        self.__tasks = []
        #commands handlers
        self.__handlers = {
                            "getTask"    : self.__getTask,
                            "diffFiles"  : self.__nop,
                            "diffStop"   : self.__nop
                         }

        #TODO: add auto modules loader
        self.__modules = {"any": CAny(),
                          "flash": CFlash(),
                          "IE": CAny()
                          }
        #additional initialization
        self.__modules["IE"].pairFinder.addSpecifiedFiles(["mshtml.dll"])
        
    """
        Dispatch routine
    """                       
    def run(self):
        Logger.log("Waiting for task....")
        while True:
            command = self.getCommand()                 
            if not self.__busy and isinstance(command,dict):
                print command     
                self.__busy = True
                #dispatch command
                self.__handlers[command["command"]](command["params"])
           
            time.sleep(1)
    
    def getCommand(self):
        try:
            data   = urllib.urlencode( {"id": self.getAgentID()} )
            result = urllib2.urlopen("%s/Command/getCommand" % Config.HOST, data).read()
            return json.loads(result)
        except Exception as e:
            return []


    """
        Handlers
    """
    def __getTask(self,params):
        task = []
        try:
            data   = urllib.urlencode( {"agent_id": self.getAgentID()} )
            result = urllib2.urlopen("%s/Task/getTask" % Config.HOST, data).read()
            task = json.loads(result)
            #depends on product type launch different module to handle this pair of patches
            module = self.__modules[task["product"]];                
            module.initialize(Config.WORK_DIR,task)                
            module.run()
        except Exception as e:
            pass

    def __nop(self,params):
        pass

    """
        Helpers
    """    
    def getAgentID(self):
        return os.getenv("COMPUTERNAME")
    
if __name__ == "__main__":
    Logger.log("Launching agent")
    agent = CAgent()
    agent.start()               