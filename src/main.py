import sys
import subprocess
import argparse


def parse_args(args):
    arg_parser = argparse.ArgumentParser(
        description='Compile neolang language to x86 assembly')
    arg_parser.add_argument('-t', '--test', action='store_true',
                            help='Runs unit tests')
    return arg_parser.parse_args(args)


if __name__ == '__main__':
    parsed_args = parse_args(sys.argv[1:])
    if parsed_args.test:
        exit(subprocess.call(
            [sys.executable, '-m', 'unittest', 'discover', 'tests/']))
