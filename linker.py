#!/usr/bin/python3
import re
import sys
import os
# <REGEX DEFINITIONS>
# identifying the start and end of code-blocks
block_start   = re.compile("^```(python|c|rust|bash|cpp|c\+\+|go|js|javascript|lua)#run( *#\w*( *= *[\w.]*)?)*$")
block_end     = re.compile("^```$")

block_unboxed = re.compile(".*#unboxed")
block_new     = re.compile(".*#new")
block_hide    = re.compile(".*#hide")
# </REGEX DEFINITIONS>

# <MAIN PROCESS>
def link(file, depth=3, pattern="^!r(?:eq(?:uire)?)?\(([\w\-. \/]+)\)$"):
    """ link a markdown file

    Input: the path to a file
    Output: A list of strings, the resulting file.

    The default pattern matches `!require(...)` or `!r(...)`, with a path
    relative to the source file.
    """
    pattern = re.compile(pattern)
    lines = []

    # save the current working directory
    cwd = os.getcwd()
    if len(fdir := os.path.dirname(file)) > 0:
        os.chdir(fdir)
    with open(os.path.basename(file), "r") as f:
        source_lines = f.readlines()
        for i, line in enumerate(source_lines):
            if depth > 0 and (match:=pattern.match(line)):
                lines += link(match.group(1), depth-1)
            else: lines.append(line)
    # if the last line doesn't end with a newline, add one
    if lines[-1][-1] != "\n": lines[-1] += "\n"
    os.chdir(cwd)
    return lines
# </MAIN PROCESS>


# <CLI INVOCATION>
if __name__ == '__main__':
    # link the file
    result = link(sys.argv[1])
    # output the results
    if len(sys.argv) == 3:
        with open(sys.argv[2], 'w') as dest:
            for line in result:
                dest.write(line)
    else:
        for line in result:
            print(line, end='')
# </CLI INVOCATION>
