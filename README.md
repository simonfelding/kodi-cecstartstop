Starts and stops Kodi when TV powers on and off with a remote control.
Made for Raspberry Pi running Raspbian.

# Requirements
A user named kodi for the kodi service, in groups render, audio, lp

pip install cec

# Install procedure
sudo mv *.service /etc/systemd/system/

sudo mv kodistartstop.py /usr/bin/kodistartstop.py

sudo chmod +x /usr/bin/kodistartstop.py

sudo systemctl enable kodistartstop.service
