# coding=utf-8

import time
import podb
import settings
from random import shuffle


class cplaylist:
    def __init__(self,o):
        self.o = o

    def build_playlist(self,l,lenght):
        if len(l) == 0: return False
        s = sorted(l, key=lambda podcast: podcast.date, reverse=True)
        shuffle(s)
        for i in range(0,min(len(l),lenght)):
            str_date = time.strftime("%a, %d %b %Y %H:%M:%S",s[i].date)
            self.o.output(1,"Playlist %d - %s-%s-%s" % (i,s[i].p_title,s[i].e_title,str_date),None)
            settings.playlist.put(s[i])
        return min(len(l),lenght)

