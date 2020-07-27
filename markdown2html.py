#!/usr/bin/python3
'''
Take 2 strings as arguments.
The first is the name of the Markdown file.
The second is the output file name.
'''

import sys
import os.path

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)
    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)
    exit(0)
