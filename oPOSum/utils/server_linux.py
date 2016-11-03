#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import json
import logging 
import logging.handlers as handlers
#import win32print
import time
import traceback
import subprocess


LOG_FILENAME = '/home/balco/projects/oposum/log/server.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = handlers.TimedRotatingFileHandler(LOG_FILENAME, when='D', interval=1, backupCount=5)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
USER_SERIAL = False
SERIALPORT = '/dev/ttyACM0'
BAUDRATE = 115200
 
class LocalData(object):
    records = {}

class LocalUtil(object):
    def __init__(self):
        self.const = {
            '{{LF}}': '\x0a',
            '{{CR}}': '\x0d',
            '{{TAB}}': '\t',
            '{{PAPERCUT}}': '\x1d\x56\x01',
            '{{BOLDOFF}}': '\x1b\x45\x00',
            '{{BOLDON}}': '\x1b\x45\x01',
        }
    def get_printers(self):
        printers = win32print.EnumPrinters(2)
        return printers
    
    def get_zebra_printer(self):
        printers = self.get_printers()
        for printer in printers:
            if printer[2].lower() == 'zebra':
                return printer
        return None

    def send_to_zebra(self, data):
        print_str=''
        for word in data.split():
            if word in self.const:
                print_str += self.const[word]
            else:
                print_str += word + ' '
        if not USER_SERIAL:
            p = subprocess.Popen(['lpr', '-P', 'zebra'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            p.communicate(input=print_str)
        else:
            import serial
            ser = serial.Serial(SERIALPORT, BAUDRATE)
            ser.bytesize = serial.EIGHTBITS
            ser.parity = serial.PARITY_NONE
            ser.stopbits = serial.STOPBITS_ONE
            try:
                ser.open()
                if ser.isOpen():
                    ser.write(print_str)
            except Exception as err:
                logger.debug('Error printing to serial: ')
                logger.debug(err)
        return
 
class HTTPRequestHandler(BaseHTTPRequestHandler):
 
    def do_POST(self):
        res = "";
        if None != re.search('/api/v1/print', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            length = int(self.headers.getheader('content-length'))
            try:
                data = self.rfile.read(length)
                lu = LocalUtil()
                #printer = lu.get_zebra_printer()
                #data = json.loads(data)
                #data['data'] = data['data'].encode('utf-8').decode('latin-1')
                lu.send_to_zebra(data)
                res = '{"status": 200, "message": "ok"}'
                self.send_response(200)
            except:
                logger.error('error : \n{0}'.format(traceback.format_exc()));
                res = '{"status": 500, "message": "' + traceback.format_exc() + '"}'
                self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write('jsonp(' + res + ')')
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return
 
    def do_GET(self):
        if None != re.search('/api/v1/get-printers', self.path):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write('{"printers": ["printer1", "printer2"]}')
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
     allow_reuse_address = True
 
     def shutdown(self):
         self.socket.close()
         HTTPServer.shutdown(self)
         self.server_close()
 
class SimpleHttpServer():
     def __init__(self, ip, port):
         self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
 
     def start(self):
         self.server_thread = threading.Thread(target=self.server.serve_forever)
         self.server_thread.daemon = True
         self.server_thread.start()
 
     def waitForThread(self):
         self.server_thread.join()
 
     def addRecord(self, recordID, jsonEncodedRecord):
         LocalData.records[recordID] = jsonEncodedRecord
 
     def stop(self):
         self.server.shutdown()
         self.waitForThread()
 
if __name__=='__main__':

     server = SimpleHttpServer('0.0.0.0', 9099)
     print 'HTTP Server Running...........111'
     server.start()
     server.waitForThread()

