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
    parser.add_argument("-o","--output",
                        # type=lambda x: _is_valid_file(parser,x),
                        type=str,
                        help='Output file name, default output.xlsx')
    parser.add_argument("-s","--seed",
                        default=5,
                        type=int,
                        help='seed value for randomness')
    parser.add_argument("-r","--reserved",
                        default=0,
                        type=int,
                        help='reserved number of seats for each session')
    parser.add_argument("-d","--debug",
                        action='store_true',
                        help='print debug info')

    verify_parser = parser.add_mutually_exclusive_group()
    verify_parser.add_argument("-vr",
                        type=lambda x: _is_valid_file(parser,x),
                        help='verify room_list file')
    verify_parser.add_argument("-vs",
                        type=lambda x: _is_valid_file(parser,x),
                        help='verify schedule_list file')
    verify_parser.add_argument("-vt",
                        type=lambda x: _is_valid_file(parser,x),
                        help='verify teachers_list file')
    verify_parser.add_argument("-vw",
                        type=lambda x: _is_valid_file(parser,x),
                        help='verify work_ratio file')

    autocomplete(parser)
    return parser.parse_args()
