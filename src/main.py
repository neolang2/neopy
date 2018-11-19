import sys
import unittest.mock
import subprocess
import argparse

from compiler import handler


def parse_args(args):
    arg_parser = argparse.ArgumentParser(
        description='Compile neolang language to x86 assembly')
    arg_parser.add_argument(
        'files', help='Compiles all files', nargs='+', type=argparse.FileType('r'))
    return arg_parser.parse_args(args)


if __name__ == '__main__':
    parsed_args = parse_args(sys.argv[1:])
    handler.compile_files(parsed_args)
