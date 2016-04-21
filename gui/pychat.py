#https://github.com/chprice/Python-Chat-Program/blob/master/pyChat.py
#import json
#import select
#import socket
#import string
#import sys
 
#def prompt():
    #   sys.stdout.write('<> ')
        #  sys.stdout.flush()
 
#main function
#if __name__ == "__main__":
    
    #   user = 'Guest'
        #  host = 'localhost'
            # port = 6000
     
                #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #s.settimeout(2)
     
                # connect to remote host
            # try:
                #    s.connect((host, port))
                #except:
                    #   print 'Unable to connect'
                        #  sys.exit()
     
                #print 'Connected to chat. Start sending messages'
    
                #if user == 'Guest':
                    #   sys.stdout.write('<' + user + '> Please enter your name to start chat :')
                    #   user = sys.stdin.readline().rstrip('\n')
                        # s.send(json.dumps({'username': user}))
                    #  sys.stdout.write('\n<you>:')
     
                #while 1:
                    #   socket_list = [sys.stdin, s]

                        # Get the list sockets which are readable
                    #  read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

                        #  for sock in read_sockets:
                            #incoming message from remote server
                        #      if sock == s:
                            #         data = json.loads(sock.recv(4096))
                            #         if not data:
                            #             print '\nDisconnected from chat server'
                            #            sys.exit()
                                #        else:
                                #            #print data
                                #            sys.stdout.write('\n<' + data['username'] + '>: ' + data['msg'])
                                #            sys.stdout.write('\n<you>:')
                                    #           sys.stdout.flush()

                                        #user entered a message
                                    #   else:
                                    #       msg = sys.stdin.readline()
                                        #      s.send(json.dumps({'username': user, 'msg': msg.rstrip('\n')}))
                                        #      sys.stdout.write('\n<you>:')
                                        #      sys.stdout.flush()

import Tkinter
import threading
import socket
import random
import math
import json

class simpleapp_tk(Tkinter.Tk):
    
    user = 'Guest'
    host = '192.168.2.132'
    port = 6000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        
        self.sock.settimeout(10)

        # connect to remote host
        try:
            self.sock.connect((self.host, self.port))
            status = 'Connected to chat. Please enter your name \n'
        except:
            status = 'Unable to connect \n'
            #sys.exit()
            
        self.mainBody = Tkinter.Frame(self, height=20, width=50)

        self.mainBodyText = Tkinter.Text(self.mainBody)
        self.mainBodyTextScroll = Tkinter.Scrollbar(self.mainBody)
        self.mainBodyText.focus_set()
        self.mainBodyTextScroll.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        self.mainBodyText.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
        self.mainBodyTextScroll.config(command=self.mainBodyText.yview)
        self.mainBodyText.config(yscrollcommand=self.mainBodyTextScroll.set)
        self.mainBody.pack()
        
        self.mainBodyText.insert(Tkinter.END, status)
        self.mainBodyText.config(state=Tkinter.DISABLED)
        
        self.entryVariable = Tkinter.StringVar()
        self.textInput = Tkinter.Entry(self, width=60, textvariable=self.entryVariable)
        self.textInput.bind("<Return>", self.OnPressEnter)
        self.textInput.pack()
        
#        self.grid()
#
#        self.entryVariable = Tkinter.StringVar()
#        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
#        self.entry.grid(column=0, row=0, sticky='EW')
#        self.entry.bind("<Return>", self.OnPressEnter)
#        #self.entryVariable.set(u"Enter text here.")
#
#        button = Tkinter.Button(self, text=u"Send",
#                                command=self.OnButtonClick)
#        button.grid(column=1, row=0)
#
#        self.labelVariable = Tkinter.StringVar()
#        label = Tkinter.Message(self, textvariable=self.labelVariable,
#                                anchor="w", fg="black", bg="grey")
#        label.grid(column=0, row=1, columnspan=2, sticky='EW')
#        self.labelVariable.set(status)
#
#        self.grid_columnconfigure(0, weight=1)
#        self.resizable(True, False)
#        self.update()
#        self.geometry(self.geometry())       
#        self.entry.focus_set()
#        self.entry.selection_range(0, Tkinter.END)
        
        #start_new_thread(, (self,))
        threading.Thread(target=self.getMessage).start()
#        while 1:
#            socket_list = [self.labelVariable, self.sock]
#            
#            for sock in socket_list:
#                if sock == self.sock:
#                    data = json.loads(self.sock.recv(4096))
#                    if not data:
#                        self.labelVariable.set("Disconnected from chat server \n"+self.labelVariable.get())
#                    else:
#                        self.labelVariable.set(data['username']+": "+data['msg']+"\n"+self.labelVariable.get())
                

    def OnPressEnter(self, event):
        self.sendMessage()
        
    def sendMessage(self):
        if self.user == 'Guest':
            self.user = self.entryVariable.get()
            self.sock.send(json.dumps({'username': self.user}))
        else:
            self.sock.send(json.dumps({'username': self.user, 'msg': self.entryVariable.get().rstrip('\n')}))
            #self.labelVariable.set("you: " + self.entryVariable.get() + "\n" + self.labelVariable.get())
            self.mainBodyText.config(state=Tkinter.NORMAL)
            self.mainBodyText.insert(Tkinter.END, "you: " + self.entryVariable.get() + "\n")
            self.mainBodyText.yview(Tkinter.END)
            self.mainBodyText.config(state=Tkinter.DISABLED)
            
        self.entryVariable.set("")
        self.textInput.focus_set()
        self.textInput.selection_range(0, Tkinter.END)
    
    def getMessage(self):
        while 1:
            try:
                data = self.sock.recv(4096)
                if data:
                    data = json.loads(data)
                    #print data['username']
                    #if (data['username'] != self.user) or (self.user == "Guest"):
                    #self.labelVariable.set(data['username'] + ": " + data['msg'] + "\n" + self.labelVariable.get())
                    self.mainBodyText.config(state=Tkinter.NORMAL)
                    self.mainBodyText.insert(Tkinter.END, data['username'] + ": " + data['msg'] + "\n")
                    self.mainBodyText.yview(Tkinter.END)
                    self.mainBodyText.config(state=Tkinter.DISABLED)
            except:
                continue

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('chat')
    app.mainloop()