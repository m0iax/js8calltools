#! /usr/bin/python3
'''
Created on 21 May 2019
JS8CallGPSUI Copyright 2019 M0IAX
@author: Mark Bumstead M0IAX
http://m0iax.com
'''

import tkinter as tk
from tkinter import StringVar
import socket, time, json
import gps_listener as gpsl
import configAndSettings

HEIGHT=500
WIDTH=500
JS8CALL_IPADDRESS=configAndSettings.getAttribute("JS8CALLSERVER", "serverip")
JS8CALL_PORT=int(configAndSettings.getAttribute("JS8CALLSERVER", "serverport"))

SERIAL_ENABLED=False
TYPE_STATION_SETGRID='STATION.SET_GRID'
TYPE_TX_GRID='TX.SEND_MESSAGE'
TYPE_TX_SETMESSAGE='TX.SET_TEXT'
TYPE_TX_SEND='TX.SEND_MESSAGE'
TYPE_WINDOWRAISE='WINDOW.RAISE'
TXT_ALLCALLGRID='@APRSIS GRID '
TYPE_STATION_GETCALLSIGN='STATION.GET_CALLSIGN'
UDP_ENABLED=False
global getResponse
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       
class utils:
    def from_message(self,content):
        try:
            return json.loads(content)
        except ValueError:
            return {}
    def to_message(self,typ, value, params=None):
        if params is None:
            params = {}
        if typ==TYPE_STATION_GETCALLSIGN:
            self.getResponse=True
        return json.dumps({'type': typ, 'value': value, 'params': params})
        
class SendToJS8Call:
       
    def send(self, *args, **kwargs):
        params = kwargs.get('params', {})
        if '_ID' not in params:
            params['_ID'] = int(time.time()*1000)
            kwargs['params'] = params
        message = utils.to_message(self,*args, **kwargs)
        print('outgoing message to JS8Call:', message)
        if self.first:
            self.first=False
            sock.bind((JS8CALL_IPADDRESS,JS8CALL_PORT))
            content, self.addr = sock.recvfrom(65500)
        reply_to = self.addr
        print(reply_to)
        print("Please Wait...")
        sock.sendto(message.encode(),reply_to)
        value=''
        if self.getResponse:
            data=sock.recv(65550)
            data=utils.from_message(self, data)
            value=data.get('value','')
            print("Got Value ",value)
            self.getResponse=False
        print("Message Sent.")
     
class UserInterface:
    
    first=True
    addr = ('127.0.0.1',65500)
    getResponse=False
    def __init__(self):
        self.MAX_TIMER=600    
    
        self.mainWindow=tk.Tk()
        self.mainWindow.title("JS8CALL GPS Utilities by M0IAX")

        
        self.first=True
        self.getResponse=False
        
        canvas = tk.Canvas(self.mainWindow, height=HEIGHT, width=WIDTH)
        canvas.pack()
        
        self.var1 = StringVar()
        self.var2 = StringVar()

        frame=tk.Frame(self.mainWindow, bg="black", bd=5)
        frame.place(relx=0.5,rely=0.1, relwidth=0.85, relheight=0.2, anchor='n')
        
        self.gridrefEntry = tk.Entry(frame, font=40, textvariable=self.var1)
        self.gridrefEntry.place(relwidth=0.5,relheight=1)
        
        self.getGridButton = tk.Button(frame, text="Get Grid from GPS", command=self.getGrid, bg="white", font=30)
        self.getGridButton.place(relx=0.6,relwidth=0.4,relheight=1)
        
        lowerFrame=tk.Frame(self.mainWindow, bg="black", bd=5)
        lowerFrame.place(relx=0.5,rely=0.3, relwidth=0.85, relheight=0.6, anchor='n')
        
        
        self.setJS8CallGridButton = tk.Button(lowerFrame, text="Send Grid to JS8Call", command=lambda: self.sendGridToJS8Call(self.gridrefEntry.get()), bg="white", font=40)
        self.setJS8CallGridButton.place(relx=0.02, relwidth=0.45,relheight=0.4)
        self.setJS8CallGridButton.configure(state='disabled')
        
        self.sendJS8CallALLCALLButton = tk.Button(lowerFrame, text="TX Grid to @ALLCALL", command=lambda: self.sendGridToALLCALL(self.gridrefEntry.get()), bg="white", font=40)
        self.sendJS8CallALLCALLButton.place(relx=0.55,relwidth=0.44,relheight=0.4)
        self.sendJS8CallALLCALLButton.configure(state='disabled')
        
        self.autoGridToJS8Call = 0
        self.autoGridCheck = tk.Checkbutton(lowerFrame, text="Auto update JS8Call Grid every 10 minutes.", variable=self.autoGridToJS8Call, command=self.cb)
        self.autoGridCheck.place(relx=0.05,rely=0.5, relwidth=0.9,relheight=0.1)
        
        self.timerlabel = tk.Label(lowerFrame,text="When timer reaches zero\nThe Grid in JS8Call will be updated.\nIt does NOT transmit, use the button above to do that.", bg="black", fg="white")
        self.timerlabel.place(relx=0.05,rely=0.6, relwidth=0.9,relheight=0.18)
        
        self.timer=30
        self.timerStr = StringVar()
        
        self.timerStr.set("Timer Not Active")
        self.timerlabel = tk.Label(lowerFrame, textvariable=self.timerStr )
        self.timerlabel.place(relx=0.05,rely=0.9, relwidth=0.9,relheight=0.1)
        
        self.update_timer()
        self.mainWindow.mainloop()
    def cb(self):
        if self.autoGridToJS8Call==0:
            self.autoGridToJS8Call=1
        else:
            self.autoGridToJS8Call=0
            self.timerStr.set("Timer Not Active")
    def update_timer(self):
        if self.autoGridToJS8Call==0:
            self.initTimer()
        if self.autoGridToJS8Call==1:
            if self.timer<=0:
                self.initTimer()
            self.timer=self.timer-1
            t="Timer: " + str(self.timer)
            self.timerStr.set(t)
            if self.timer<=0:
                gridstr = self.getGrid()
                self.sendGridToJS8Call(gridstr)
                self.initTimer()
        self.mainWindow.after(1000, self.update_timer)
        
    def initTimer(self):
            self.timer=self.MAX_TIMER
            
    def sendGridToJS8Call(self, gridText):
        print('Sending Grid to JS8CAll...',gridText) 
        UDP_ENABLED=True
        SendToJS8Call.send(self,TYPE_STATION_SETGRID, gridText)
        UDP_ENABLED=False
    
    def sendGridToALLCALL(self,gridText):
        messageToSend = TXT_ALLCALLGRID + gridText
        print("Sending ", messageToSend)
        SendToJS8Call.send(self,TYPE_WINDOWRAISE,'')
        SendToJS8Call.send(self, TYPE_TX_SEND, messageToSend)
        
    def getCallsignFromJS8Call(self):
        callsign=SendToJS8Call.send(self, TYPE_STATION_GETCALLSIGN,'')
        self.var2 = callsign
        
    def getGrid(self):
        print('Getting Grid from GPS')
        
        gpsText = gpsl.gpsl.get_current_mhgrid()
        gpsTime = gpsl.gpsl.get_current_gpstime()
        print("Got Grid "+gpsText, gpsTime)
        
        if gpsText!= "No Fix":
            self.setJS8CallGridButton.configure(state='normal')
            self.sendJS8CallALLCALLButton.configure(state='normal')
        else:
            self.setJS8CallGridButton.configure(state='disabled')
            self.sendJS8CallALLCALLButton.configure(state='disabled')
        
        self.var1.set(gpsText)
        return gpsText
        
        

try:
    b = UserInterface()
    gpsl.gpsl.setrun(False)
    
finally:
    gpsl.gpsl.setrun(False)
    

