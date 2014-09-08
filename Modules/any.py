from threading import Thread
from module import Module
from Lib.utils import Utils
import os
from config import Config

class CAny(Thread,Module):
    def __init__(self):
        Thread.__init__(self)
        Module.__init__(self)        
    
    def run(self):     
        #download files
        if Config.DEBUG:
            downloadNew = r"d:\download\tmp\Windows6.0-KB2957689-x86.msu"
            downloadOld = r"d:\download\tmp\Windows6.0-KB2936068-x86.msu"
        else:
            downloadNew = Utils.downloadPatch(self._task["url_new"],self._downloadDir)
            downloadOld = Utils.downloadPatch(self._task["url_old"],self._downloadDir)
        #unpack them        
        self._unpacker.unpack(downloadNew,self._newDir)
        self._unpacker.unpack(downloadOld,self._oldDir)
        #find proper pairs
        #self._pairFinder.addSpecifiedExtensions([".exe",".dll"]) # better even without this cos there can be files like in MS14-028
        #self.pairFinder.addSpecifiedFiles(["mshtml.dll"])
        self.pairFinder.collectFiles(self._newDir,self._oldDir)
        self._sendFileList( self.pairFinder.getFiles() )
        if self._task["mode"] == "auto":
            pairs = self.pairFinder.getPairs()
            for pair in pairs:
                newIDB = self._binDiffer.createIDB(pair["new"]["path"])
                oldIDB = self._binDiffer.createIDB(pair["old"]["path"])
                #run BinDiff
                self._binDiffer.runBinDiff(newIDB,oldIDB)
