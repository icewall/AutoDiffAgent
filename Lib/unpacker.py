import zipfile
import subprocess
import os
from config import Config

class Unpacker(object):
    
    def __init__(self):
        self.__handlers = {".msi":self.__msiHandler,
                           ".msu":self.__msuHandler,
                           ".zip":self.__zipHandler,
                           ".msp":self.__mspHandler,
                           ".exe":self.__exeHandler
                           }

    def unpack(self,filePath,extractDir):
        name,ext = os.path.splitext(filePath)
        self.__handlers[ext](filePath,extractDir)

    def __msiHandler(self,filePath,targetDir):
        """
        Usage: MsiX.exe <file> [/out <output>] [/ext]

        file - Path to an MSI, MSM, MSP, or PCP file.
        out  - Extract streams and storages to the <output> directory.
        ext  - Append appropriate extensions to output files.
        """
        msiXPath = os.path.join(Config.AGENT_LOCATION,"bin","MsiX.exe")
        if subprocess.call([msiXPath, filePath, "/out",targetDir]) != 0:
                    print "Could not unpack msu"
                    return False

    def __msuHandler(self,filePath,targetDir):
        '''
        expand -F:* update.msu C:<targetDir>
        cd <targetDir>
        expand -F:* update.cab C:<targetDir>
        '''

        print "Expanding", filePath, "to", targetDir

        if subprocess.call(['expand', '-F:*', filePath, targetDir]) != 0:
            print "Could not unpack msu"
            return False

        os.chdir(targetDir)

        garbage, cabname = os.path.split(filePath)
        cabname, ext = os.path.splitext(cabname)
        cabname = cabname + '.cab'
        os.path.join(targetDir, cabname)

        print "Expanding", cabname, "to", targetDir

        if subprocess.call(['expand', '-F:*', cabname, targetDir]) != 0:
            print "Could not unpack cab"
            return False

        return True
        
    def __zipHandler(self,filePath,extractDir):
        with zipfile.ZipFile(filePath) as zf:
            zf.extractall(extractDir)

    def __mspHandler(self,filePath,extractDir):
        """
        Usage: MsiX.exe <file> [/out <output>] [/ext]

        file - Path to an MSI, MSM, MSP, or PCP file.
        out  - Extract streams and storages to the <output> directory.
        ext  - Append appropriate extensions to output files.
        """
        msiXPath = os.path.join(Config.AGENT_LOCATION,"bin","MsiX.exe")
        if subprocess.call([msiXPath, filePath, "/out",targetDir]) != 0:
                    print "Could not unpack msu"
                    return False
        
        #some cab can be there o_0

        return True

    def __exeHandler(self,filePath,extractDir):
        if subprocess.call([filePath, "/quiet", "/extract:", targetDir]) != 0:
            print "Could not unpack cab"
            return False
        return True
