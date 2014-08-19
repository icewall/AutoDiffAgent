import os
import re
import hashlib
from logger import Logger
Logger.init(Logger.CONSOLE)

class PairFinder(object):
    def __init__(self):
        self.__pairs = []
        self.__newFilesList = []
        self.__oldFilesList = []
        self.__specifiedFiles = []
        self.__specifiedExtensions = []
    
    def addSpecifiedFiles(self,files):
        """
            File name can be defined as regex formula.
        """
        if not isinstance(files,list):
            raise Exception("Files need to be passed as list type")
        self.__specifiedFiles += files

    def addSpecifiedExtensions(self,extensions):
        if not isinstance(extensions,list):
            raise Exception("Extensions need to be passed as list type")

    def collectFiles(self,newFiles,oldFiles):
        for root, dirs, files in os.walk(newFiles):
            for f in files:
                self.__newFilesList.append( os.path.join(root,f) )
        
        for root, dirs, files in os.walk(oldFiles):
            for f in files:
                self.__oldFilesList.append( os.path.join(root,f) )

        print "Old files:"
        print "\n".join(self.__oldFilesList)
        print ""
        print "New files:"
        print "\n".join(self.__newFilesList)
    
    def getPairs(self):
        if len(self.__pairs):
            return self.__pairs
        return self.__findPairs()

    def __compare(self,newFile,oldFile):
        """
            Returns True if file are the same and False in other way.
        """
        #TODO : add comparing by size first ????
        with file(newFile,'rb') as f:
            newHash = hashlib.sha1(f.read()).hexdigest()

        with file(oldFile,'rb') as f:
            oldHash = hashlib.sha1(f.read()).hexdigest()        

        return newHash == oldHash

    def __findPairs(self):
        """
            Generic pair finder
        """
        for oldFile in self.__oldFilesList:
            pattern = None
            if len(self.__specifiedExtensions):
                name , ext = os.path.splitext(old)
                if not ext in self.__specifiedExtensions:
                    continue

            old = os.path.split(oldFile)[1]
            if len(self.__specifiedFiles):
                for specifiedFile in self.__specifiedFiles:
                    if re.match(specifiedFile,old):
                        pattern = specifiedFile
            if pattern == None:
                continue

            for newFile in self.__newFilesList:
                new = os.path.split(newFile)[1]
                if pattern:
                    if re.match(pattern,new):
                        Logger.log("There is new pair:")
                        Logger.log("Old : %s" % old)
                        Logger.log("New : %s" % new)                        
                        self.__pairs.append({"new" : {"name": new, "path": newFile},"old":{"name": old, "path": oldFile} } )
                elif old == new:
                    if self.__compare(newFile,oldFile):
                        print "Files are the same!!!"
                    Logger.log("There is new pair:")
                    Logger.log("Old : %s" % old)
                    Logger.log("New : %s" % new)
                    self.__pairs.append( ({"name": new, "path": newFile},{"name": old, "path": oldFile} ) )
        return self.__pairs