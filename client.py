import zmq
import time
import sys
import pickle
import debug_output
import settings
from interface_s import RadioMsg
import argparse

def print_list(li):
    for l in li:
        print(l.pod_to_str())

def playlist(which):
    sndmsg = RadioMsg()
    sndmsg.type = None
    if which == 'gaming':
        sndmsg.type = settings.LIST_PLAYLIST
        sndmsg.subtype = settings.GAMING
    if which == 'movies':
        sndmsg.type = settings.LIST_PLAYLIST
        sndmsg.subtype = settings.MOVIES
    if which == 'various':
        sndmsg.type = settings.LIST_PLAYLIST
        sndmsg.subtype = settings.VARIOUS
    if which == 'downloads':
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
    return rcvmsg

def main():
    parser = argparse.ArgumentParser(description='RadioCast CTRL client')
    parser.add_argument('ip',help='IP address of the RadioCast server')
    parser.add_argument('command',help='Either: gaming, movies, various, downloads, nowplaying')
    args = parser.parse_args()

    settings.init()

    port = "4443"
    ip = args.ip
    socket.connect ("tcp://%s:%s" % (ip,port))

    rcvmsg = RadioMsg()
    if args.command == 'gaming': 
        rcvmsg = playlist('gaming')
        print_list(rcvmsg.list)
    if args.command == 'movies': 
        rcvmsg = playlist('movies')
        print_list(rcvmsg.list)
    if args.command == 'various': 
        rcvmsg = playlist('various')
        print_list(rcvmsg.list)
    if args.command == 'downloads': 
        rcvmsg = playlist('downloads')
        print_list(rcvmsg.list)
    if args.command == 'nowplaying': 
        rcvmsg = playlist('gaming')
        rcvmsg2 = RadioMsg()
        rcvmsg2 = playlist('movies')
        rcvmsg3 = RadioMsg()
        rcvmsg3 = playlist('various')
        print("Now playing GAMING:\n")
        print(rcvmsg.list[0].pod_to_str())
        print("Now playing MOVIES:\n")
        print(rcvmsg2.list[0].pod_to_str())
        print("Now playing VARIOUS:\n")
        print(rcvmsg3.list[0].pod_to_str())


        



if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    main()

