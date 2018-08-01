# coding=utf-8
###################################################################
# Developed by ozymandias-cast (https://github.com/ozymandias-cast)
# License: GPLv3
###################################################################

import time
import podb
import settings
from random import shuffle


class cplaylist:
    def __init__(self):
        pass

    def build_playlist(self,l,length,category):
        if len(l) == 0: return 0
        minl = min(len(l),length)
        s = sorted(l, key=lambda podcast: podcast.date, reverse=True)
        s=s[:minl]
        shuffle(s)
        for i in range(0,len(s)):
            str_date = time.strftime("%a, %d %b %Y %H:%M:%S",s[i].date)
            if (category == 'gaming'): settings.playlist_gaming.put(s[i])
            if (category == 'various'): settings.playlist_various.put(s[i])
            if (category == 'movies'): settings.playlist_movies.put(s[i])
        return len(s)

    def print_playlist(self,category):
        if category == 'gaming': playlist = settings.playlist_gaming
        if category == 'various': playlist = settings.playlist_various
        if category == 'movies': playlist = settings.playlist_movies
        settings.o.output(1,"PLAYLIST %s -------------------------------------------------------------------------------" % category,None)
        while not playlist.empty():
            pod=playlist.get()
            pod.print_podcast()

        

