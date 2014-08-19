import os
import shutil
from Lib.unpacker import Unpacker
from config import Config
from Lib.pairFinder import PairFinder
from Lib.bindiffer import Bindiffer

class Module(object):
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
         #support classes
         self._unpacker = Unpacker()
         self.pairFinder = PairFinder()
         self._binDiffer  = Bindiffer(self._patchDir)
     
     def getPatchDir(self):
         return self._patchDir