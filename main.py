#!/usr/bin/env python3
import os, cec, syslog, psutil, time, sys


cec.init()
tv = cec.Device(0)

if tv.is_on():
    tv_on = True
else:
    tv_on = False

def logger(msg):
    if "-v" in sys.argv[1:]:
        print(msg)


def power_state(type, layer, time, message):
    global tv_on
    logger(message)
    if tv_on == False:
        if "to 'on'" in message: # power status on
            tv_on = True
            logger("TV is on")
    if tv_on == True:
        if '>> 0f:36' == message: # tell all to power off code
            tv_on = False
            logger("TV is off")
            sleep(5)
    if tv_on == False and message == "logical address changed to Broadcast (f)": # restart if broken
        cec.init()

cec.add_callback(power_state, cec.EVENT_LOG)

while True:
    if tv_on == True:
        if "kodi" not in (p.name() for p in psutil.process_iter()):
            logger("starting kodi")
            os.system("/usr/bin/kodi &")
        while tv_on == True:
            logger("sleep while on")
            time.sleep(3)
    if tv_on == False:
        if "kodi" in (p.name() for p in psutil.process_iter()):
            os.system("/usr/bin/pkill kodi.bin_v8")
            logger("tv is off. stopping kodi")
        while tv_on == False:
            logger("sleep while off")
            time.sleep(3)
