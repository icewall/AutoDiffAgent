import win32console

#TODO add somewhere free console

class Logger(object):

    """
        Available logging modes
    """
    NONE    = -1
    CONSOLE =  0
    FILE    =  1
    BOTH    =  2
    CMD     =  3

    def __init__(self):
        pass

    @classmethod
    def init(cls,type = NONE):

        cls.__handlers = {cls.NONE    : cls.__noneHandler,
                          cls.CONSOLE : cls.__consoleHandler,
                          cls.CMD     : cls.__cmdHandler,
                          cls.FILE    : cls.__fileHandler
                          }

        cls.__handler = cls.__handlers[type]
        cls.__cmdBuffer = None
        cls.__logFile = None
        pass
        
    @classmethod
    def log(cls,msg):
        msg += "\n"
        cls.__handler(msg)
        pass

    @classmethod
    def setLoggerType(cls,type):
        cls.__handler = cls.__handlers[type]
    
    @classmethod
    def setLogFile(cls,logFile):
        cls.__logFile = logFile

    """
    Handlers
    """
    @classmethod
    def __noneHandler(cls,msg):
        pass

    @classmethod
    def __consoleHandler(cls,msg):
        print msg

    @classmethod
    def __cmdHandler(cls,msg):
        if cls.__cmdBuffer == None:
            win32console.AllocConsole()
            cls.__cmdBuffer = win32console.CreateConsoleScreenBuffer()
            cls.__cmdBuffer.SetConsoleActiveScreenBuffer()
        cls.__cmdBuffer.WriteConsole(msg)
    
    @classmethod
    def __fileHandler(cls,msg):
        if cls.__logFile == None:
            cls.__logFile = "log.txt"
        with open(cls.__logFile,'a+') as f:
            f.write(msg)            