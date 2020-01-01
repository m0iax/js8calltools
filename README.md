# js8calltools

JSCall GPS Tools
By Mark, M0IAX

This software is provided as-is with no warranty whatsoever. Use it at your own risk.

Introduction

This utility will allow you to get your current maidenhead locator from GPSD and set JS8Call's locator.
You may then use this app to send the ALLCALL command in js8call.

First install the pre-requisites:

Ensure you have already installed and configured GPSD. if you do not have that installed this script will not work.

Open a terminal window and enter the following commands:

sudo apt-get install python3

pip3 install gps

pip3 install maidenhead


chmod +x js8callgpsUI.py

Finally to run the software enter this command:

./js8callgpsUI.py

PLEASE NOTE:

JS8Call verison 2 has changed the default UDP port to 2242. This software now creates a settings text file settings.cfg 
Please ensure you either updste the port number in the settings file or change your JS8Call settings to use port 2242

