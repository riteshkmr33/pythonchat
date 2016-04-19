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
            
#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import json
import select
import socket
import string
import sys
import threading

class simpleapp_tk(Tkinter.Tk):
    
    user = 'Guest'
    host = '127.0.0.1'
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
            status = 'Connected to chat. Please enter your name'
        except:
            status = 'Unable to connect'
            #sys.exit()

        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0, sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        #self.entryVariable.set(u"Enter text here.")

        button = Tkinter.Button(self, text=u"Send",
                                command=self.OnButtonClick)
        button.grid(column=1, row=0)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Message(self, textvariable=self.labelVariable,
                              anchor="w", fg="black", bg="grey")
        label.grid(column=0, row=1, columnspan=2, sticky='EW')
        self.labelVariable.set(status)

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
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
                

    def OnButtonClick(self):
        self.sendMessage()

    def OnPressEnter(self, event):
        self.sendMessage()
        
    def sendMessage(self):
        if self.user == 'Guest':
            self.user = self.entryVariable.get()
            self.sock.send(json.dumps({'username': self.user}))
        else:
            self.sock.send(json.dumps({'username': self.user, 'msg': self.entryVariable.get().rstrip('\n')}))
            self.labelVariable.set("you: "+self.entryVariable.get()+"\n"+self.labelVariable.get())
            
        self.entryVariable.set("")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
    
    def getMessage(self):
        while 1:
            data = self.sock.recv(4096)
            if data:
                data = json.loads(data)
                self.labelVariable.set(data['username']+": "+data['msg']+"\n"+self.labelVariable.get())

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('chat')
    app.mainloop()