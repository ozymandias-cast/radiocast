# coding=utf-8
###################################################################
# Developed by ozymandias-cast (https://github.com/ozymandias-cast)
# License: GPLv3
###################################################################

import podb
import debug_output
import requests
import unicodedata
import hashlib
from threading import Thread
import settings
import time
import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue



class download(Thread):
    def __init__(self,o):
        Thread.__init__(self)
        self.o = o
        return None

    def run(self):
        while True:
            #count = 0
            while True:
                self.o.output(1,"Retrieving one elment from the queue %d" % settings.to_d.qsize(),None)
                pod = settings.to_d.get(block=True)
                self.o.output(1,"Downloading Episode %s %s - %s" % (pod.p_title.encode('utf-8'), pod.e_title.encode('utf-8'), pod.file),None)
                try:
                    r = requests.get(pod.file, allow_redirects=True, timeout=10)
                    hash_object = hashlib.sha1(pod.e_title.encode('utf-8'))
                    pod.mp3 = settings.gpath + hash_object.hexdigest() + ".mp3"
                    newFile = open(pod.mp3, "wb")
                    newFile.write(r.content)
                    newFile.close()
                except Exception as e:
                    self.o.output(1,"Failed downloading %s-%s" % (pod.p_title,pod.e_title),e)
                    pod.mp3 = None
                settings.from_d.put(pod)
                settings.to_d.task_done()
                #count = count+1
            #self.o.output(1,"%d episodes downloaded" % count,None)
            #time.sleep(10)


