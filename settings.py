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
    global playlist_gaming
    global playlist_various
    global playlist_movies
    global ip
    global port_gaming
    global port_movies
    global port_various
    global gpath
    global db
    global pod_xml

    to_d = queue.Queue()
    from_d = queue.Queue()
    playlist_gaming = queue.Queue()
    playlist_various = queue.Queue()
    playlist_movies = queue.Queue()

    #gpath = './podcasts/'
    gpath = '/podcasts/'
    db = gpath + 'radiocast.db'
    pod_xml = gpath + 'Downcast.opml'
    
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    
    port_gaming = "4444"
    port_movies = "4445"
    port_various = "4446"

    print("Gaming %s:%s" % (ip,port_gaming))
    print("Movies %s:%s" % (ip,port_movies))
    print("Various %s:%s" % (ip,port_various))

    s.close()