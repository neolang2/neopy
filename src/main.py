import sys
import unittest.mock
import subprocess
import argparse

from compiler import handler


def parse_args(args):
    arg_parser = argparse.ArgumentParser(
        description='Compile neolang language to x86 assembly')
    return arg_parser.parse_args(args)


if __name__ == '__main__':
    parsed_args = parse_args(sys.argv[1:])
