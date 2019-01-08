#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys

from srblib import Colour

from . import __version__, __mod_name__
from .scheduler import Scheduler
from .parser import get_parser
from .configurations import default_output_xlsx_path

def main():
    args = get_parser()
    if args.version:
        print(__mod_name__+'=='+__version__)
        sys.exit()

    global default_output_xlsx_path
    if args.output: default_output_xlsx_path = args.output

    try:
        Scheduler().schedule(default_output_xlsx_path)
        Colour.print('Output written to : ' + Colour.END + default_output_xlsx_path, Colour.BLUE)
    except KeyboardInterrupt:
        Colour.print('Exiting on KeyboardInterrupt ...',Colour.YELLOW)

if(__name__=="__main__"):
    main()
