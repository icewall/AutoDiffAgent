import subprocess
import os
from config import Config
import sqlite3
import win32file
import pefile 

class Bindiffer(object):

    def __init__(self,patchDir):
        self.__newIDBPath = None
        self.__oldIDBPath = None
        self.__patchDir = patchDir
        self.__IDA_PATH = "" #depends on file arch it gonna change
        self.__BINDIFF_PLUGIN = ""
        self.__IDBEXT = ""        
        self.__archFlag = False
        self.__initPaths()        

    def createIDB(self,filePath):
        self.__setArch(filePath)
        subprocess.check_output([self.__IDA_PATH, '-B', '-A', filePath])
        #replace extension
        path, ext = os.path.splitext(filePath)
        return path + self.__IDBEXT

    def runBinDiff(self,newIDB,oldIDB):
        #create .binDiff file name        
        self.__initBinDiffFile(newIDB,oldIDB)
        self.__makeBinDiffScript()
        self.__makeBinDiffAu3(oldIDB)
        subprocess.call([self.__IDA_PATH, '-S"%s"' % (self.__scriptBinDiffPath), newIDB])
    
    def getResult(self):
        db = sqlite3.connect(self.__binDiffFilePath)
        db.row_factory = sqlite3.Row
        result = db.execute("select count(*) as amount from function where similarity < 1.0 order by similarity").fetchall()
        db.close()
        result = result[0]
        return result["amount"]

    """
        Helpers
    """

    def __initPaths(self):
        #IDAScripts
        self.__idaScriptsPath = os.path.join(Config.AGENT_LOCATION,"IDAScripts")
        self.__templateBinDiffPath = os.path.join(self.__idaScriptsPath,"run_binDiff.template")
        self.__scriptBinDiffPath = os.path.join(self.__idaScriptsPath,"run_binDiff.py")
        #Au3 - AutoIt
        self.__au3Path = os.path.join(Config.AGENT_LOCATION,"Au3")
        self.__au3BinDiffTemplate = os.path.join(self.__au3Path,"bindiffer_template.au3")
        self.__au3BinDiffPath = os.path.join(self.__au3Path,"bindiffer.au3")


    def __initBinDiffFile(self,newIDB,oldIDB):
        path, file = os.path.split(newIDB)
        newName, ext = os.path.splitext(file)
        path, file = os.path.split(oldIDB)
        oldName, ext = os.path.splitext(file)
        self.__binDiffFileName = "%s_vs_%s.BinDiff" % (newName,oldName)
        self.__binDiffFilePath = os.path.join(self.__patchDir,self.__binDiffFileName)        
    
    def __makeBinDiffScript(self):        
        with file(self.__templateBinDiffPath,'r') as f:
            template = f.read()

        with file(self.__scriptBinDiffPath,'w') as f:
            template = template.replace("***AUTOIT_PATH***",Config.AUTOIT_PATH)
            template = template.replace("***AUTOIT_SCRIPT***",self.__au3BinDiffPath)
            template = template.replace("***BINDIFF_PLUGIN***",self.__BINDIFF_PLUGIN)
            f.write(template)
    
    def __makeBinDiffAu3(self,oldIDB):
        with file(self.__au3BinDiffTemplate,'r') as f:
            template = f.read()

        with file(self.__au3BinDiffPath,'w') as f:
            template = template.replace("***OLD_IDB***",oldIDB)
            template = template.replace("***BD_DB***",self.__binDiffFilePath)
            template = template.replace("***EXIT_SCRIPT***",os.path.join(self.__idaScriptsPath,"exit.py"))
            f.write(template)

    def __setArch(self,filePath):
        if not self.__archFlag:
            self.__archFlag = True
        else:
            return

        pe = pefile.PE(filePath,fast_load = True)
        if pe.OPTIONAL_HEADER.Magic == 0x20b: #PE+ (x64)
            self.__IDA_PATH = Config.IDA_PATH.replace("idaq.exe","idaq64.exe")
            self.__BINDIFF_PLUGIN = Config.BINDIFF_PLUGIN.replace("zynamics_bindiff_4_0.plw","zynamics_bindiff_4_0.p64")
            self.__IDBEXT = ".i64"
        else:
            #PE (x86)
            self.__IDA_PATH = Config.IDA_PATH
            self.__BINDIFF_PLUGIN = Config.BINDIFF_PLUGIN
            self.__IDBEXT = ".idb"

       


                