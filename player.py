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
import time
import os
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

class player(Thread):

    def event_callback(self,event):
        settings.o.output(1,"VLC ERROR: %s" % str(event),None)
        self.episode_end(None)

    def episode_end(self,event):
        try: 
            if (self.category == 'gaming'): pod = settings.playlist_gaming.get()
            if (self.category == 'various'): pod = settings.playlist_various.get()
            if (self.category == 'movies'): pod = settings.playlist_movies.get() 
            settings.o.output(1,"Playing a new podcast:",None)
            pod.print_podcast()
            cmd = [pod.mp3]
            #cmd.append("sout=#duplicate{dst=rtp{dst=%s,port=%s}" % (self.dst,self.port))
            #cmd.append("sout=#standard{access=http,mux=ogg,dst=%s:%s}" % (self.dst,self.port))
            cmd.append("sout=#standard{access=http,mux=ts,dst=%s:%s}" % (self.dst,self.port))
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
            settings.o.output(1,"Playing %s-%s" % (pod.p_title, pod.e_title),None)
            self.current = pod
            self.player.play()
            time.sleep(2)
            self.duration = self.player.get_length() / 1000
            settings.o.output(1,"Media duration: %d" % self.duration,None)

        except Exception as e:
            settings.o.output(0,"VLC ERROR: Cannot play %s-%s %s" % (pod.p_title,pod.e_title,pod.mp3,),e)
            pod.type = settings.NOTPLAYED
            settings.from_d.put(pod)
            self.episode_end()

    
    def __init__(self,dst,port,category):
        Thread.__init__(self)
        self.dst = dst
        self.port = port
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.medialist = self.instance.media_list_new() 
        self.event_manager = self.player.event_manager()
        self.category = category
        #self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.episode_end)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.event_callback)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerNothingSpecial, self.event_callback)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerUncorked, self.event_callback)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerCorked, self.event_callback)
        self.event_manager.event_attach(vlc.EventType.VlmMediaInstanceStatusError , self.event_callback)
        self.current = None

    def run(self):
        while True: 
            try: 
                if (self.category == 'gaming'): pod = settings.playlist_gaming.get()
                if (self.category == 'various'): pod = settings.playlist_various.get()
                if (self.category == 'movies'): pod = settings.playlist_movies.get() 
                pod.print_podcast()
                cmd = [pod.mp3]
                #cmd.append("sout=#duplicate{dst=rtp{dst=%s,port=%s}" % (self.dst,self.port))
                #cmd.append("sout=#standard{access=http,mux=ogg,dst=%s:%s}" % (self.dst,self.port))
                #cmd.append("sout=#standard{access=http,mux=ts,dst=%s:%s}" % (self.dst,self.port))
                #cmd.append("no-sout-rtp-sap")    
                #cmd.append("no-sout-standard-sap")
                #cmd.append("sout-rtp-caching=1000")
                #cmd.append("sout-mux-caching=1000")
                #cmd.append("sout-rtp-name=Hola")
                #cmd.append("sout-rtp-description=Hola")
                #cmd.append("sout-rtp-proto=tcp")
                #cmd.append("sout-keep")  

                cmd.append("sout=#duplicate{dst=rtp{dst=%s,port=%s}" % (self.dst,self.port))
                cmd.append("no-sout-rtp-sap")    
                cmd.append("no-sout-standard-sap")
                cmd.append("sout-rtp-caching=1000")
                cmd.append("sout-mux-caching=1000")
                cmd.append("sout-rtp-proto=udp")

                Media = self.instance.media_new(*cmd)
                self.player.set_media(Media)
                self.player.get_media()
                settings.o.output(1,"Playing %s-%s" % (pod.p_title, pod.e_title),None)
                self.current = pod
                self.player.play()
                time.sleep(2)
                self.duration = (self.player.get_length() / 1000)-1
                settings.o.output(1,"Media duration: %d" % self.duration,None)
                time.sleep(self.duration)
            except Exception as e:
                settings.o.output(0,"VLC ERROR: Cannot play %s-%s %s" % (pod.p_title,pod.e_title,pod.mp3,),e)
                pod.type = settings.FILENOTFOUND
                settings.from_d.put(pod)
    
    def is_playing(self):
        if not self.current == None:
            settings.o.output(1,"Player %s is playing (%d): " % (self.port,self.player.is_playing()),None)
            self.current.print_podcast()
            return self.player.is_playing()
        else:
            settings.o.output(1,"Player not playing",None)
