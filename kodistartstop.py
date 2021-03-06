#!/usr/bin/env python3

# Kodi start-stop script

import cec,time,os,sys,psutil,syslog

def logger(str):
    global verbose
    if "-v" in sys.argv[1:]:
        print(str)
    else:
        syslog.syslog(f"kodistartstop: {str}")

def listener(a,b,c,message):
    global on
    if '>> 0f:36' == message:
        on = 0
    if tv.is_on():
        on = 1

def init():
    cec.init()
    global tv
    tv = cec.Device(0)
    global on
    try:
        if tv.is_on():
            on = 1 # avoids polling the tv all the time and causing libCEC errors.
        else:
            on = 0
    except:
        on = 0
    cec.add_callback(listener, cec.EVENT_LOG)

# relaunched by systemctl to evade a CEC bug with Kodi, otherwhise put this part in a while true loop.
def main():
    if "-v" in sys.argv[1:]:
        print("-v in arguments, logging to stdout only")
    logger("initialising")
    init()
    logger("finished init")

    while on == 0: # wait for TV on
        time.sleep(0.1)
    logger("tv is on, starting bluetooth and kodi")
    os.system("systemctl start pulseaudio-bluetooth")
    os.system("systemctl start kodi")
    while on == 1:
        if "kodi" not in (p.name() for p in psutil.process_iter()): # wait for TV off/kodi exit
            logger("kodi process not running but tv is on. restarting kodi..")
            os.system("systemctl start kodi")
        time.sleep(0.5)
    logger("tv is off, stopping kodi and bluetooth")
    os.system("systemctl stop kodi")
    os.system("systemctl stop pulseaudio-bluetooth")
    while tv.is_on() or "kodi" in (p.name() for p in psutil.process_iter()):
        logger("waiting for kodi and tv to be off")
        time.sleep(0.5)
    logger("now the whole thing is off.")
if __name__ == "__main__":
    main()
