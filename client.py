import zmq
import time
import sys
import pickle
import debug_output
import settings
from interface_s import RadioMsg
import argparse


def main():
    parser = argparse.ArgumentParser(description='RadioCast CTRL client')
    parser.add_argument('ip',help='IP address of the RadioCast server')
    parser.add_argument('command',help='Either: gaming, movies, various, downloads')
    args = parser.parse_args()

    settings.init()

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    port = "4443"
    socket.connect ("tcp://%s:%s" % (args.ip,port))

    sndmsg = RadioMsg()
    sndmsg.type = None
    if args.command == 'gaming':
        sndmsg.type = settings.LIST_PLAYLIST
        sndmsg.subtype = settings.GAMING
    if args.command == 'movies':
        sndmsg.type = settings.LIST_PLAYLIST
        sndmsg.subtype = settings.MOVIES
    if args.command == 'various':
        sndmsg.type = settings.LIST_PLAYLIST
        sndmsg.subtype = settings.VARIOUS
    if args.command == 'downloads':
        sndmsg.type = settings.LIST_TO_D
        sndmsg.subtype = None
    if sndmsg.type == None:
        print("ERROR: Incorrect command\n")
        exit(-1)
        
    data = pickle.dumps(sndmsg)
    socket.send(data)
    data = socket.recv()
    rcvmsg = RadioMsg()
    rcvmsg = pickle.loads(data)
    for l in rcvmsg.list:
        print(l.pod_to_str())

if __name__ == "__main__":
    main()

