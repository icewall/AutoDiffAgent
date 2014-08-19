from threading import Thread
from module import Module
from Lib.utils import Utils
from logger import Logger
import os
import win32api

Logger.init(Logger.CONSOLE)

class CFlash(Thread,Module):

    def run(self):
        print "Running Flash module"
        downloadNew = Utils.downloadPatch(self._task["url_new"],self._downloadDir)
        downloadOld = Utils.downloadPatch(self._task["url_old"],self._downloadDir)
        self._unpacker.unpack(downloadNew,self._newDir)
        self._unpacker.unpack(downloadOld,self._oldDir)
        newFlashInstaller = getFlashInstaller(self._newDir)
        oldFlashInstaller = getFlashInstaller(self._oldDir)
        Logger.log("Time to uninstall existing flash...")
        #uninstall first whatever is installed there
        Logger.log(oldFlashInstaller)
        subprocess.check_output([oldFlashInstaller,"-uninstall"])
        Logger.log("Install old version...")
        #install old version
        subprocess.check_output([oldFlashInstaller,"-install"])
        #collect files
        newFlashPath = os.path.join(DOWNLOAD_PATH,"new_flash")
        oldFlashPath = os.path.join(DOWNLOAD_PATH,"old_flash")
        Logger.log("Copy files..")
        try:
            shutil.rmtree(oldFlashPath, ignore_errors = True)
        except Exception as e:
            print e.message
        shutil.copytree(getFlashDirectory(),oldFlashPath)
        subprocess.check_output([oldFlashInstaller,"-uninstall"])
        #install new version
        subprocess.check_output([newFlashInstaller,"-install"])
        try:
            shutil.rmtree(newFlashPath, ignore_errors = True)
        except Exception as e:
            print e.message
        shutil.copytree(getFlashDirectory(),newFlashPath)
        self.pairFinder.addSpecifiedFiles(["^NPSWF32_"])
        self.pairFinder.collectFiles(self._newDir,self._oldDir)
        pairs = self.pairFinder.getPairs()
        for pair in pairs:
            newIDB = self._binDiffer.createIDB(pair["new"]["path"])
            oldIDB = self._binDiffer.createIDB(pair["old"]["path"])
            #run BinDiff
            self._binDiffer.runBinDiff(newIDB,oldIDB)


    def is64Bits():
        #under windows
        return os.environ.has_key("ProgramFiles(x86)")

    def getFlashDirectory():
        #create flash path
        flashPath = win32api.GetWindowsDirectory()
        system32 = "SysWOW64" if is64Bits() else "system32"
        flashPath = os.path.join(flashPath,system32,"Macromed\\Flash")
        Logger.log(flashPath)
        return flashPath

    def getFlashInstaller(installerDir):
        installerDir = os.path.join(installerDir,"*","*.exe")
        files = glob.glob(installerDir)
        for f in files:
            if f.find("_debug") == -1 and f.find("_winax") == - 1 and f.find("uninstall_") == -1:
                return f
