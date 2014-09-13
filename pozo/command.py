'''
Created on 21.8.2014

@author: A417280
'''

import record
import broker
import properties
import re
import time

class PozoCmd(object):
    '''
    classdocs
    '''
    sender = 'JARDIN'
    pb = broker.Broker(properties.POZOIP, properties.POZOPORT)

    def __init__(self):
        self.cmd = 'error'
        self.help = 'Command does nothing but returning error,'
        self.pozocode = 'NOTOK'
        self.args = []
        self.cmdrecord = record.Record()
        
    def execute(self, args):
        arg1 = 0
        arg2 = 0
        if len(args) > 1: 
            arg1 = args[1]
        if len(args) > 2:
            arg2 = args[2]
        if self.isVerbose():
            print self.__class__.__name__
        return self.method(arg1, arg2)

    def isVerbose(self):
        return properties.VERBOSE
        
    def print_nice(self):
        print 'now NICE output implemented'
    
    def print_raw(self):
        print 'now RAW output implemented'
        
    def print_json(self):
        print 'not JSON output implemented'    
    
    # creates command strip
    # A:xxxx where A is command code and xxxx is value
    # 
    def create_value_strip(self, type_name, value):
        return "{0}:{1}:".format(properties.pozocode.get(type_name), value)
    
    def create_cmd_strip(self):
        '''
        returns 'C:101'
        '''
        return "{0}:{1}:".format(properties.pozocode.get('COMMAND'),properties.pozocode.get(self.pozocode))

    def sender_strip(self):
        '''
        returns 'S:101'
        '''
        return "{0}:{1}:".format(properties.pozocode.get('SENDER'), properties.pozocode.get(self.sender))

    def error_ok_strip(self):
        '''
        returns 'S:101'
        '''
        return "{0}:{1}:".format(properties.pozocode.get('ERRORCODE'), properties.pozocode.get("OK"))

    
    def create_message(self):
        '''
        returns 'S:102:C:104:E:456'
        '''
        msg = self.sender_strip()
        msg = msg + self.create_cmd_strip()
        msg = msg + self.error_ok_strip()
        if properties.VERBOSE > 0:
            print msg
        return msg
    
    def get_pozocode(self, stringcode):
        return properties.pozocode.get(stringcode)
    
    def method(self, arg1, arg2):
        print "This method should not be called"
        return properties.pozocode.get("NOTOK")
    
    def print_help(self):
        print "{0}: {1}".format(self.cmd, self.help)
        
    def send_msg(self, msg):
        return PozoCmd.pb.send_msg(msg)
        
    def retrieve_reply_body(self, reply ):
        #retrieve message body from the response from Pozo
        pozoid = 'POZO/'
        idx = reply.find(pozoid)
        idx = idx + len(pozoid)
        msg_body = reply[idx:]
        if properties.VERBOSE > 0:
            print msg_body
        return msg_body
   
    '''' 
    def parse_answer(self, answr):
        self.cmdrecord = Record.Record()
        splited = re.split(":", answr)
        if properties.VERBOSE > 0: 
            print splited   
        iscode = False;
        
        for x in splited:
            if (iscode == False):
                code = x
                iscode = True
            else:
                value = x
                iscode = False
                self.cmdrecord.store_code_value(code, value)
    
                if properties.VERBOSE > 0: 
                    print "CODE:{0}:VALUE:{1}".format(code, value)
    
        return self.cmdrecord
   
   '''
   
    def print_result(self, outputtype):    
        if outputtype == properties.pozocode.get('NICE'):
            self.print_nice()
        elif outputtype == properties.pozocode.get('JSON'):
            pass
        else:
            self.print_raw()                

    
    def print_error(self):
        print "errorcode: {0}".format(self.cmdrecord.errorcode)    

       

'''                             
    "ping"
    "freeram"
    "header"
    "settime"
    "gettime"
    "sethigh"
    "setlow"
    "setbinary"
    "get1wnum"
    "read1wnum"
    "read1wtemp"
    "pinstatus"
'''
            
'''
************** COMMANDS *********************
'''



class Freeram(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'freeram'
        self.help = 'Returns free RAM of POZO (ARDUINO) in bytes'
        self.pozocode = 'FREERAM'
        self.delay = 0
          
    def method(self, arg1, arg2):
        msg = self.create_message()       
        answ = PozoCmd.pb.send_record(msg)
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode       
    
    def print_nice(self):
        self.cmdrecord.value1 = int(self.cmdrecord.value1)
        print "POZO free {0:} bytes".format(self.cmdrecord.value1)

    def print_raw(self):
        print int(self.cmdrecord.value1)

class HeaderVersion(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'headerver'
        self.help = 'Returns version of Pozocodes to check compatibility'
        self.pozocode = 'READHEADERVER'
        self.delay = 0
          
    def method(self, arg1, arg2):
        msg = self.create_message()       
        answ = PozoCmd.pb.send_record(msg)
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode       
    
    def print_nice(self):
        self.cmdrecord.value1 = int(self.cmdrecord.value1)
        print "POZO header version {0:}".format(self.cmdrecord.value1)

    def print_raw(self):
        print int(self.cmdrecord.value1)


class GetTime(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'gettime'
        self.help = 'Get POZO system time and date'
        self.pozocode = 'GETTIME'
          
    def method(self, args1, args2):
        msg = self.create_message()       
        answ = PozoCmd.pb.send_record(msg)
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode

    def print_nice(self):
        self.cmdrecord.value1 = float(self.cmdrecord.value1)
        print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(float(self.cmdrecord.value1)))

    def print_raw(self):
        print self.cmdrecord.value1



class Header(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'header'
        self.help = 'Print out header pozo_codes.h for server side C++ code (Arduino)'
        self.pozocode = 'CLIENT'
        self.delay = 0
          
    def method(self, arg1, arg2):
        self.print_raw()
        return properties.pozocode.get("OK")

    def print_define(self, key, value): 
        print "#define {0:<10} {1}".format(key,value)
    
    def print_define_char(self, key, value):
        print "#define {0:<10} \'{1}\'".format(key,value)
    
    def print_define_str(self, key, value):
        print "#define {0:<10} \"{1}\"".format(key,value)
    
    def print_nice(self):
        self.print_raw()

    def print_raw(self):
              
        print("/*")
        print("* properties.h")
        print("*")
        print("* Created on: {0}".format(time.strftime("%d/%m/%Y")))
        print("* Author: Norad Sparta")
        print("*/\n\n")
        print("#ifndef POZOCODES_H_")
        print("#define POZOCODES_H_")
        print("\n")
              
        # UNSORTED: for key, value in properties.pozocode.iteritems():
        for key, value in sorted(properties.pozocode.items()):

            if type(value) is int:
                self.print_define(key, value)
            elif type(value) is long:
                self.print_define(key, value)
            elif type(value) is str:
                if len(value) == 1:
                    self.print_define_char(key, value)
            else:
                self.print_define_str(key, value)
      
        print("\n/* OTHER CONSTANTS */\n")        
        self.print_define("HEADERVERSION", properties.HEADERVERSION)
                          
        print("\n\n#endif /* POZOCODES_H_ */")
        
        
class SetVerbose(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'verbose'
        self.help = 'set VERBOSE mode to value'
        self.pozocode = 'CLIENT'
          
    def method(self, arg1, arg2):
        properties.VERBOSE = int(arg1)
        return properties.pozocode.get("OK")

    def print_nice(self):
        #print "VERBOSE = {0:}".format(properties.VERBOSE)
        pass

    def print_raw(self):
        pass





class Nope(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'nope'
        self.help = 'This function does nothing'
        self.pozocode = 'NOPE'
        
    def execute(self, args):
        return self.pozocode('OK')
    
    def print_nice(self):
        print 'Successfuly done nothing'



class Ping(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'ping'
        self.help = 'Returns response time to Pozo in milliseconds'
        self.pozocode = 'PING'
        self.delay = 0
          
    def method(self, arg1, arg2):
        msg = self.create_message()
        startime = self.millis()
        answ = self.pb.send_record(msg)
        print answ
        self.delay = self.millis() - startime
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode
    
    def print_nice(self):
        print "Reply from POZO in {:0}ms".format(self.delay)

    def print_raw(self):
        print self.delay
           
    def millis(self):
        return int(round(time.time() * 1000))
    
    

class PinStatus(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)  #call super constructor
        self.cmd = 'pinstatus'
        self.help = 'Get status of relays in binary form  #1 - #8'
        self.pozocode = 'PINSTATUS'
          
    def method(self, args1, args2):
        if properties.VERBOSE > 0:
            print "calling {0}.method".format(self.cmd)       
        msg = self.create_message()
        answ = PozoCmd.pb.send_record(msg)
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode

    def print_nice(self):
        self.cmdrecord.value1 = int(self.cmdrecord.value1)
        print "Pins status: {0:07b}    Remaining: {1}s".format(int(self.cmdrecord.value1), int(self.cmdrecord.value2))
    
    def print_raw(self):
        self.cmdrecord.value1 = int(self.cmdrecord.value1)
        print "{0};{1};".formatself.cmdrecord.value1, self.cmdrecord.value2
        
    def get_byte(self):
        return self.cmdrecord.value1
    
    def get_remaining(self):
        return self.cmdrecord.value2


class Read1wAddr(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'read1waddr'
        self.help = 'get number of connected 1-wire devices'
        self.pozocode = 'READ1WADDR'
          
    def method(self, args1, args2):
        msg = self.create_message()
        msg = msg + self.cre_long_strip(args1)
        answ = self.send_msg(msg)
        answ = self.retrieve_reply_body( answ )
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode


    def print_nice(self):
        print self.cmdrecord.value1

    def print_raw(self):
        print self.cmdrecord.value1
        
        

class Read1wNum(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'read1wnum'
        self.help = 'get number of connected 1-wire devices'
        self.pozocode = 'READ1WNUM'
          
    def method(self, args1, args2):
        msg = self.create_message()
        
        answ = self.send_msg(msg)
        answ = self.retrieve_reply_body( answ )
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode


    def print_nice(self):
        print self.cmdrecord.value1

    def print_raw(self):
        print self.cmdrecord.value1 

        
class Get1wNum(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'get1wnum'
        self.help = 'get number of connected 1-wire devices'
        self.pozocode = 'GET1WNUM'
          
    def method(self, args1, args2):
        msg = self.create_message()       
        answ = self.send_msg(msg)
        answ = self.retrieve_reply_body( answ )
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode


    def print_nice(self):
        print self.cmdrecord.value1

    def print_raw(self):
        print self.cmdrecord.value1 

        

class Read1wTemp(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'read1wtemp'
        self.help = 'get number of connected 1-wire devices'
        self.pozocode = 'READ1WTEMP'
          
    def method(self, args1, args2):
        msg = self.create_message()
        msg = msg + self.create_value_strip('LONG', args1)
        answ = self.send_msg(msg)
        answ = self.retrieve_reply_body( answ )
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode

    def print_nice(self):
        print float(self.cmdrecord.value1)
        #print float(self.cmdrecord.value2)

    def print_raw(self):
        print float(self.cmdrecord.value1)                      
       
    

class SetBinary(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'setbinary'
        self.help = 'Set 8 relay outputs according the bits in the 8bit binary number. Second argument is the period of seconds.  '
        self.pozocode = 'SETBINARY'
        
    def method(self, arg1, arg2):
        msg = self.create_message()
        msg = msg + self.create_value_strip('BYTE', int(arg1,2))
        msg = msg + self.create_value_strip('LONG', arg2)
        
        answ = self.pb.send_msg( msg )
        answ = self.pb.retrieve_reply_body( answ )
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode          
    
    def print_nice(self):
        print 'set'
        
    def print_raw(self):
        pass

 
class SetTime(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'settime'
        self.help = 'Set POZO system time and date'
        self.pozocode = 'SET_TIME'
        self.timeset = int(time.time())
          
    def method(self, arg1, arg2):
        msg = self.create_message()
        self.timeset = int(time.time())        
        msg = msg + self.create_value_strip('TIMEDATE', self.timeset)
        answ = self.pb.send_record(msg)
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode

    def print_nice(self):
        print "Time set"

    def print_raw(self):
        print self.cmdrecord.value1       
        

class Uptime(PozoCmd):
    
    def __init__(self):
        PozoCmd.__init__(self)
        self.cmd = 'uptime'
        self.help = 'Tell how long the Arduino has been running.'
        self.pozocode = 'UPTIME'
        self.delay = 0
          
    def method(self, arg1, arg2):
        msg = self.create_message()       
        answ = PozoCmd.pb.send_record(msg)
        self.cmdrecord.parse_answer(answ)
        return self.cmdrecord.errorcode       
    
    def print_nice(self):
        self.cmdrecord.value1 = int(self.cmdrecord.value1)
        print "POZO uptime {0:} ".format(self.cmdrecord.value1)

    def print_raw(self):
        print int(self.cmdrecord.value1)        
        
        
'''
    ********** Command LIST *********************
'''     
        
        
        
        
        
        
class CmdList(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        '''                             
        "ping"
        "freeram"
        "header"
        "settime"
        "gettime"
        "sethigh"
        "setlow"
        "setbinary"
        "get1wnum"
        "read1wnum"
        "read1wtemp"
        "pinstatus"
        '''
        
        self.cmdlist = []
        self.cmdlist.append(PozoCmd())
        self.cmdlist.append(Freeram())
        self.cmdlist.append(GetTime())
        self.cmdlist.append(Header())
        self.cmdlist.append(Nope())
        self.cmdlist.append(Ping())
        self.cmdlist.append(PinStatus())
        self.cmdlist.append(Read1wNum())
        self.cmdlist.append(Read1wAddr())
        self.cmdlist.append(Read1wTemp())
        self.cmdlist.append(SetBinary())
        self.cmdlist.append(SetTime())
        self.cmdlist.append(HeaderVersion())
        self.cmdlist.append(SetVerbose())
        self.cmdlist.append(Get1wNum())
        self.cmdlist.append(Uptime())

        
    def find_entry(self, cmdstring):
        found = False
        for cmdentry in self.cmdlist:
            if (cmdentry.cmd == cmdstring):
                found = True
                break
        if found == False:
            cmdentry = self.cmdlist[0]
        return cmdentry
     
    def print_listOfCommands(self):
        for cmdentry in self.cmdlist:
            print cmdentry.cmd
    
    def execute(self, command):
        if properties.VERBOSE > 0:
            print "CmdList: Execute command"
        margs = re.split(" ", command)
        acmd = self.find_entry(margs[0])
        if acmd is self.cmdlist[0]:
            print "unknown command"
        else:
            result = int(acmd.execute(margs))
            if properties.VERBOSE > 0:
                print "Execute result = {0}".format(result)
            if int(result) > 0:
                acmd.print_error()
            else:
                acmd.print_result(properties.OUTPUTTYPE)

            

'''
   VARIABLES
'''
CMDLIST = CmdList()

        