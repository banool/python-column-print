import queue
import textwrap

from contextlib import suppress
from shutil import get_terminal_size

DELIMITER = ' | '

width = get_terminal_size((80, 20)).columns

num_cols = 2

width = width - (num_cols-1)*len(DELIMITER)  # For the dashed line in the middle.

q0 = queue.Queue()
q1 = queue.Queue()

qs = [q0, q1]

def column_print(str, col=None):
    if col is None:
        raise RuntimeError('The integer value "col" must be given')
    qs[col].put(str)

def get_cols(qs, width):
    strings = {}
    num_cols = len(qs)
    subwidth = width // num_cols
    for i, q in enumerate(qs):
        with suppress(queue.Empty):
            s = q.get(timeout=0.5)
            strings[i] = s
    # Get the print for each column, or '' if there wasn't one, and break it
    # into rows that fit in that column (see subwidth).
    cols = []
    for i in range(num_cols):
        s = strings.get(i, '')
        ss = textwrap.wrap(s, subwidth)
        cols.append(ss)
    # Fill in columns with shorter strings to print with empty rows.
    most = max(len(i) for i in cols)
    for col in cols:
        if len(col) < most:
            for i in range(0, most-len(col)):
                col.append('')
    # Fill in whitespace on the right of each string if necessary.
    for col in cols:
        for i, row in enumerate(col):
            col[i] = row.ljust(subwidth)
    return cols

def print_cols(cols):
    zipped = list(zip(*cols))
    for row in zipped:
        print(DELIMITER.join(row))

column_print('hey my dude how are you i hope you are good like this is a big deal 4 me i think', col=0)
column_print('this is in my second column which i hope prints juut fine alongside my first one though you never really know do you', col=1)

cols = get_cols(qs, width)

print_cols(cols)
