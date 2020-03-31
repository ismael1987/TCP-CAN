# TCP-CAN
# To run the app:
1. run the server ==> python3 Server.py
2. run the client ==> python3 Client.py 
==============================
# if we need to run the app and no real device the so we have to init virtual on ubuntu :
# open terminal and write this command:
1. sudo apt-get install can-utils   //this just for one time
2. sudo modprobe vcan              // this also one time
3. sudo ip link add dev vcan0 type vcan  // this each time we want to use the app
4. sudo ip link set up vcan0                     // this each time we want to use the app
5. to run it "cangen vcan0 -v"                 // when we want to run the simulation
