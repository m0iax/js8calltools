
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


Download the zip file

wget http://m0iax.com/downloads/js8calltools.zip

Next Unzip the files to your home directory

Command line

unzip js8calltoolz.zip

In the command line type

cd ~/js8calltools

chmod +x js8callgpsUI.py

Finally to run the software enter this command:

./js8callgpsUI.py

