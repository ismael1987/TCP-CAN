import socket
import struct
import sys


#sudo ip link add dev vcan0 type vcan  // this each time we want to use the app
#sudo ip link set up vcan0                     // this each time we want to use the app
#to run it "cangen vcan0 -v"                 // when we want to run the simulation

# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
can_frame_fmt = "=IB3x8s"

def build_can_frame(can_id, data):
               can_dlc = len(data)
               data = data.ljust(8, b'\x00')
               return struct.pack(can_frame_fmt, can_id, can_dlc, data)

def dissect_can_frame(frame):
               can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
               return (can_id, can_dlc, data[:can_dlc])

if len(sys.argv) != 2:
               print('Provide CAN device name (can0, slcan0 etc.)')
               sys.exit(0)

       # create a raw socket and bind it to the given CAN interface
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind((sys.argv[1],))


while True:
        cf, addr = s.recvfrom(16)
        writer = open('test.txt', 'a')

        message = 'Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf)
        writer.write(str(message) + '\n')
        writer.close()     
        print(message)

        try:
            s.send(cf)
        except socket.error:
                print('Error sending CAN frame')

        try:
             s.send(build_can_frame(0x01, b'\x01\x02\x03'))
        except socket.error:
                print('Error sending CAN frame')

