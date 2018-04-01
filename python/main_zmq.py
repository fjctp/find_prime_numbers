#!/bin/env python3

import argparse
import zmq
import threading
import json
import time

from libs.mylib import is_prime

def parse_args():
    parser = argparse.ArgumentParser(description='Find all prime number in a range (from 2).')
    parser.add_argument('max', type=int, default=1000,
                        help='from 2 to MAX')

    return parser.parse_args()


def worker_routine(worker_url, control_url, context=None):
    """Worker routine"""
    print('thread started')

    context = context or zmq.Context.instance()

    w_socket = context.socket(zmq.REP)
    w_socket.connect(worker_url)

    c_sub = context.socket(zmq.SUB)
    c_sub.connect(control_url)
    c_sub.setsockopt(zmq.SUBSCRIBE, b"S")

    while True:
        try:
            [address, stop_bit] = c_sub.recv_multipart(flags=zmq.NOBLOCK)
            print('==> %s, %s'%(address, stop_bit))
            if int(stop_bit) == 1:
                break
        except zmq.Again as e:
            pass
            
        try:
            string  = w_socket.recv(flags=zmq.NOBLOCK)
            data = json.loads(string)
            value = data['value']
            known_primes = data['known_primes']
            isPrime = is_prime(value, known_primes)
            #print('%d: %d', value, isPrime)

            #send reply back to client
            w_socket.send(b"%d"%isPrime)
            #w_socket.send(b'%d'%True)
        except zmq.Again as e:
            pass

    print('thread terminated')
    #w_socket.close()
    #context.close()

def main(num_threads=2, num_ceil=10, known_primes=[2, ]):
    worker_url = "inproc://workers"
    control_url = "inproc://control"

    context = zmq.Context.instance()
    w_socket = context.socket(zmq.REQ)
    w_socket.bind(worker_url)
    c_pub = context.socket(zmq.PUB)
    c_pub.bind(control_url)

    print('Start threads')
    for i in range(num_threads):
        thread = threading.Thread(target=worker_routine, 
            args=(worker_url, control_url, ))
        thread.start()

    print('Find primes')
    for i in range(3, num_ceil+1):
        data = {'value': i, 'known_primes':known_primes}
        str_data = json.dumps(data)
        b_data = str_data.encode('ascii');

        w_socket.send(b_data)

        y_n = w_socket.recv()
        if int(y_n) == 1:
            known_primes.append(i)

    print('Done finding')
    c_pub.send_multipart([b'S', b'1'])
    time.sleep(1)

    w_socket.close()
    c_pub.close()
    context.term()

    return known_primes


if __name__ == '__main__':
    args = parse_args()

    known_primes = main(2, args.max)

    print(known_primes)