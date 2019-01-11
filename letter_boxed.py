#!/usr/bin/env python3

__doc__ = """
letter-boxed: Finds valid solutions for the NYT Letter Boxed puzzle

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
from letter_boxed_valid import validWords, grouper

def chainSet(chain):
    return set.union(*[set(word) for word in chain])

def coversSet(chain, puzset):
    return puzset.issubset(chainSet(chain))

#############################    main    ##################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__)

    parser.add_argument('--dict', type=argparse.FileType('r'),
                        default='/usr/share/dict/words',
                        help='Dictionary file (default: %(default)s)')

    parser.add_argument('--max', type=int,
                        default=4,
                        help='Maximum length of word chains to find (default: %(default)s)')

    parser.add_argument('puzzle_string',
                        help="""List of letters going around the box.  Will be split into groups of three letters per side.  Example: 'loigntshcpau' => [('l', 'o', 'i'), ('g', 'n', 't'), ('s', 'h', 'c'), ('p', 'a', 'u')]""")

    args = parser.parse_args()

    puzset = set(args.puzzle_string.lower())
    puzData = list(grouper(args.puzzle_string.lower(),3))

    valid = validWords(puzset, puzData, args.dict)

    maxChainLen = args.max
    validChains = [[word] for word in valid]

    for i in range(1,maxChainLen + 1):

        oldValidChains = validChains
        validChains = []

        for chain in oldValidChains:

            if coversSet(chain, puzset):
                print('-'.join(chain).upper())

            if i == maxChainLen: # this is wasteful on the last step
                continue

            lastLet = chain[-1][-1]

            newChains = [ chain + [word] for word in valid
                          if word[0] == lastLet ]

            # Question: should we restrict newChains so that it only
            # contains words that cover more letters (have a longer
            # chain set length)?
            # chSetLen = len(list(chainSet(chain)))

            validChains.extend(newChains)

