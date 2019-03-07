#!/usr/bin/python3
"""Send an OSC message to capinibal"""
# see http://das.nasophon.de/pyliblo/examples.html

import liblo, sys, argparse

parser = argparse.ArgumentParser(description='Send an OSC message to capinibal.')
parser.add_argument('--host', help='IP Address', default='127.0.0.1')
parser.add_argument('--port', help='Port', default='1234')
parser.add_argument('-s', '--speed', default='4',
    help='Speed of change (changes per second)')

args = parser.parse_args()

ip_address = args.host
port = int(args.port)
speed=float(args.speed)

# send message to given port on specified host
try:
    target = liblo.Address(ip_address, port)
except (liblo.AddressError, err):
    print (str(err))
    sys.exit()

# send message "/cpb/speed" with float argument
liblo.send(target, "/cpb/speed", speed)
