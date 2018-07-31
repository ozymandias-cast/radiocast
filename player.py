# coding=utf-8
###################################################################
# Developed by ozymandias-cast (https://github.com/ozymandias-cast)
# License: GPLv3
###################################################################

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

    def event_callback(self,event):
        self.o.output(1,"VLC ERROR: %s" % str(event),None)
        self.episode_end(None)

    def episode_end(self,event):
        try: 
            if (self.category == 'gaming'): pod = settings.playlist_gaming.get()
            if (self.category == 'various'): pod = settings.playlist_various.get()
            if (self.category == 'movies'): pod = settings.playlist_movies.get()  
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
            self.current = pod
            self.player.play()
        except Exception as e:
            self.o.output(0,"VLC ERROR: Cannot play %s-%s %s" % (pod.p_title,pod.e_title,pod.mp3,),e)
            pod.type = settings.NOTPLAYED
            settings.from_d.put(pod)
            self.episode_end()

    
    def __init__(self,o,dst,port,category):
        Thread.__init__(self)
        self.dst = dst
        self.port = port
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.medialist = self.instance.media_list_new() 
        self.o = o
        self.event_manager = self.player.event_manager()
        self.category = category
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.episode_end)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.event_callback)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerNothingSpecial, self.event_callback)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerUncorked, self.event_callback)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerCorked, self.event_callback)
        self.event_manager.event_attach(vlc.EventType.VlmMediaInstanceStatusError , self.event_callback)


        self.current = None

    def run(self):
        self.episode_end(None)
    
    def is_playing(self):
        if not self.current == None:
            self.o.output(1,"Player %s is playing:" % self.port,None)
            self.current.print_podcast(self.o)
            return self.player.is_playing()
        else:
            self.o.output(1,"Player not playing",None)
