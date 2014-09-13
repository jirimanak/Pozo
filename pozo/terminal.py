'''
Created on 22.8.2014
@author: A417280
'''

import Queue
import os
import command


history = Queue.LifoQueue(20)

prompt = 'pozo> '


import cmd

class ShellPrompt(cmd.Cmd):
    """Simple command processor example."""

    prompt = 'prompt: '
    intro = "Simple command processor example."

    doc_header = 'doc_header'
    misc_header = 'misc_header'
    undoc_header = 'undoc_header'
    
    ruler = '-'
    
    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + '> '

    def do_EOF(self, line):
        return True

    def do_shell(self, line):
        "Run a shell command"
        print "running shell command:", line
        output = os.popen(line).read()
        print output
        self.last_output = output
   
    def do_echo(self, line):
        "Print the input, replacing '$out' with the output of the last shell command"
        # Obviously not robust
        print line.replace('$out', self.last_output)
        
    def default(self, line):
        command.CMDLIST.execute(line)
        
   
        
def interactive():
    ShellPrompt().cmdloop()

    
def old_interactive():    
    ''' control interactive command line mode '''
    goahead = True
    while(goahead):    
        ''' read user input ''' 
        user_input = raw_input(prompt)
        
        if ("last" in user_input):
            ''' if command is 'last' get last command from the queue '''
            user_input = history.get();
            ''' print out last command on the prompt '''
            print("{0}{1}", prompt, user_input )
        else:
            ''' ... else store command for history '''
            history.put(user_input)

        arg = user_input.split()

        
        if("quit" in arg[0]):
            print('bye!')
            goahead = False;
            
        elif("connect" in arg[0]):
            ''' second argument can be ip address '''
            if (len(arg)>1):
                ''' s = open_connection(arg[1]) '''
            else:
                ''' s = open_connection() '''
        else:
            pass 
            # goahead = execute_command(arg)