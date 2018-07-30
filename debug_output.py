# coding=utf-8

import datetime
import sys

class debug:

    def __init__(self,tofile,filename):
        if tofile == True:
            try:
                self.f = open(self.filename, 'a')
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
            if self.tofile == True:
                self.f.write(de)
            else: 
                print(de.encode('utf-8'))
            if level == 0: sys.exit()
    
        
