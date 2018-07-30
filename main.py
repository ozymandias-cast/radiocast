# coding=utf-8

import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/")
sys.path.append("./")
import feedparser
import vlc
import time
import xml.etree.ElementTree as ET
import random
import sqlite3 as sql
import podb
import debug_output
import download
from threading import Thread
import settings
import player
import playlist
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

o = debug_output.debug(False,'')    
p = podb.podb('/podcasts/radiocast.db',o)
settings.init()
cp = playlist.cplaylist(o)

p.load_podcasts('/podcasts/Downcast.opml')
p.load_episodes()

d = download.download(o)
d.start()

play = player.player(o,settings.ip,settings.port)
play.start()

## Building playlist
rows = p.downloaded_episodes()
o.output(1,"Episodes already downloaded %d" % len(rows),None)
l = list()
for row in rows:
    l.append(p.decode_episode(row))
res = cp.build_playlist(l,40)
if res==0: o.output(1,"Cannot start playing, no mp3 downloaded",None)
 
while True:
    
    ## Updating Episodes
    p.load_podcasts()
    p.load_episodes()
    
    ## Adding episodes to download
    rows = p.missing_episodes()
    o.output(1,"Missing Episodes %d" % len(rows),None)
    for row in rows:
        settings.to_d.put(p.decode_episode(row))
    if settings.to_d.empty(): 
        r=p.housekeeping_downloading()
        o.output(1,"Housekeeping Downloading episodes: %d" % r,None)
       
    ## Storing downloaded episodes
    o.output(1,"Downloaded episodes to be stored %d" % settings.from_d.qsize(), None)
    while not settings.from_d.empty():
        try:
            pod = settings.from_d.get(block = False)
            if pod.mp3 == None: pass
            else: 
                o.output(1,"New available episode %s - %s - %s" % (pod.p_title,pod.e_title,pod.date),None)
                p.write_mp3(pod)
        except Exception as e:
            o.output(1,"Failed to download episode",e)
        settings.from_d.task_done()

    ## Re-building playlist
    if settings.playlist.empty():
        rows = p.downloaded_episodes()
        o.output(1,"Episodes already downloaded %d" % len(rows),None)
        l = list()
        for row in rows:
            l.append(p.decode_episode(row))
        res = cp.build_playlist(l,40)
        if res==0: o.output(1,"Cannot start playing, no mp3 downloaded",None)

    ## Sleeping
    if not settings.playlist.empty():
        sleep_time = 10*settings.playlist.qsize()
        o.output(1,"Sleeping for %ds" % sleep_time,None)
        time.sleep(sleep_time)

