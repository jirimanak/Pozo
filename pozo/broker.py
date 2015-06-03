'''
..reated on 22.8.2014.

@author: A417280
'''


import socket
import sys

import properties

class Broker:
    '''
    classdocs
    '''

    def __init__(self, ipaddr, port = 8888):
        '''
        Constructor
        '''
        self.host = ipaddr
        self.port = int(port)
        self.ipaddr = ipaddr   

        
        
    def open_connection_byhostname(self):

        #create an INET, STREAMing socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'ERROR: Failed to create socket'
            sys.exit()
         
        if properties.VERBOSE > 0:
            print 'Socket Created'
      
        try:
            remote_ip = socket.gethostbyname( self.host )
     
        except socket.gaierror:
            #could not resolve
            print 'ERROR Hostname could not be resolved. Exiting'
            sys.exit()
        #Connect to remote server
#        self.s.connect((remote_ip , self.port))
        self.s.connect((remote_ip , self.port))
     
        if properties.VERBOSE > 0:
            print 'Socket Connected to ' + self.host + ' on ip ' + remote_ip
            
        return self.s


    def open_connection(self):

        #create an INET, STREAMing socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)        
            print 'ERROR: Failed to create socket'
            sys.exit()
         
        if properties.VERBOSE > 0:
            print 'Socket Created'
      
        try:
            if properties.VERBOSE > 0:
                print 'Before socket.create_connection((self.ipaddr , self.port), 1)'
                print "IP:{0} PORT:{1}".format(self.ipaddr , self.port)
                
            socket.create_connection((self.ipaddr , self.port), 1)
        except socket.error as e:
            print 'ERROR: client {0}:{1} not found'.format(self.ipaddr, self.port)
            print "I/O error({0}): {1}".format(e.errno, e.strerror)     
            sys.exit()
            
     
        if properties.VERBOSE > 0:
            print 'Socket Connected to ' + self.host + ' on ip ' + self.ipaddr
            
        return self.s


        
    def send_msg(self,  msg ):       
        s = self.open_connection_byhostname()        
        #Send some data to remote server
        message = "GET " + "/" + msg + " HTTP/1.1\r\n\r\n"
        if properties.VERBOSE > 1:
            print "Message: {0}".format(message)
        try :
            #Set the whole string
            if properties.VERBOSE > 0:
                print 'Before s.sendall(message)'
     
    
            s.sendall(message)
        except socket.error as e:
            #Send failed
            print 'ERROR: Send failed'
            print "I/O error({0}): {1}".format(e.errno, e.strerror)            
            sys.exit()
        if properties.VERBOSE > 0:
            print 'Message send successfully'
     
        #Now receive data
        x = 100;
        while (x > 0):
            reply = s.recv(4096)
            if (len(reply) > 0):
                break;
            x -= 1
        
        if properties.VERBOSE > 0:
            print "X={0}".format(x)
    
        s.close()
                        
        return reply
    
    def retrieve_reply_body(self, reply ):
        #retrieve message body from the response from Pozo
        pozoid = 'POZO/'
        idx = reply.find(pozoid)
        idx = idx + len(pozoid)
        msg_body = reply[idx:]
        if properties.VERBOSE > 0:
            print "Record recieved: {0}".format(msg_body)
        return msg_body
    
    
    def send_record(self, qwst):
        reply = self.send_msg(qwst)
        answ = self.retrieve_reply_body(reply)
        return answ
        