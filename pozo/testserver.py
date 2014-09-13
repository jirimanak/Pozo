'''
Created on 20.8.2014

@author: A417280
'''

#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep


import record
import properties
import time

PORT_NUMBER = 8888
VERBOSE = 1

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):


    def execute_command(self, command):
        pc = record.Record()
        if VERBOSE > 0:
            print command
        pc.parse_answer(command)
        if pc.command == properties.pozocode.get('PING'):
            answ = "S:504:C:{0}:E:0".format(pc.command)
        elif pc.command == properties.pozocode.get('GETTIME'):
            answ = "S:504:C:{0}:L:{1}:E:0".format(pc.command, int(time.time()))
        elif pc.command == properties.pozocode.get('PINSTATUS'):
            answ = "S:504:C:{0}:B:{1}:L:{2}:E:0".format(pc.command, 182,640)
        else:
            answ = "S:504:C:100:E:0"
            
        if VERBOSE > 0:
            print "ANSWER: {0}".format(answ)
        return answ    
    
    
    #Handler for the GET requests
    def do_GET(self):
        
        if VERBOSE > 0:
            print "PATH: {0}".format(self.path)
        
        if self.path.endswith("favicon.ico"):
            # browser requested icon
            try:
            #Open the static file requested and send it
                mimetype = "image/x-icon"
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
            
        elif self.path.startswith("/S:"):
            # POZO COMMAND
            print "RECIEVED: {0}".format(self.path)
            answ = self.execute_command(self.path[1:])
            answ = "POZO/" + answ
            try:
                #Open the static file requested and send it
                mimetype='text/html'
                self.send_response(200,answ)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                print "SENT: {0}".format(answ)
                #self.wfile.write(answ)
                self.wfile.write("""<HTML><HEAD><TITLE>Sample Page</TITLE></HEAD>
        <BODY>This is a sample HTML page.</BODY></HTML>""")

            except IOError:
                self.send_error(404,'File Not Found: %s' % self.path)
        else:
            answ = "<HTML>" + self.path[1:] + "</HTML>" 


            

def main():
    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Started http server on port ' , PORT_NUMBER
        
        #Wait forever for incoming htto requests
        server.serve_forever()
    
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()
    

if __name__ == '__main__':
    main()