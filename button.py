#!/usr/bin/env python
 
import sys, usb.core

LOGFILENAME='/tmp/foo'

def touchfile():
    try:
        logfile = open(LOGFILENAME, 'r+')
        print "tempfile exists"
        return False
    except IOError:
        # didn't exist yet
        print "tempfile doesn't exist"
        logfile = open(LOGFILENAME, 'w+')
        logfile.close()
        return True


dev = usb.core.find(idVendor=0x04f3, idProduct=0x04a0)
if dev is None:
    sys.exit("No Panic button found in the system");
 
try:
    if dev.is_kernel_driver_active(0) is True:
        dev.detach_kernel_driver(0)
except usb.core.USBError as e:
    sys.exit("Kernel driver won't give up control over device: %s" % str(e))
 
try:
    dev.set_configuration()
    dev.reset()
except usb.core.USBError as e:
    sys.exit("Cannot set configuration the device: %s" % str(e))
 
endpoint = dev[0][(0,0)][0]
while 1:
    try:
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize,
                        timeout=10000)
        if data is not None and len(data) > 2:
            if data[0] == 6 and data[2] == 19:
                # Panic button was pressed!
                print "PRESS BUTAN"
                touchfile()
    except usb.core.USBError as e:
        if e.errno != 110: # 110 is a timeout.
            sys.exit("Error readin data: %s" % str(e))
