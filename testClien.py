from socket import *
from struct import pack
import time, os


class ClientProtocol:

    def __init__(self):
        self.socket = None

    def connect(self, server_ip, server_port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((server_ip, server_port))

    def close(self):
        self.socket.shutdown(SHUT_WR)
        self.socket.close()
        self.socket = None

    def send_image(self, image_data):

        # use struct to make sure we have a consistent endianness on the length
        length = pack('>Q', len(image_data))

        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(image_data)

        ack = self.socket.recv(1)

        # could handle a bad ack here, but we'll assume it's fine.


if __name__ == '__main__':
    cp = ClientProtocol()

    image_data = None
    filename = 'test.txt'
    with open('test.txt', 'rb') as fp:
        #image_data = fp.read()
        #Find the size of the file and move to the end
        st_results = os.stat(filename)
        st_size = st_results[6]
        fp.seek(st_size)
        while 1:
            where = fp.tell()
            line = fp.readline()
            if not line:
              time.sleep(1)
              fp.seek(where)
            else:
              print (line) # already has newline
              #assert(len(image_data))
              cp.connect('127.0.0.1', 55555)
              cp.send_image(line)
              cp.close()
    #assert(len(image_data))

    