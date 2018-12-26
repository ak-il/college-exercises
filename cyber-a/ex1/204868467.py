#!/usr/bin/python

import sys, getopt
from flask import Flask, request
import requests
import random

app = Flask(__name__)
porta = -1
portb = -1
a = -1
A = -1
B = -1
p = -1
q = -1
shared_key = -1

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/init')
def init():
    global portb, a, A, p, g
    a = random.randint(1, 101)
    print 'a: ' + str(a)
    p = generatePrime()
    print 'p: ' + str(p)
    g = randomPrimRoot(p)
    print 'g: ' + str(g)
    A = (g**a)%p
    print 'A: ' + str(A)
    params = { 'A': A, 'p': p, 'g': g }
    requests.get('http://localhost:%d/exchange/1' % portb, params=params)
    return 'init'

@app.route('/exchange/1')
def exchange1():
    global portb, p, g, a, A, B, shared_key
    a = random.randint(1, 101)
    print 'a: ' + str(a)
    p = int(request.args.get('p'))
    print 'p: ' + str(p)
    g = int(request.args.get('g'))
    print 'g: ' + str(g)
    A = (g**a)%p
    print 'A: ' + str(A)
    B = int(request.args.get('A'))
    print 'B: ' + str(B)
    params = { 'B': A }
    requests.get('http://localhost:%d/exchange/2' % portb, params=params)
    shared_key = (B**a)%p
    print 'shared_key: ' + str(shared_key)
    return 'exchange1'

@app.route('/exchange/2')
def exchange2():
    global B, shared_key
    B = int(request.args.get('B'))
    print 'B: ' + str(B)
    shared_key = (B**a)%p
    print 'shared_key: ' + str(shared_key)
    return 'exchange2'

@app.route('/send_plain_message/<msg>')
def send_plain_message(msg):
    global portb, shared_key
    enc_msg = xor_str(msg, shared_key)
    params = {'enc_msg': enc_msg}
    new_enc_msg = requests.post('http://localhost:%d/receive_secure_message' % portb, params=params).text
    return 'decrypted ack msg: %s' % xor_str(new_enc_msg, shared_key)

@app.route('/receive_secure_message', methods = ['POST'])
def receive_secure_message():
    global shared_key
    enc_msg = request.args.get('enc_msg')
    dec_msg = xor_str(enc_msg, shared_key)
    return xor_str(dec_msg + "ack", shared_key)

def xor_str(msg, key):
    return "".join(unichr(ord(x) ^ key) for x in msg)

def randomPrimRoot(modulo):
    coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}
    return random.choice([g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)
                                                        for powers in range(1, modulo)}])

def gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

def generatePrime():
    primes = [i for i in range(100,1000) if isPrime(i)]
    return random.choice(primes)

def isPrime(n):
    if n==2 or n==3: return True
    if n%2==0 or n<2: return False
    for i in range(3,int(n**0.5)+1,2): # only odd numbers
        if n%i==0:
            return False
    return True

def main(script_name, argv):
    global porta, portb
    try:
        opts, args = getopt.getopt(argv,"",["porta=","portb="])
    except getopt.GetoptError:
        print '%s --porta <porta> --portb <portb>' % script_name
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print '%s --porta <porta> --portb <portb>' % script_name
            sys.exit()
        elif opt == "--porta":
            porta = int(arg)
        elif opt == "--portb":
            portb = int(arg)
    if porta == -1 or portb == -1:
        print '%s --porta <porta> --portb <portb>' % script_name
        sys.exit(2)
    app.run('', porta)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
