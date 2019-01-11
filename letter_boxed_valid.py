#!/usr/bin/env python3

__doc__ = """
letter-boxed-valid: Finds valid words for the NYT Letter Boxed puzzle

"""
__copyright__ = "Copyright (C) 2019 Leo C. Stein"
__email__ = "leo.stein@gmail.com"
__status__ = "testing"
__author__ = "Leo C. Stein"
__version__ = "0.1"
__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import argparse
from itertools import zip_longest, groupby

def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks
grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
Taken from the itertools recipes, https://docs.python.org/3/library/itertools.html#itertools-recipes
"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def posLet(c, data):
    """Find the position of character c in the list of tuples or sets in data.  Will error if c does not appear"""
    return [i for i,x in enumerate(data) if c in x][0]

def alwaysSideChanging(word, data):
    """Test if every consecutive character in word comes from a different side (group in list data) of the square"""
    sides = [posLet(c, data) for c in word]
    return len(sides) == len(list(groupby(sides)))

def validWords(puzset, puzData, dictlines):
    words = [line.strip().lower() for line in dictlines]

    return [word for word in words
            if set(word).issubset(puzset) and alwaysSideChanging(word, puzData) ]

#############################    main    ##################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__)

    parser.add_argument('--dict', type=argparse.FileType('r'),
                        default='/usr/share/dict/words',
                        help='Dictionary file (default: %(default)s)')

    parser.add_argument('puzzle_string',
                        help="""List of letters going around the box.  Will be split into groups of three letters per side.  Example: 'loigntshcpau' => [('l', 'o', 'i'), ('g', 'n', 't'), ('s', 'h', 'c'), ('p', 'a', 'u')]""")

    args = parser.parse_args()

    puzset = set(args.puzzle_string.lower())
    puzData = list(grouper(args.puzzle_string.lower(),3))

    words = validWords(puzset, puzData, args.dict)
    words.sort(key=len)

    for word in words:
        print(word)
