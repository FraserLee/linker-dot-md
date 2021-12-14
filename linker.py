#!/usr/bin/python3
import re
import sys
import os

def link(file_path, depth=3, pattern='^!r(?:eq(?:uire)?)?\(([\w\-. \/]+)\)$'):
    """
    Input: the path to a file
    Output: the resulting file as a list of strings

    The default pattern matches `!require(...)` (or `!req(...)` or `!r(...)`),
    with '...' a path relative to the source file. For custom patterns, just
    ensure the first capture group is the path to the file you want linked.
    """
    pattern = re.compile(pattern)
    lines = []

    # save the current working directory, then cd to the file before opening
    # so that relative paths are resolved correctly.
    cwd = os.getcwd()

    try:
        if len(file_dir := os.path.dirname(file_path)) > 0: os.chdir(file_dir)
        file = open(os.path.basename(file_path), 'r')
    except OSError: # (either dir or file not found)
        lines = [f'Unable to link file \'{file}\'\n']
    else:
        with file:
            for line in file.readlines():
                if depth > 0 and (match:=pattern.match(line)):
                    lines += link(match.group(1), depth-1) # recurse
                else: lines.append(line)

    # if the last line doesn't end with a newline, append one
    if lines[-1][-1] != '\n': lines[-1] += '\n'

    os.chdir(cwd) # cd back to the start
    return lines


# <CLI INVOCATION>
if __name__ == '__main__':

    result = link(sys.argv[1])

    if len(sys.argv) == 3: # output to file
        with open(sys.argv[2], 'w') as dest:
            for line in result:
                dest.write(line)

    else:                  # output to stdout
        for line in result:
            print(line, end='')
# </CLI INVOCATION>
