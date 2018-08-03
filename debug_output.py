# coding=utf-8
###################################################################
# Developed by ozymandias-cast (https://github.com/ozymandias-cast)
# License: GPLv3
###################################################################
 

import datetime
import sys
import os
import signal

class debug:

    def __init__(self,tofile,filename):
        self.tofile = tofile
        self.filename = filename
        if tofile == True:
            try:
                self.tofile = True
            except Exception as e:
                print("Warning: Cannot open file %s (%s)" % (filename,e))
                print("Switching to stdout output")
                self.tofile = False
                pass
        else: self.tofile = False
        return None
    
    def output(self,level,description,err):
        if level>1: return False
        else:
            now = datetime.datetime.now()
            str_t = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
            if level == 0:
                str_t2 = str_t + ':' + 'ERROR:'
            else:
                str_t2 = str_t + ':' + 'DEBUG:' + str(level)
            if err == None: de = str_t2 + '-' + description
            else: de = str_t2 + '-' + description + '-' + str(err)
            de = de + '\n'
            if self.tofile == True:
                try:
                    self.f = open(self.filename, 'a+')
                    self.f.write(de)
                    self.f.close()
                except Exception as e:
                    print("Cannot write to file %s" % str(e))
                    sys.stdout.flush()
                    sys.stderr.flush()

            else: 
                print(de.encode('utf-8'))
            if level == 0: 
                os.kill(os.getpid(), signal.SIGUSR1)

    
        
