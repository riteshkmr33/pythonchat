import json
import select
import socket
import string
import sys
 
def prompt():
    sys.stdout.write('<> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
    
    user = 'Guest'
    host = '192.168.2.132'
    port = 6000
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to chat. Start sending messages'
    
    if user == 'Guest':
        sys.stdout.write('<' + user + '> Please enter your name to start chat :')
        user = sys.stdin.readline().rstrip('\n')
        s.send(json.dumps({'username' : user}))
        sys.stdout.write('\n<you>:')
     
    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = json.loads(sock.recv(4096))
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    #print data
                    sys.stdout.write('\n<' + data['username'] + '>: ' + data['msg'])
                    sys.stdout.write('\n<you>:')
                    sys.stdout.flush()

            #user entered a message
            else:
                msg = sys.stdin.readline()
                s.send(json.dumps({'username': user, 'msg': msg.rstrip('\n')}))
                sys.stdout.write('\n<you>:')
                sys.stdout.flush()
