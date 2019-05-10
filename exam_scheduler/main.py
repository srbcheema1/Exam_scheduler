#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import os
import sys

from srblib import Colour

from . import __version__, __mod_name__
from .scheduler import Scheduler
from .parser import get_parser
from .configurations import default_output_xlsx_path
from .verifier import Verifier

def main():
    args = get_parser()
    if args.version:
        print(__mod_name__+'=='+__version__)
        sys.exit()

    if args.vr:
        Verifier.verify_room_list(args.vr)
        sys.exit()
    if args.vs:
        Verifier.verify_schedule_list(args.vs)
        sys.exit()
    if args.vt:
        Verifier.verify_teachers_list(args.vt)
        sys.exit()
    if args.vw:
        Verifier.verify_work_ratio(args.vw)
        sys.exit()

    if args.seed <= 0:
        Colour.print('seed value should be a positive integer, got : ' + str(args.seed),Colour.RED)
        sys.exit(1)

    global default_output_xlsx_path
    if args.output: default_output_xlsx_path = args.output

    if args.reserved < 0:
        Colour.print('Reserved number should be a non-negative integer, got : ' + str(args.reserved), Colour.RED)
        sys.exit(1)

    try:
        scheduler = Scheduler(int(args.seed),int(args.reserved))
        if args.debug: scheduler.debug = True
        scheduler._configure_paths() # done manually
        res = scheduler.compileall()
        if not res:
            Colour.print('Error during compilation',Colour.RED)
            print(res)
            sys.exit(1)
        scheduler.schedule(default_output_xlsx_path)
        Colour.print('Output written to : ' + Colour.END + default_output_xlsx_path, Colour.BLUE)
    except KeyboardInterrupt:
        Colour.print('Exiting on KeyboardInterrupt ...',Colour.YELLOW)

if(__name__=="__main__"):
    main()
