#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys

from srblib import show_dependency_error_and_exit

try:
    import argparse
    from argcomplete import autocomplete
except:
    raise # till next release of srblib
    show_dependency_error_and_exit()

from . import __version__, __mod_name__

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--version",action='store_true',help='Display version number')
    parser.add_argument("roll",nargs='?',help="your roll number")

    autocomplete(parser)
    return parser.parse_args()

def main():
    args = get_parser()

    if(args.version):
        print(__mod_name__+'=='+__version__)
        sys.exit()

    try:
        pass
    except KeyboardInterrupt:
        Colour.print('Exiting on KeyboardInterrupt ...',Colour.YELLOW)

if(__name__=="__main__"):
    main()
