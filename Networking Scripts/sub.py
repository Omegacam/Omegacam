import zmq
import time

ctx = zmq.Context()
sock = ctx.socket(zmq.SUB)
sock.connect("tcp://192.168.1.10:1234")
sock.subscribe("") # Subscribe to all topics

print("Starting receiver loop ...")
while True:
    msg = sock.recv_string()
    print("Received string: %s ..." % msg)

sock.close()
ctx.term()
