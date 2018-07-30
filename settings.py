# coding=utf-8
###################################################################
# Developed by ozymandias-cast (https://github.com/ozymandias-cast)
# License: GPLv3
###################################################################

import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

def init():
    global to_d
    global from_d
    global playlist
    global ip
    global port
    to_d = queue.Queue()
    from_d = queue.Queue()
    playlist = queue.Queue()

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    port = "4444"
    print("Detected %s:%s" % (ip,port))
    s.close()