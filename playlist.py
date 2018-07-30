# coding=utf-8

import time
import podb
import settings
from random import shuffle


class cplaylist:
    def __init__(self,o):
        self.o = o

    def build_playlist(self,l,length):
        if len(l) == 0: return 0
        minl = min(len(l),length)
        self.o.output(1,"Building playlist: l-%d length-%d min-%d" % (len(l),length,minl),None)
        s = sorted(l, key=lambda podcast: podcast.date, reverse=False)
        str_date1 = time.strftime("%a, %d %b %Y %H:%M:%S",s[0].date)
        str_date2 = time.strftime("%a, %d %b %Y %H:%M:%S",s[(len(s)-1)].date)
        self.o.output(1,"Head %s Tail %s" % (str_date1,str_date2),None)
        s[:minl]
        shuffle(s)
        for i in range(0,len(s)):
            str_date = time.strftime("%a, %d %b %Y %H:%M:%S",s[i].date)
            self.o.output(1,"Playlist %d - %s-%s-%s" % (i,s[i].p_title,s[i].e_title,str_date),None)
            settings.playlist.put(s[i])
        return len(s)

