#!/usr/local/bin/python2.7
# encoding: utf-8
'''
src.pozo_client -- shortdesc

src.pozo_client is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2014 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
#import pozo_term
import terminal
import properties
import command

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 5.0
__date__ = '2015-06-03'
__updated__ = '2015-06-03'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2014 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--VERBOSE", dest="VERBOSE", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-I", "--interactive", dest="interactive", action="store_true", help="start interactive mode" )
        parser.add_argument("-H", "--header", dest="header", action="store_true", help="print out header file" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-o', '--output', dest='output', action='store', help="specify out file, valid only with option -H or --header")
        parser.add_argument('-i', '--input', dest='input', action='store', help="specify path and name of file which consist of commands  ")
        #parser.add_argument('-c', '--command', dest='command', action='store', help="execute one command with max two arguments")
        parser.add_argument('-a', '--address', dest='address', action='store', help="IP address of POZO server")
        parser.add_argument('-p', '--port', dest='port', action='store', help="listening port of POZO server")
        # positional argument - optional 
        parser.add_argument('command', action='store', nargs='?', default="", help = 'command string(s)')
        parser.add_argument('cmd_value', action='store', nargs='?', default="", help = 'command string(s)')
        parser.add_argument('cmd_period', action='store', nargs='?', default="", help = 'command string(s)')
       

        #parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')

        # Process arguments
        args = parser.parse_args()
        
        properties.VERBOSE = args.VERBOSE
        properties.POZOIP = args.address
        properties.POZOPORT = args.port
        
        #props = properties.Properties()
                          
        if args.header == True:
            cmdentry = command.CMDLIST.find_entry("header")
            cmdentry.print_raw();
            return 0
        
        if args.interactive == True:
            result = terminal.interactive();
            return result
        else:
            if properties.VERBOSE > 0:
                print 'ARGS command: {0}'.format(args.command)
            if (args.command):
                if (args.cmd_value):
                    result = command.CMDLIST.execute_cmdline(args.command, args.cmd_value, args.cmd_period)
                    if properties.VERBOSE > 0:
                        print 'ARGS: args.command{0}'.format(args)
                else:
                    result = command.CMDLIST.execute(args.command)
 
                return result
        return 0
    
        
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'src.pozo_client_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())