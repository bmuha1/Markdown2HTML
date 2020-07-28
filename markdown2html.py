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

    with open(sys.argv[1]) as r:
        with open(sys.argv[2], 'w') as w:
            unordered_start = False
            for line in r:
                headings = line.lstrip('#')
                heading_count = len(line) - len(headings)
                unordered = line.lstrip('-')
                unordered_count = len(line) - len(unordered)
                if 1 <= heading_count <= 6:
                    line = '<h{}>'.format(
                        heading_count) + headings.strip() + '</h{}>\n'.format(
                        heading_count)
                if unordered_count:
                    if not unordered_start:
                        w.write('<ul>\n')
                        unordered_start = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if unordered_start and not unordered_count:
                    w.write('</ul>\n')
                    unordered_start = False
                w.write(line)
            if unordered_start:
                w.write('</ul>\n')

    exit(0)
