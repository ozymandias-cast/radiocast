import zmq
import time
import sys
import pickle
import debug_output
import settings
from interface_s import RadioMsg

def main():
    settings.init()

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    port = "4443"
    socket.connect ("tcp://localhost:%s" % port)

    sndmsg = RadioMsg()
    sndmsg.type = settings.LIST_PLAYLIST
    sndmsg.subtype = settings.GAMING
    data = pickle.dumps(sndmsg)
    socket.send(data)
    data = socket.recv()
    rcvmsg = RadioMsg()
    rcvmsg = pickle.loads(data)
    for l in rcvmsg.list:
        print(l.pod_to_str())

if __name__ == "__main__":
    main()

