import socket
import sys
from thread import *
import struct

HOST = '127.0.0.1'
PORT = 9999

# lamp`s functions, add here new function
def on(length):
    return 'turn on lamp'

def off(length):
    return 'turn off lamp'

def color(length):
    if(length==3):
        # each function can use its own struct                      
        color_struct = struct.Struct('!BBB')
        data = conn.recv(length)
        value = color_struct.unpack(data)
        return 'lamp color now is #'+str(struct.pack('BBB',*value).encode('hex'))
    else:
        return 'wrong color'

# request          
def clientthread(conn):
    while True:
        # receive 2 bytes: type and length    
        data = conn.recv(2)
        if not data:
            break
        type = type_struct.unpack(data[0])[0]
        length = type_struct.unpack(data[1])[0]
        switcher = {
            0x12: on,
            0x13: off,
            0x20: color,
            # add here new functions      
        }
        func = switcher.get(type)
        conn.sendall(func(length))
    conn.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
    except socket.error , msg:
        print 'bind failed. err code : ' + str(msg[0]) + ' err msg ' + msg[1]
        sys.exit()
    s.listen(10)

    type_struct = struct.Struct('!B')
    length_struct = struct.Struct('!B')

    while 1:
        conn, addr = s.accept()
        start_new_thread(clientthread ,(conn,))

    s.close()



