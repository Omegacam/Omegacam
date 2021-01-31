import zmq
import time

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.bind("tcp://*:1234")

print("Starting loop...")
i = 1
while True:
    msg = "Hi for the %d:th time..." % i
    sock.send_string(msg)
    print("Sent string: %s ..." % msg)
    i += 1
    time.sleep(1)

sock.close()
ctx.term()
