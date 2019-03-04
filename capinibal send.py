#!/usr/bin/python3
# http://das.nasophon.de/pyliblo/examples.html

import liblo, sys

# send all messages to port 1234 on the local machine
try:
    target = liblo.Address(1234)
except (liblo.AddressError, err):
    print (str(err))
    sys.exit()

# send message "/cpb/speed" with float argument
liblo.send(target, "/cpb/speed", 2.0)
