# coding=utf-8
###################################################################
# Developed by ozymandias-cast (https://github.com/ozymandias-cast)
# License: GPLv3
###################################################################

import sys
import signal
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/")
sys.path.append("./")
import feedparser
import vlc
import time
import xml.etree.ElementTree as ET
import random
import sqlite3 as sql
import podb
import os
import debug_output
import download
from threading import Thread
import datetime
import settings
import player
import playlist

def signal_handler(sig, frame):
    if (sig == signal.SIGTERM or sig==signal.SIGINT):
        settings.o.output(1,"Terminating gracefuly",None)
        p.close()
    if (sig == signal.SIGUSR1):
        settings.o.output(1,"Self-destruction",None)
        p.close()
    os._exit(0)


def main_new_playlist(category):
    if category == 'gaming':
        settings.o.output(1,"Current Gaming Playlist: %d" % settings.playlist_gaming.qsize(),None)
        if settings.playlist_gaming.empty():
            rows = p.downloaded_episodes(category)
            if len(rows) > 0: 
                settings.o.output(1,"Building new playlist (%s) Available episodes: %d" % (category,len(rows)),None)
                l = list()
                for row in rows:
                    l.append(p.decode_episode(row))
                res = cp.build_playlist(l,40,category)
                #cp.print_playlist(category)
            else: settings.o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)
    if category == 'movies':
        settings.o.output(1,"Current Movies Playlist: %d" % settings.playlist_movies.qsize(),None)
        if settings.playlist_movies.empty():
            rows = p.downloaded_episodes(category)
            if len(rows) > 0: 
                settings.o.output(1,"Building new playlist (%s) Available episodes: %d" % (category,len(rows)),None)
                l = list()
                for row in rows:
                    l.append(p.decode_episode(row))
                res = cp.build_playlist(l,40,category)
                #cp.print_playlist(category)
            else: settings.o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)
    if category == 'various':
        settings.o.output(1,"Current Various Playlist: %d" % settings.playlist_various.qsize(),None)
        if settings.playlist_various.empty():
            rows = p.downloaded_episodes(category)
            if len(rows) > 0: 
                settings.o.output(1,"Building new playlist (%s) Available episodes: %d" % (category,len(rows)),None)
                l = list()
                for row in rows:
                    l.append(p.decode_episode(row))
                res = cp.build_playlist(l,40,category)
                #cp.print_playlist(category)
            else: settings.o.output(1,"Cannot start playing %s, no mp3 downloaded" % category,None)

def main():

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    p.load_podcasts(settings.pod_xml)
    p.load_episodes()

    d.start()

    play_gaming.start()
    play_movies.start()
    play_various.start()

    ## Building playlist Gaming
    main_new_playlist('gaming')

    ## Building playlist Movies
    main_new_playlist('movies')

    ## Building playlist Movies
    main_new_playlist('various')

    while True:
        
        ## Updating Episodes
        p.load_podcasts(settings.pod_xml)
        p.load_episodes()
        
        ## Adding episodes to download
        rows = p.missing_episodes()
        settings.o.output(1,"Missing Episodes %d" % len(rows),None)
        for row in rows:
            pod=p.decode_episode(row)
            pod.type = settings.DOWNLOAD
            if (pod.valid()): 
                settings.to_d.put(pod)
            else:
                settings.o.output(1,"Episode too old:",None)
                pod.print_podcast()
                p.too_old(pod)
        if settings.to_d.empty(): 
            r=p.housekeeping_downloading()
            settings.o.output(1,"Housekeeping Downloading episodes: %d" % r,None)
        
        ## Storing downloaded episodes
        settings.o.output(1,"Downloaded episodes to be stored %d" % settings.from_d.qsize(), None)
        while not settings.from_d.empty():
            try:
                pod = settings.from_d.get(block = False)
                if not pod.type == settings.DOWNLOADED: 
                    if pod.type == settings.FILENOTFOUND:
                        if p.file_exists(pod):
                            settings.o.output(1,"File %s (%s-%s) cannot be played" % (pod.mp3,pod.p_title,pod.e_title),None)
                            p.remove_file(pod)
                            p.do_not_play(pod)
                        else:
                            settings.o.output(1,"Episode %s (%s-%s) exist but file not found" % (pod.mp3,pod.p_title,pod.e_title),None)
                            p.redownload(pod)
                    if pod.type == settings.URLNOTFOUND:
                        settings.o.output(1,"Episode (%s-%s) cannot be downloaded" % (pod.p_title,pod.e_title),None) 
                        p.do_not_download(pod)
                else: 
                    settings.o.output(1,"New available episode %s - %s - %s" % (pod.p_title,pod.e_title,pod.date),None)
                    p.write_mp3(pod)
            except Exception as e:
                settings.o.output(1,"Failed to download episode",e)
            settings.from_d.task_done()

        ## Re-building playlist
        ## Building playlist Gaming
        main_new_playlist('gaming')
        #play_gaming.is_playing()
            
        ## Building playlist Movies
        main_new_playlist('movies')
        #play_movies.is_playing()

        ## Building playlist Movies
        main_new_playlist('various')
        #play_various.is_playing()

        ## Sleeping
        minlen = min(settings.playlist_gaming.qsize(),settings.playlist_movies.qsize(),settings.playlist_various.qsize())
        if minlen > 0:
            sleep_time = 10*minlen
            settings.o.output(1,"Already playing, sleeping for %ds" % sleep_time,None)
            time.sleep(sleep_time)
        
        if not settings.to_d.empty():
            sleep_time = 100
            settings.o.output(1,"Already downloading, sleeping for %ds (to_d queue size: %d)" % (sleep_time,settings.to_d.qsize()),None)
            time.sleep(sleep_time)

if __name__ == "__main__":
    #try: 
        if sys.version[0] == '2': import Queue as queue
        else: import queue as queue
        settings.init()
        p = podb.podb(settings.db)
        cp = playlist.cplaylist()
        d = download.download()
        play_gaming = player.player(settings.ip,settings.port_gaming,'gaming')
        play_movies = player.player(settings.ip,settings.port_movies,'movies')
        play_various = player.player(settings.ip,settings.port_various,'various')
        main()
    #except Exception as e:
        #print("Exception not handled in main: %s" % str(e))
        #sys.exit(0)

