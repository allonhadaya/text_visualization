#!/usr/bin/env python
'''Histogram. Draws normalized ascii histograms of numbers or text length from stdin.

Usage:
  histogram.py [--width=<width>] [--height=<height>] [--symbol=<symbol>] [--length]

Options:
  -h --help          Show this screen.
  --width=<width>    The width of the histogram in characters. [default: 80]
  --height=<height>  The height of the histogram in lines. [default: 120]
  --symbol=<symbol>  The symbol used to indicate one unit. [default: |]
  --length           Pass the input lines through the len function rather than float.

'''
from docopt import docopt
import sys
import math

if __name__ == '__main__':

    def average(xs):
        return sum(xs) / float(len(xs))

    def reduce_average(seq, size):
        result = []
        for element in seq:
            result.append(element)
            if len(result) == size:
                yield average(result)
                result = []
        if len(result) > 0:
            yield average(result)

    arguments = docopt(__doc__, version='1.0')

    text = sys.stdin

    if arguments['--length']:
        text = (len(line) for line in text)

    numbers = [float(line) for line in text]
    numbers.sort()

    group_size = int(math.ceil(float(len(numbers)) / int(arguments['--height'])))
    group_size = max(1, group_size) # no less than one item per line

    numbers = list(reduce_average(numbers, group_size))

    largest_number = numbers[-1]

    width_factor = int(arguments['--width']) / largest_number

    numbers = (width_factor * number for number in numbers)
    symbols = (arguments['--symbol'] * int(number) for number in numbers)

    for s in symbols:
        print s

