# coding=utf-8

import time
import podb
import settings
from random import shuffle


class cplaylist:
    def __init__(self,o):
        self.o = o

    def build_playlist(self,l,lenght):
        if len(l) == 0: return 0
        minl = min(len(l),lenght)
        s = sorted(l, key=lambda podcast: podcast.date, reverse=True)
        s[:minl]
        shuffle(s)
        for i in range(0,len(s)):
            str_date = time.strftime("%a, %d %b %Y %H:%M:%S",s[i].date)
            self.o.output(1,"Playlist %d - %s-%s-%s" % (i,s[i].p_title,s[i].e_title,str_date),None)
            settings.playlist.put(s[i])
        return len(s)

