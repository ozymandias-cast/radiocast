import feedparser
import vlc
import time
import xml.etree.ElementTree as ET
import random
import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/")
import sqlite3 as sql
import podb
import debug_output
import download

o = debug_output.debug(False,'')    
p = podb.podb('./radiocast.db',o)
#p.load_podcasts('./Downcast.opml')
#p.print_podcasts()
#p.load_episodes()
#p.print_episodes()
d = download.download(p,o)
d.now()
 

#Podcasts=ReadOPML('./Downcast.opml')
#p = Podcasts
#print ("%s podcasts loaded" % len(Podcasts))

#instance = vlc.Instance()
#player = instance.media_list_player_new()
#medialist = instance.media_list_new()

#for i in range(0,len(p)):
    #num=random.randint(0,len(p))
    #title = p[i][0]
    #url = p[i][1]
    #print ("Trying to add %s - %s (%d)" % (title,url,i+1))
    #try:
        #feed = feedparser.parse(url)
        #item = feed.entries[0].enclosures[0]
        #file = item.href
        #if "feedburner.com" in file:
            #file = file + "?fmt=xml"
    #except:
        #e = sys.exc_info()[0]
        #print e
    #medialist.add_media(instance.media_new(file))
    #print ("Success %s (%d)" % (file,i+1))

#player.set_media_list(medialist)
#player.play()
#time.sleep(5)
#player.next()
#time.sleep(5)
#player.next()
#time.sleep(5)
#player.next()


#Instance = vlc.Instance()
#player = Instance.media_player_new()
#Media = Instance.media_new(file.href)
#player.set_media(Media)
#player.get_media()
#player.play()
#time.sleep(60)
