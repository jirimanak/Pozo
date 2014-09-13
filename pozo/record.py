'''
Created on 9.6.2014

@author: A417280
'''

import properties
import re

class Record(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.sender = 501
        self.errorcode = 0
        self.command = 100
        self.value1 = 0
        self.value2 = 0
        self.numofvalues = 0
        self.timedate = 0

    # creates command strip
    # A[xxxx] where A is command code
    # 
    def cre_value_strip(self, cmd_name, value):
        return "{0}[{1}]".format(properties.pozocode.get(cmd_name),value)

    def cre_long_strip(self, value):
        return "{0}[{1}]".format(properties.pozocode.get('LONG'),value)

    def cre_byte_strip(self, value):
        return "{0}[{1}]".format(properties.pozocode.get('BYTE'),value)

    def cre_double_strip(self, value):
        return "{0}[{1}]".format(properties.pozocode.get('DOUBLE'),value)

    def cre_timedate_strip(self, value):
        return "{0}[{1}]".format(properties.pozocode.get('TIMEDATE'),value)

    def cre_cmd_strip(self, cmd_name, value_name):
        return "{0}[{1}]".format(properties.pozocode.get(cmd_name), properties.pozocode.get(value_name))

    def store_value(self,value):
        if (self.numofvalues == 0):
            self.value1 = value
            self.numofvalues = self.numofvalues + 1
        if (self.numofvalues == 1):
            self.value2 = value
            self.numofvalues = self.numofvalues + 1
        if properties.VERBOSE > 0:
            print self.numofvalues
            print self.value1
            print self.value2

    def store_code_value(self, code, value):
        if (code == properties.pozocode.get('SENDER')):
            self.sender = value
        elif (code == properties.pozocode.get('ERRORCODE')):
            self.errorcode = value        
        elif (code == properties.pozocode.get('COMMAND')):
            self.command = int(value) 
        elif (code == properties.pozocode.get('INTEGER')):
            self.store_value(int(value))        
        elif (code == properties.pozocode.get('LONG')):
            self.store_value(int(value))        
        elif (code == properties.pozocode.get('FLOAT')):
            self.store_value(float(value))        
        elif (code == properties.pozocode.get('DOUBLE')):
            self.store_value(float(value))
        elif (code == properties.pozocode.get('TIME')):
            self.timedate = long(value) 
        elif (code == properties.pozocode.get('BYTE')):
            self.store_value(int(value))
        elif (code == properties.pozocode.get('STRVALUE')):
            self.store_value(value)
                           
    def reset_values(self):
        self.errorcode = 0
        self.command = 100
        self.value1 = 0
        self.value2 = 0
        self.numofvalues = 0
        self.timedate = 0       
                
    def parse_answer(self, answr):
        self.reset_values()
        if properties.VERBOSE > 0:
            print answr
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
                self.store_code_value(code, value)
                if properties.VERBOSE > 0: 
                    print "CODE:{0}: VALUE:{1}".format(code, value)   
        return self
