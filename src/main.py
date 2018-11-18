import sys
import subprocess
import argparse

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Compile neolang language to x86 assembly')
    if 'test' in sys.argv:
        exit(subprocess.call(
            [sys.executable, '-m', 'unittest', 'discover', 'tests/']))
