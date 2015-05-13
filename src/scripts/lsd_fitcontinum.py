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

    logging.info('Reading in input spectrum: %s' % opt.filename)

    data = Table.read(opt.filename, format='ascii.no_header')
    mask = np.bitwise_and(data['col1'] > 5700, data['col1'] < 6500)
    spectrum = spec.Spectrum(data['col1'][mask], data['col2'][mask], data['col2'][mask] / 25.)

    p = np.polyfit(spectrum.x, spectrum.flux, opt.order)

    # py.plot(spectrum.x,spectrum.flux)
    # py.plot(spectrum.x,np.polyval(p,spectrum.x))
    #
    # py.show()
    #
    # return 0

    minmax = {}
    init = np.zeros_like(p)

    for i in range(len(p)):
        vals = np.array([p[i] + 0.5 * p[i], p[i] - 0.5 * p[i]])
        print np.min(vals), np.max(vals), p[i] * 1.1, p[i]
        minmax['%i_min' % i] = np.min(vals)
        minmax['%i_max' % i] = np.max(vals)
        minmax['%i_val' % i] = (np.random.rand(1) * np.abs(p[i]) * 0.5) + np.min(vals)
        init[i] = minmax['%i_val' % i]
    print init

    M = pymc.MCMC(continumFactory(spectrum, opt.order, minmax),
                  db='ram')
    # map_ = pymc.MAP( M )
    #map_.fit()

    M.sample(iter=50000, burn=25000, tune_interval=1000,
             tune_throughout=False)  #try running for longer if not happy with convergence.

    logging.info('Sampler done...')

    #M.write_csv(opt.output)

    coeff = np.zeros_like(p)
    for i in range(len(coeff)):
        coeff[i] = np.mean(np.array([ii for ii in M.trace('par_%02i' % i)[:]]))

    print p
    print coeff
    print init
    #py.plot(tt,ecflx)
    #py.errorbar(ectobs,ecobs+ecerr,0.1,fmt='o')

    cont = np.array(M.trace('continum')[:]).T
    oarray = np.array([np.mean(i) for i in cont])
    #earray = np.array(	[ np.std(i) for i in cont] )

    py.plot(spectrum.flux)
    py.plot(np.polyval(p, spectrum.x))
    py.plot(np.polyval(init, spectrum.x))
    py.plot(oarray)
    pymc.Matplot.plot(M)

    py.show()

    return 0


if __name__ == '__main__':
    main(sys.argv)