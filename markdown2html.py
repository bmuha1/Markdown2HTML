#!/usr/bin/python3
'''
Take 2 strings as arguments.
The first is the name of the Markdown file.
The second is the output file name.
'''

import sys
import os.path
import re
import hashlib

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
            unordered_start, ordered_start, paragraph = False, False, False
            for line in r:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md5_inside[0].encode()).hexdigest())

                remove_c = re.findall(r'\(\(.+?\)\)', line)
                if remove_c:
                    line = line.replace('((', '')
                    line = line.replace('))', '')
                    line = ''.join(c for c in line if c not in 'Cc') + '\n'

                length = len(line)
                headings = line.lstrip('#')
                heading_count = length - len(headings)
                unordered = line.lstrip('-')
                unordered_count = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_count = length - len(ordered)

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

                if ordered_count:
                    if not ordered_start:
                        w.write('<ol>\n')
                        ordered_start = True
                    line = '<li>' + ordered.strip() + '</li>\n'
                if ordered_start and not ordered_count:
                    w.write('</ol>\n')
                    ordered_start = False

                if not (heading_count or unordered_start or ordered_start):
                    if not paragraph and length > 1:
                        w.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        w.write('<br/>\n')
                    elif paragraph:
                        w.write('</p>\n')
                        paragraph = False
                if length > 1:
                    w.write(line)

            if unordered_start:
                w.write('</ul>\n')
            if ordered_start:
                w.write('</ol>\n')
            if paragraph:
                w.write('</p>\n')

    exit(0)
