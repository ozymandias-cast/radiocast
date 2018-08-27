import zmq
import time
import sys
import pickle
import debug_output
import settings
from threading import Thread


class RadioMsg:
    def __init__(self):
        self.type = 0
        self.subtype = 0
        self.list = None
        return None

class zmqinterface(Thread):
    def __init__(self,port):
        Thread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        settings.o.output(1,"Interface UP on port %s" % port,None)
        self.socket.bind("tcp://*:%s" % port)

    def parse_message(self,rcvmsg):
        sndmsg = RadioMsg()
        if rcvmsg.type == settings.LIST_PLAYLIST:
            sndmsg.type = settings.LIST_PLAYLIST
            if (rcvmsg.subtype == settings.GAMING):
                sndmsg.subtype = settings.GAMING 
                sndmsg.list = list(settings.playlist_gaming.queue)
            if (rcvmsg.subtype == settings.VARIOUS): 
                sndmsg.subtype = settings.VARIOUS
                sndmsg.list = list(settings.playlist_various.queue)
            if (rcvmsg.subtype == settings.MOVIES): 
                sndmsg.subtype = settings.MOVIES.copy()
                sndmsg.list = list(settings.playlist_movies.queue)
        if rcvmsg.type == settings.LIST_TO_D:
            sndmsg.type = settings.LIST_TO_D
            sndmsg.subtype = None
            sndmsg.list = list(settings.to_d.queue)
        return sndmsg
        
    def run(self):
        while True:
            data = self.socket.recv()
            settings.o.output(1,"ZMQ: Message received",None)
            radiomsg = RadioMsg()
            rcvmsg = pickle.loads(data)
            sndmsg = self.parse_message(rcvmsg)
            data = pickle.dumps(sndmsg)
            self.socket.send(data)
