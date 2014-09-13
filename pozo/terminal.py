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

    def do_exit(self, line):
        return True

    def do_quit(self, line):
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
