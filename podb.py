# coding=utf-8
###################################################################
# Developed by ozymandias-cast (https://github.com/ozymandias-cast)
# License: GPLv3
###################################################################

import feedparser
import vlc
import time
import datetime
import xml.etree.ElementTree as ET
import random
import sys
import sqlite3 as sql
import debug_output
import ssl
import settings
import os
from datetime import datetime


class podcast:
    def __init__(self,row):
        self.pod_id = row[0]
        self.p_title = row[1]
        self.e_title = row[2]
        d = row[3]
        d = d[:-6]
        try:
            self.date = time.strptime(d,"%a, %d %b %Y %H:%M:%S")
        except Exception as e:
            d = row[3]
            if 'GMT' in d:
                d = d[:-4]
                try:
                    self.date = time.strptime(d,"%a, %d %b %Y %H:%M:%S")
                except Exception as e:
                    print("Failed to convert time %s" % row[3])
                    sys.exit(0)
        self.file = row[4]
        self.description = row[5]
        self.downloaded = row[6]
        self.downlading = row[7]
        self.mp3 = row[8]
        self.category = row[9]
        self.type = settings.NONE
        return None

    def print_podcast(self):
        str_date = time.strftime("%a, %d %b %Y %H:%M:%S",self.date)
        settings.o.output(1,"Podcast: %s-%s (Category: %s) Date:%s URL: %s Filename: %s" % (self.p_title,self.e_title,self.category,str_date,self.file,self.mp3),None)

    def valid(self):
        now = datetime.now()
        delta = now.year - int(self.date[0])
        settings.o.output(1,"Episode %s-%s old: %d" % (self.p_title,self.e_title,delta),None)
        return delta<settings.delta

class podb:

    def __init__(self,file):
        self.pod_c = 0

        try:
            self.conn = sql.connect(file)
            self.c = self.conn.cursor()
            #self.c.execute("DROP TABLE IF EXISTS episodes")
            #self.c.execute("DROP TABLE IF EXISTS podcasts")
        except Exception as e:
            settings.o.output(0,'Failed connecting to DB',e)

        try:
            self.c.execute("CREATE TABLE IF NOT EXISTS podcasts (id INTEGER PRIMARY KEY AUTOINCREMENT, title, url, category)")
            self.c.execute("CREATE TABLE IF NOT EXISTS episodes (pod_id INTEGER, p_title text, e_title text, date text, file text, description text, downloaded text, downloading text, mp3 text, category text)")
            self.conn.commit()        
        except Exception as e:
            settings.o.output(0,'Failed connecting to DB',e)

    def write_mp3(self,pod):
        try:
            self.c.execute("UPDATE episodes SET mp3=?,downloaded=1,downloading=0 WHERE e_title=?",(pod.mp3,pod.e_title))
            self.conn.commit()
        except Exception as e: 
            settings.o.output(0,"Error writing mp3 %s" %pod. e_title,e)

    def insert_episode(self,pod_id,p_title,e_title,date,file,description,category):
        
        try:
            if (self.episode_exists(e_title) == False):
                str="Inserting episode %s %s %s %s %s" % (pod_id,p_title,e_title,date,file)
                settings.o.output(1,str,None)
                self.c.execute("INSERT INTO episodes(pod_id,p_title,e_title,date,file,description,downloaded,downloading,category) VALUES (?,?,?,?,?,?,?,?,?)",(pod_id,p_title,e_title,date,file,description,0,0,category))
                self.conn.commit()
                return 1
            else: return 0
        except Exception as e: 
            settings.o.output(0,"Error inserting episode %s-%s" % p_title,e_title,e)
            return 0

    def podcast_exists(self,title):
        self.c.execute("SELECT * FROM podcasts WHERE title=?", [title])
        rows = self.c.fetchall()
        if (len(rows)>0): return True
        else: return False

    def episode_exists(self,e_title):
        self.c.execute("SELECT * FROM episodes WHERE e_title=?", [e_title])
        rows = self.c.fetchall()
        if len(rows)>0: 
            settings.o.output(2,"Episode %s already exists" % e_title,None)
            return True
        else: return False

    def insert_podcast(self,title,url,category):
        try:
            if (self.podcast_exists(title) == False):
                settings.o.output(1,"Insertng podcast: %s %s" % (title,url),None)
                self.c.execute("INSERT INTO podcasts(title,url,category) VALUES (?,?,?)",(title,url,category))
            else:
                settings.o.output(2,"Podcast already exists: %s %s" % (title, url),None)
        except Exception as e: self.o.output(0,"Error inserting podcast: (%s,%s)" % (title,url),e)
        self.conn.commit()
        return True

    def lookup_podcast_id(self,p_title):
        self.c.execute("SELECT pod_id FROM episodes WHERE p_title=?",[p_title])
        rows = self.c.fetchall()
        if len(rows) == 0:
            self.pod_c = self.pod_c + 1
            return self.pod_c - 1
        else:
            return int(rows[0][0])

    def load_podcasts(self,file):
        tree = ET.parse(file)
        root = tree.getroot()
        for child in root[1]:
            title = child.get('title')
            url = child.get('xmlUrl')
            category = child.get('category')
            if "feedburner.com" in url:
                url = url + "?fmt=xml"
            self.insert_podcast(title,url,category)

    def load_episodes(self):
        count = 0
        self.c.execute("SELECT url,category FROM podcasts")
        rows = self.c.fetchall()
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        settings.o.output(1,"Trying to load %d episodes" % len(rows),None)
        for row in rows:
            try:
                url = row
                url = url[0]
                category = str(row[1])
                d = feedparser.parse(str(url))
                p_title = d.feed.title
                pod_id = self.lookup_podcast_id(p_title)
            except Exception as e:
                settings.o.output(2,"Error parsing episode %s" % url,e)
                pass
            try: 
                for i in range(0,len(d.entries)):
                    e_title = d.entries[i].title
                    date = d.entries[i].published
                    file2 = d.entries[i].enclosures[0].href
                    description = d.entries[i].description
                    r=self.insert_episode(pod_id,p_title,e_title,date,file2,description,category)
                    count = count + r
            except Exception as e:
                settings.o.output(2,"Error loading episode %s" % url,e)
                pass 
        settings.o.output(1,"Loaded %s new episodes" % count,None)

    def print_podcasts(self):
        count = 0
        for row in self.c.execute("SELECT * FROM podcasts"):
            settings.o.output(3,str(row[0]) + '-' + row[1],None)
            count = count + 1
        settings.o.output(1,"Total Podcasts: %s" % count,None)

    def print_episodes(self):
        count = 0
        for row in self.c.execute("SELECT * FROM episodes"):
            temp = str(row[0]) + '-' + row[1] + '-' + row[2] + '-' + row[3]
            settings.o.output(3,temp,None)
            count = count + 1
        settings.o.output(1,"Total Episodes: %s" % count,None)

    def missing_episodes(self):
        self.c.execute("SELECT * FROM episodes WHERE downloaded=0 AND downloading=0")
        rows = self.c.fetchall()
        self.c.execute("UPDATE episodes SET downloading=1 WHERE downloaded=0 AND downloading=0")
        self.conn.commit()
        return rows

    def housekeeping_downloading(self):
        self.c.execute("SELECT * FROM episodes WHERE downloading=1")
        rows = self.c.fetchall()
        r = len(rows)
        for row in rows:
            pod=self.decode_episode(row)
            settings.o.output(1,"Removing partially downloaded file %s-%s %s" % (pod.p_title,pod.e_title,pod.mp3),None)
            self.remove_file(pod)
        self.c.execute("UPDATE episodes SET downloading=0 WHERE downloading=1")
        self.conn.commit()
        return r

    def downloaded_episodes(self,category):
        self.c.execute("SELECT * FROM episodes WHERE downloaded=1 AND downloading=0 AND category=?",[category])
        rows = self.c.fetchall()
        return rows

    def decode_episode(self,row):
        pod = podcast(row)
        return pod

    def random_playable_podcast(self):
        self.c.execute("SELECT * FROM episodes WHERE downloaded=1")
        rows = self.c.fetchall()
        num=random.randint(0,len(rows)-1)
        if len(rows) == 0: return None
        else: return self.decode_episode(rows[num])

    def too_old(self,pod):
        self.c.execute("UPDATE episodes SET downloading=2 WHERE e_title=?",[pod.e_title])
        self.conn.commit()
        return True

    def do_not_play(self,pod):
        self.c.execute("UPDATE episodes SET downloading=3 WHERE e_title=?",[pod.e_title])
        self.conn.commit()
        return True

    def redownload(self,pod):
        self.c.execute("UPDATE episodes SET downloading=0,downloaded=0 WHERE e_title=?",[pod.e_title])
        self.conn.commit()
        return True

    def do_not_download(self,pod):
        self.c.execute("UPDATE episodes SET downloading=4 WHERE e_title=?",[pod.e_title])
        self.conn.commit()
        return True

    def close(self):
        self.conn.commit()
        self.conn.close()

    def remove_file(self,pod):
        if pod.mp3 == None: return False
        filename = settings.gpath + str(pod.mp3)
        try:
            os.remove(filename)
        except Exception as e:
            settings.o.output(1,"Trying to remove file that does not exists: %s-%s %s" % (pod.p_title,pod.e_title,pod.mp3),None)
        return True

    def file_exists(self,pod):
        if pod.mp3 == None: return False
        filename = settings.gpath + str(pod.mp3)
        return os.path.isfile(filename) 


