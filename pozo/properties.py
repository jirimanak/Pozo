'''
Created on 9.6.2014

@author: A417280

'''

'''
 
 !!!!   CHANGE HEADERVERSION after changing values in pozocode dictionary !!!!!!!!!!!!!
 
'''

pozocode = {
            
# 000 - 020 error codes    
  'NOTOK' : 1,
  'OK': 0,
  'BADFORMAT': 2, 
  'BADTYPE': 3, 
  'OUTOFRANGE': 4, 

  'NULLPTR': 25,

# 021 - 050  

# 031 - 040  value types
  'INTEGER': 'I',
  'LONG': 'L',
  'DOUBLE': 'D',
  'FLOAT': 'F',
  'TIMEDATE': 'T',
  'NOTYPE':'N',
  'ERRORCODE':'E',
  'SENDER':'S',
  'COMMAND':'C',
  'BYTE':'B',
  'STRVALUE':'R',
  
  
# 100 - 199 commands

  'NOPE':100,      # no command - do nothing
  'CLIENT':101,     # client side only command: will not be transfered to the server 
  'SET_TIME':102,  # set time from seconds after epoch
  'PING':103,      # get response if alive
  'PONG':104,      # inform POZO ping response received successfully
  'FREERAM':105,    # get free ram of POZO
  'GETTIME':106,    # get system time of POZO
  
  'SETHIGH':107,    # set pin number N high
  'SETLOW':108,     # set pin number N low
  'GETPIN':109,     # get status of pin
  'SETBINARY':110,  # set all pins according BYTE  0 = low 1 = high
  'PINSTATUS':111,  # get pin status and remaining time, zero remaining time mean infinite 

  'GET1WNUM':120,   # get number of devices
  'READ1WNUM':121,  # get number of devices
  'READ1WADDR':122, # read address of 1 wire device
  'READ1WTEMP':123, # read temperature of 1 wire device
  'READHEADERVER':124, # return version of header - to ensure codes compatibility         
  
  
# 200 - 299 response codes

# 500 - 599 sender codes
  'OTHER':500,
  'JARDIN':501,
  'POZO':502,
  'PUENTE':503,
  'TESTSERVER':504,
  
 # 600-610 output format
  'NICE': 600,   # descriptive output 
  'RAW':601,  # shortest possible response - mostly only numbers
  'JSON':602,  # output in serialize JSON string
  }



''' 
!!!!   CHANGE HEADERVERSION after changing values in pozocode dictionary !!!!!
'''

HEADERVERSION = 101

VERBOSE = 1
# POZOIP = '127.0.0.1'
# POZOPORT = '8888'
POZOIP = '192.168.0.15'
POZOPORT = '80'
OUTPUTTYPE = 600


'''
module_name, package_name, ClassName, method_name, ExceptionName, 
function_name, GLOBAL_CONSTANT_NAME, 
global_var_name, instance_var_name, 
function_parameter_name, local_var_name.
'''

class Properties(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''

