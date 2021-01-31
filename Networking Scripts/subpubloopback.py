import time
import zmq

ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)
sub = ctx.socket(zmq.SUB)

url = "tcp://127.0.0.1:5555"
pub.bind(url)
sub.connect(url)

# subscribe to 'a' and 'b'
sub.setsockopt(zmq.SUBSCRIBE, b'a')
sub.setsockopt(zmq.SUBSCRIBE, b'b')

time.sleep(1)

for word in [ 'alpha', 'beta', 'gamma', 'apple', 'carrot', 'bagel']:
    pub.send(word)

time.sleep(1)

for i in range(4):
    print sub.recv(zmq.NOBLOCK)
