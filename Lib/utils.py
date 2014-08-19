import urllib2
from urlparse import urlparse
import os

class Utils(object):
    @staticmethod
    def downloadPatch(url,directory):
        try:
            urlObject = urlparse(url)
            fileName = os.path.basename(urlObject.path)
            dst = os.path.join(directory,fileName)
            fileContent = urllib2.urlopen(url).read()
            with file(dst,'wb') as f:
                f.write(fileContent)
            return dst
        except Exception as e:
            print e.message
            return None


