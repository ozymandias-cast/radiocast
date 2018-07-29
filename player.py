# coding=utf-8

import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/")
sys.path.append("./")
import feedparser
import vlc
from threading import Thread
import settings
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue
class player(Thread):
    
    def episode_end(self,event):
        pod = settings.playlist.get()
        cmd = [pod.mp3]
        #cmd.append("sout=#duplicate{dst=rtp{dst=%s,port=%s}" % (self.dst,self.port))
        cmd.append("sout=#standard{access=http,mux=ogg,dst=%s:%s}" % (self.dst,self.port))
        #cmd.append("no-sout-rtp-sap")    
        #cmd.append("no-sout-standard-sap")
        #cmd.append("sout-rtp-caching=1000")
        cmd.append("sout-mux-caching=1000")
        #cmd.append("sout-rtp-name=Hola")
        #cmd.append("sout-rtp-description=Hola")
        #cmd.append("sout-rtp-proto=tcp")
        cmd.append("sout-keep")                
        Media = self.instance.media_new(*cmd)
        self.player.set_media(Media)
        self.player.get_media()
        self.o.output(1,"Playing %s-%s" % (pod.p_title, pod.e_title),None)
        self.player.play()
    
    def __init__(self,o,dst,port):
        Thread.__init__(self)
        self.dst = dst
        self.port = port
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.medialist = self.instance.media_list_new() 
        self.o = o
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.episode_end)

    def run(self):
        self.episode_end(None)
        