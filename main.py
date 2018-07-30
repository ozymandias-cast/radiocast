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
settings.init()
p = podb.podb(settings.db,o)
cp = playlist.cplaylist(o)

p.load_podcasts(settings.pod_xml)
p.load_episodes()

d = download.download(o)
d.start()

play = player.player(o,settings.ip,settings.port_gaming,'gaming')
play.start()
play = player.player(o,settings.ip,settings.port_movies,'gaming')
play.start()
play = player.player(o,settings.ip,settings.port_movies,'various')
play.start()


## Building playlist Gaming
category = 'gaming'
rows = p.downloaded_episodes(category)
o.output(1,"Episodes already downloaded (%s) %d" % (category,len(rows)),None)
l = list()
for row in rows:
    l.append(p.decode_episode(row))
res = cp.build_playlist(l,40,category)
if res==0: o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)

## Building playlist Movies
category = 'movies'
rows = p.downloaded_episodes(category)
o.output(1,"Episodes already downloaded (%s) %d" % (category,len(rows)),None)
l = list()
for row in rows:
    l.append(p.decode_episode(row))
res = cp.build_playlist(l,40,category)
if res==0: o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)

## Building playlist Movies
category = 'various'
rows = p.downloaded_episodes(category)
o.output(1,"Episodes already downloaded (%s) %d" % (category,len(rows)),None)
l = list()
for row in rows:
    l.append(p.decode_episode(row))
res = cp.build_playlist(l,40,category)
if res==0: o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)

while True:
    
    ## Updating Episodes
    p.load_podcasts(settings.pod_xml)
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
    ## Building playlist Gaming
    if settings.playlist_gaming.empty():
        category = 'gaming'
        rows = p.downloaded_episodes(category)
        o.output(1,"Episodes already downloaded (%s) %d" % (category,len(rows)),None)
        l = list()
        for row in rows:
            l.append(p.decode_episode(row))
        res = cp.build_playlist(l,40,category)
        if res==0: o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)

    ## Building playlist Movies
    if settings.playlist_movies.empty():
        category = 'movies'
        rows = p.downloaded_episodes(category)
        o.output(1,"Episodes already downloaded (%s) %d" % (category,len(rows)),None)
        l = list()
        for row in rows:
            l.append(p.decode_episode(row))
        res = cp.build_playlist(l,40,category)
        if res==0: o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)

    ## Building playlist Various
    if settings.playlist_various.empty():
        category = 'various'
        rows = p.downloaded_episodes(category)
        o.output(1,"Episodes already downloaded (%s) %d" % (category,len(rows)),None)
        l = list()
        for row in rows:
            l.append(p.decode_episode(row))
        res = cp.build_playlist(l,40,category)
        if res==0: o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)

    ## Sleeping
    minlen = min(settings.playlist_gaming.qsize(),settings.playlist_movies.qsize(),settings.playlist_various.qsize())
    o.output(1,"Gaming playlist size: %d" % settings.playlist_gaming.qsize(),None)
    cp.print_playlist('gaming')
    o.output(1,"Movies playlist size: %d" % settings.playlist_movies.qsize(),None)
    cp.print_playlist('movies')
    o.output(1,"Various playlist size: %d" % settings.playlist_various.qsize(),None)
    cp.print_playlist('various')
    if minlen > 0:
        sleep_time = 10*minlen
        o.output(1,"Already playing, sleeping for %ds" % sleep_time,None)
        time.sleep(sleep_time)
    
    if not settings.to_d.empty():
        sleep_time = 60
        o.output(1,"Already downloading, sleeping for %ds (to_d queue size: %d)" % (sleep_time,settings.to_d.qsize()),None)
        time.sleep(sleep_time)

