import os
import shutil
from Lib.unpacker import Unpacker
from config import Config
from Lib.pairFinder import PairFinder
from Lib.bindiffer import Bindiffer
import urllib
import urllib2
import json

class Module(object):
    def __init__(self):
        #support classes
        self._unpacker = Unpacker()
        self.pairFinder = PairFinder()

    def initialize(self,workDir,task):
         self._workDir = workDir
         self._task    = task
         #create necessary paths
         self._patchDir = os.path.join(workDir,task["name"])
         self._downloadDir = os.path.join(self._patchDir,"download")
         self._newDir = os.path.join(self._patchDir,"new")
         self._oldDir = os.path.join(self._patchDir,"old")
         #create dirs
         shutil.rmtree(self._patchDir,ignore_errors = True)
         os.mkdir(self._patchDir)
         os.mkdir(self._downloadDir)
         os.mkdir(self._newDir)
         os.mkdir(self._oldDir)
         self._binDiffer  = Bindiffer(self._patchDir)
     
    def getPatchDir(self):
         return self._patchDir
    
    def _sendFileList(self,files):
        try:
            #just add task_name == task_id  to files
            postData = {}
            postData["task_name"] = self._task["name"];
            postData["files"] = json.dumps(files)
            postData = urllib.urlencode( postData ) 
            urllib2.urlopen("%s/Storage/saveFilesList" % Config.HOST, postData)
        except Exception as e:    
            print e.message