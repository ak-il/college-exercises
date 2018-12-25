#!/usr/bin/python

import sys, getopt
import thread
import traceback
import logging
from flask import Flask
import requests

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
porta = -1
portb = -1

@app.route('/init')
def init():
    # TODO generate these
    session['A'] = 1
    session['p'] = 1
    session['g'] = 1
    if porta in request.host:
        requests.get('localhost:%d/exchange/1?p=%d&g=%d&A=%d' % (session['p'],
                                                                session['g'],
                                                                session['A']))
    return 'init'

@app.route('/exchange/1')
def exchange1():
    session['p'] = request.args.get('p')
    session['g'] = request.args.get('g')
    session['B'] = request.args.get('A')
    # TODO generate this
    session['B'] = 1
    requests.get('localhost:%d/exchange/2?B=%d' % session['A'])
    # TODO generate shared key
    return 'exchange1'

@app.route('/exchange/2')
def exchange2():
    session['B'] = request.args.get('B')
    # TODO generate shared key
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
    requests.get('localhost:%d/init' % porta)
    requests.get('localhost:%d/send_plain_message' % porta)
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
