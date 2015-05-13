__author__ = 'tiago'

'''
Provides a model factory for fitting continuum.
'''

import numpy as np
import pymc


def continumFactory(spectrum, polyorder, polyrange):
    par = [pymc.Uniform('par_%02i' % i,
                        lower=polyrange['%i_min' % i],
                        upper=polyrange['%i_max' % i],
                        value=polyrange['%i_val' % i]) for i in range(polyorder + 1)]

    @pymc.deterministic
    def continum(par=par):
        p = np.array([i for i in par])
        # print 'continum: ',
        # for i in p:
        # print '%e '%i,
        # print
        return np.polyval(par, spectrum.x)

    sig = pymc.Uniform('sig',
                       np.median(spectrum.flux) / 100.,
                       np.median(spectrum.flux) / 10.,
                       value=np.median(spectrum.flux) / 25.)

    y = pymc.Normal('y', mu=continum,
                    tau=1. / sig ** 2.,
                    value=spectrum.flux,
                    observed=True)

    return locals()



