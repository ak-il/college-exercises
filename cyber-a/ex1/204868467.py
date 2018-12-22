#!/usr/bin/python

import sys, getopt
import thread
import traceback
import logging
from flask import Flask

app = Flask(__name__)
porta = -1
portb = -1

@app.route('/init')
def init():
    return 'init'

@app.route('/exchange/1')
def exchange1():
    p = request.args.get('p')
    g = request.args.get('g')
    A = request.args.get('A')
    return 'exchange1'

@app.route('/exchange/2')
def exchange2():
    B = request.args.get('B')
    return 'exchange2'

@app.route('/send_plain_message')
def send_plain_message():
    return 'send plain msg'

@app.route('/receive_secure_message', methods = ['POST'])
def receive_secure_message():
    return 'receive_secure_message'

def start_server(app, port):
    app.run('', port)

def init_msg():
    return

def main(script_name, argv):
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
            porta = arg
        elif opt == "--portb":
            portb = arg
    if porta == -1 or portb == -1:
        print '%s --porta <porta> --portb <portb>' % script_name
        sys.exit(2)
    try:
        thread.start_new_thread(start_server, (app, porta, ))
        thread.start_new_thread(start_server, (app, portb, ))
    except Exception as e:
        print 'Error: unable to start thread'
        logging.error(traceback.format_exc())
        sys.exit(2)
    init_msg()

    while 1:
       pass

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
