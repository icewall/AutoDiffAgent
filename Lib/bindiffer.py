import subprocess
import os
from config import Config

class Bindiffer(object):

    def __init__(self,patchDir):
        self.__newIDBPath = None
        self.__oldIDBPath = None
        self.__patchDir = patchDir
        self.__initPaths()
        self.__makeBinDiffScript()

    def createIDB(self,filePath):
        subprocess.check_output([Config.IDA_PATH, '-B', '-A', filePath])
        #replace extension
        path, ext = os.path.splitext(filePath)
        return path + ".idb"

    def runBinDiff(self,newIDB,oldIDB):
        #create .binDiff file name
        self.__initBinDiffFile(newIDB,oldIDB)
        self.__makeBinDiffAu3(oldIDB)
        subprocess.call([Config.IDA_PATH, '-S"%s"' % (self.__scriptBinDiffPath), newIDB])


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
            template = template.replace("***BINDIFF_PLUGIN***",Config.BINDIFF_PLUGIN)
            f.write(template)
    
    def __makeBinDiffAu3(self,oldIDB):
        with file(self.__au3BinDiffTemplate,'r') as f:
            template = f.read()

        with file(self.__au3BinDiffPath,'w') as f:
            template = template.replace("***OLD_IDB***",oldIDB)
            template = template.replace("***BD_DB***",self.__binDiffFilePath)
            template = template.replace("***EXIT_SCRIPT***",os.path.join(self.__idaScriptsPath,"exit.py"))
            f.write(template)

                