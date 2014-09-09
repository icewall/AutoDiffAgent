from threading import Thread
import time
import urllib2
import urllib
import os
import json
from config import *
from logger import *
Logger.init(Logger.CONSOLE)

from Lib.unpacker import Unpacker
from Lib.pairFinder import PairFinder
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
                            "diffStop"   : self.__nop,
                            "unpack"     : self.__unpack
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
                #self.__busy = True
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
            data   = urllib.urlencode( {"agent_id": self.getAgentID(),
                                        "task_name" : params
                                        } )
            result = urllib2.urlopen("%s/Task/getTaskByName" % Config.HOST, data).read()
            task = json.loads(result)
            #depends on product type launch different module to handle this pair of patches
            module = self.__modules[task["product"]];                
            module.initialize(Config.WORK_DIR,task)                
            module.run()
        except Exception as e:
            print e.message

    def __unpack(self,params):
        try:
            params = json.loads(params)
            #get file objects
            if params.has_key("newID"):
                #action for new files package
                data   = urllib.urlencode( {"id": params["newID"],
                                        "task_name" : params["task_name"]
                                        } )
                result = urllib2.urlopen("%s/Storage/getFileByIdAPI" % Config.HOST, data).read()
                newFile = json.loads(result)
                #time for unpacking
                unpacker = Unpacker()
                dir = os.path.split(newFile["filePath"])[0]
                unpacker.unpack(newFile["filePath"],dir,params["type"])

            if params.has_key("oldID"):
                #action for new files package
                data   = urllib.urlencode( {"id": params["oldID"],
                                        "task_name" : params["task_name"]
                                        } )
                result = urllib2.urlopen("%s/Storage/getFileByIdAPI" % Config.HOST, data).read()
                oldFile = json.loads(result)
                #time for unpacking
                unpacker = Unpacker()
                dir = os.path.split(oldFile["filePath"])[0]
                unpacker.unpack(oldFile["filePath"],dir,params["type"])

            #let's re-scan files dir and save them again
            pairFinder = PairFinder()       
            newDir = self.getFilesDir(params["task_name"],"new")
            oldDir = self.getFilesDir(params["task_name"],"old")     
            pairFinder.collectFiles(newDir,oldDir)
            self.sendFileList(params["task_name"],pairFinder.getFiles())
                
        except Exception as e:
            print e.message

    def __nop(self,params):
        pass

    """
        Helpers
    """    
    def getAgentID(self):
        return os.getenv("COMPUTERNAME")
    
    def getTaskDir(self,task_name):
        return os.path.join(Config.WORK_DIR,task_name)

    def getFilesDir(self,task_name,name):
        return os.path.join(self.getTaskDir(task_name),name)

    def sendFileList(self,task_name,files):
        try:
            #just add task_name == task_id  to files
            print "sendFile"
            postData = {}
            postData["task_name"] = task_name
            postData["files"] = json.dumps(files)
            postData = urllib.urlencode( postData ) 
            urllib2.urlopen("%s/Storage/saveFilesList" % Config.HOST, postData)
        except Exception as e:    
            print e.message
    
if __name__ == "__main__":
    Logger.log("Launching agent")
    agent = CAgent()
    agent.start()               