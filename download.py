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
import threading
import settings
import time
import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue



class download(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = threading.Event()
        return None

    def run(self):
        while True:
            #count = 0
            while True:
                if self.stop.is_set(): 
                    settings.o.output(1,"Quitting download thread",None)
                    return True
                pod = settings.to_d.get(block=True)
                settings.o.output(1,"Download queue: %d - Downloading Episode %s %s - %s" % (settings.to_d.qsize(),pod.p_title.encode('utf-8'), pod.e_title.encode('utf-8'), pod.file),None)
                try:
                    r = requests.get(pod.file, allow_redirects=True, timeout=10)
                    hash_object = hashlib.sha1(pod.e_title.encode('utf-8'))
                    pod.mp3 = settings.gpath + hash_object.hexdigest() + ".mp3"
                    newFile = open(pod.mp3, "wb")
                    newFile.write(r.content)
                    newFile.close()
                    pod.type = settings.DOWNLOADED
                except Exception as e:
                    settings.o.output(1,"Failed downloading %s-%s" % (pod.p_title,pod.e_title),e)
                    pod.type = settings.URLNOTFOUND
                settings.from_d.put(pod)
                settings.to_d.task_done()



