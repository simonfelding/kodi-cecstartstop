#!/usr/bin/env python3

# Kodi start-stop script 

import cec,time,os

def listener(a,b,c,message):
    global on
    if '>> 0f:36' == message:
        on = 0

def init():
    cec.init()
    global tv
    tv = cec.Device(0)
    global on
    if tv.is_on():
    	on = 1 # avoids polling the tv all the time and causing libCEC errors.
    else:
        on = 0
    cec.add_callback(listener, cec.EVENT_LOG)

# relaunched by systemctl to evade a CEC bug with Kodi, otherwhise put this part in a while true loop.
def main():
    init()

    while on == 0: # wait for TV on
        time.sleep(1)
    os.system("systemctl start kodi")

    while on == 1: # wait for TV off
        time.sleep(1)
    os.system("systemctl stop kodi")
    time.sleep(30) # waiting for kodi to finish

if __name__ == "__main__":
    main()
