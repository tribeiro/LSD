#! /usr/bin/env python

'''
An experimental script to fit spectra continum using PyMC
'''

__author__ = 'tiago'

import sys
import numpy as np
from astropy.table import Table
import pymc
from lsd.core.continum_factory import continumFactory
import logging
from astropysics import spec
import pylab as py


def main(argv):
    logging.basicConfig(format='%(levelname)s:%(asctime)s::%(message)s',
                        level=logging.DEBUG)

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option('-f', '--filename',
                      help='Input spectrum to fit.'
                      , type='string')
    parser.add_option('-o', '--output',
                      help='Output root name.'
                      , type='string')
    parser.add_option('--order',
                      help="Polynomial order.",
                      type='int', default=7)
    opt, args = parser.parse_args(argv)

    return 0


if __name__ == '__main__':
    main(sys.argv)