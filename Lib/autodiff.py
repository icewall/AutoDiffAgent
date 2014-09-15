from config import Config
import os
import subprocess
import sqlite3

class AutoDiff(object):
    """description of class"""
    def run(self,primaryIDB,secondaryIDB,binDiffFilePath):
        
        self.__setArch(primaryIDB)
        autoDiffParams = "{autoDiffPath} -f 1 -b \"{binDiffFilePath}\" -d \"{idb2}\" -a".format(
                                                                                                          autoDiffPath = Config.AUTODIFF_PATH,
                                                                                                          binDiffFilePath = binDiffFilePath,
                                                                                                          idb2 = secondaryIDB
                                                                                                          )
        if subprocess.call([self.__IDA_PATH,"-A","-S" + autoDiffParams,primaryIDB]) != 0:
            print "Could not unpack exe"
            return False
        return True

    def __setArch(self,filePath):
        path,ext = os.path.splitext(filePath)
        if ext == ".i64": #PE+ (x64)
            self.__IDA_PATH = Config.IDA_PATH.replace("idaq.exe","idaq64.exe")
        else:
            #PE (x86)
            self.__IDA_PATH = Config.IDA_PATH
    
    def getResult(self,binDiffFilePath):
        db = sqlite3.connect(binDiffFilePath)
        db.row_factory = sqlite3.Row
        sqlChangedFunctions = "SELECT count(*) FROM function WHERE similarity < 1.0"

        sqlSanitizedFunctions = """
                        SELECT count(*)
                        FROM function as f 
                        WHERE similarity < 1.0 AND f.id IN (SELECT func_id FROM sanitizer_summary)
                      """
        sqlSafeIntCount = """
                            SELECT count(*) FROM sf_summary
                          """
        sqlReMatched = """
                        SELECT count(*) FROM rematcher_summary
                       """
        row = db.execute(sqlChangedFunctions).fetchone()
        changedFunctionsCount = int(row[0])                        
        row = db.execute(sqlSanitizedFunctions).fetchone()
        sanitizedFunctionsCount = int(row[0])
        row = db.execute(sqlSafeIntCount).fetchone()
        safeIntCount = int(row[0])
        row  = db.execute(sqlReMatched).fetchone()
        reMatchedCount = int(row[0])
        db.close()
        return (changedFunctionsCount - (sanitizedFunctionsCount + safeIntCount + reMatchedCount)) 