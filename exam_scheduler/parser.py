import os
import sys

from srblib import show_dependency_error_and_exit

try:
    import argparse
    from argcomplete import autocomplete
except:
    show_dependency_error_and_exit()

def get_parser():
    def _is_valid_file(parser, arg):
        if not os.path.isfile(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return arg

    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--version",
                        action='store_true',
                        help='Display version number')
    parser.add_argument("-r","--reserved",
                        default=0,
                        type=int,
                        help='reserved number of seats for each session')
    parser.add_argument("-o","--output",
                        # type=lambda x: _is_valid_file(parser,x),
                        type=str,
                        help='Output file name, default output.xlsx')
    autocomplete(parser)
    return parser.parse_args()
