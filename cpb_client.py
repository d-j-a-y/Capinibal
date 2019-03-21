#!/usr/bin/python3
"""Send an OSC message to capinibal"""
# see http://das.nasophon.de/pyliblo/examples.html

import liblo, sys, argparse

import pandas as pd

import time


parser = argparse.ArgumentParser(description='Send an OSC message to capinibal.')

parser.add_argument('--host', help='IP Address', default='127.0.0.1')
parser.add_argument('--port', help='Port', default='1234')
parser.add_argument('-s', '--speed', help='Speed of change (changes per second)')
parser.add_argument('-i', '--increase',  help='Increase Speed of change')
parser.add_argument('-d', '--decrease',  help='Decrease Speed of change')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable debug output (default: off)')

args = parser.parse_args()

if (args.verbose):
    print (args)

ip_address = args.host
port = int(args.port)

speed = inc = dec = None

if args.speed is not None:
    speed=float(args.speed)
elif args.increase is not None:
    inc=int(args.increase)
elif args.decrease is not None:
    dec=int(args.decrease)

if (args.verbose):
    print (speed, inc, dec)

while (True):

    dataframes = pd.read_html('http://bourse.latribune.fr/indices.html')
    df1 = dataframes[2]

    total_var_french_stock = 0;

    for var in df1 ['Variation %']:
        total_var_french_stock += float(var[:-1].replace(',', '.'))
        print ('var', var, 'total var', total_var_french_stock)


    if (total_var_french_stock >= 0):
        inc = int(total_var_french_stock * 10 )
    else :
        dec = int(-total_var_french_stock * 10 )

    # send message to given port on specified host
    try:
        target = liblo.Address(ip_address, port)
    except (liblo.AddressError, err):
        print (str(err))
        sys.exit()

    # ~ if speed is not None:
        # ~ # send message "/cpb/speed" with float argument
        # ~ liblo.send(target, "/cpb/speed", speed)
    # ~ el
    if inc is not None:
        # send message "/cpb/increase" with int argument
        print ("Send inc", inc)
        liblo.send(target, "/cpb/increase", inc)
    elif dec is not None:
        # send message "/cpb/decrease" with int argument
        print ("Send dec", dec)
        liblo.send(target, "/cpb/decrease", dec)
    else:
        print ("Nothing happend !!!")
        parser.print_help()

    # Wait for 15 seconds
    time.sleep(15)
