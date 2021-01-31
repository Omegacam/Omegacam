# Telemetry ZeroMQ Subscriber
# Copyright (c) 2020 Applied Engineering

import logging
import msgpack
import traceback
import zmq

# Set logging verbosity.
# CRITICAL will not log anything.
# ERROR will only log exceptions.
# INFO will log more information.
log_level = logging.INFO

# ZeroMQ Context.
context = zmq.Context.instance()
# Define the socket using the Context.
sub = context.socket(zmq.SUB)
# Define connection address.
address = 'tcp://127.0.0.1:5555'
# Define subscription.
group = 't'
# Establish the connection.
sub.connect(address)
#dish.join(group)
# Set receive timeout.
#dish.rcvtimeo = 1000

sub.setsockopt(zmq.SUBSCRIBE, b't')

if __name__ == '__main__':
    try:
        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=log_level, datefmt="%H:%M:%S")
        logging.info('Listening for "%s" group data from %s.', group, address)
        while True:
            try:
                print(sub.recv(copy=False, flags=zmq.NOBLOCK))
                logging.info('Received data.')
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    pass    # no message ready yet
                else:
                    traceback.print_exc()
    except KeyboardInterrupt:
        logging.info('Exiting now.')
        sub.close()
    except:
        traceback.print_exc()
