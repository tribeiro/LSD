__author__ = 'tiago'

import numpy as np
from astropy.io import fits


class SizeError(BaseException):
    pass


class OutOfRange(BaseException):
    pass

class LineID():

    id = None
    center = None # Wavelenght
    depth = None

    nlines = 0


class Amatrix(LineID):
    matrix = None
    wave = None

    wstart = 0.  # Start Wavelength
    wend = 0.  # End Wavelength
    wres = 0.  # Wavelength resolution

    def loadFits(self, filename, hdunum=1):
        hdu = fits.open(filename)
        self.matrix = hdu[hdunum].data()

        self.wstart = hdu[0].header['WSTART']
        self.wend = hdu[0].header['WEND']
        self.wres = hdu[0].header['WRES']

        hdu.close()

        self.wave = np.arange(self.wstart, self.wend, self.wres)
        if len(self.wave) != len(self.matrix):
            raise SizeError(
                "Matrix size (%i) does not match wavelength array (%i)... Check Matrix calculation..." % (
                len(self.matrix),
                len(self.wave)))

    def storeFits(self, filename, hdunum=1):
        raise NotImplemented("Function has not been implemented yet...")

    def calcMatrix(self):
        '''
        Use LineID information to calculate matrix. This is really slow, better run it outsize.
        :return:
        '''

        _Amtx = []
        xspec = self.wave
        wcenter = (self.wstart + self.wend) / 2.
        Zv = np.arange((self.wstart - wcenter) / wcenter * self.c_kms,
                       (self.wend - wcenter) / wcenter * self.c_kms,
                       self.wres / wcenter * self.c_kms)
        Zdv = self.wres / wcenter * self.c_kms

        support_code = """
double _A_(double x)
{
    if(-1 <= x <= 0) {
        cout << x << endl;
        return_val 1+x;
    }
    if(0 < x < 1) {
        cout << x << endl;
        return 1-x;
    }
    else return 0;
}
"""
        cpp = """
#include <cmath>

using namespace std;
#define _A_(a) ((abs(a)<(1)) ? (1-abs(a)) : (0))

//double** Ajk = new double* [xsp_SIZE];
//Ajk = new double* [xsp_SIZE];
const double c_kms = 3.0e5;

for (int j = 0; j < xsp_SIZE;j++){
    //Ajk[j] = new double [SIZE];

    for (int k = 0; k < SIZE;k++){
        double ajk = 0;

        for( int i=0; i<n; i++){
            ajk += _einfo[i]*_A_( ( Zv[k]-c_kms*(xspec[j]-_winfo[i])/_winfo[i] ) /double(Zdv));
            //cout << Ajk[j][k] << endl;
        }
        Ajk[j][k] = ajk;
        //exit(0);
    }
}

return_val = 0;
		"""
        xsp_SIZE = len(xspec)
        SIZE = len(Zv)
        n = self.nlines
        _winfo, _einfo, names = self.getWorkingLines()
        # _einfo = np.array(_einfo, dtype=float)
        # _winfo = np.array(_winfo, dtype=float)

        Ajk = np.zeros((xsp_SIZE, SIZE))  # np.zeros(self.Zv.size) #self.store_A
        # for j in range(xsp_SIZE):
        #    Ajk.append(np.zeros(SIZE))
        #	Ajk[j].resize(self.Zv.size)
        #	for k in range(self.Zv.size):
        #		Ajk[j].append(0.0)

        #print Ajk[0][0]
        print "----------------------------------------------------"
        print "| Resolvendo gargalo por codigo inline mais rapido |"
        e = scipy.weave.inline(cpp, ['xsp_SIZE', 'SIZE', 'n', '_einfo', '_winfo', 'Zv', 'Zdv', 'xspec',
                                     'Ajk'])  #,support_code=support_code)#,type_converters=scipy.weave.converters.blitz)
        print "----------------------------------------------------"
        #print e
        self.matrix = np.array(Ajk)
        print "Fim!"
        #for i in range(len(self._Amatrix)):
        #    self._Amatrix[i] = np.array(self._Amatrix[i], dtype=float)
        #for j in range(len(self._Amatrix[i])):
        #	if self._Amatrix[i][j] > 0.0: print i,j,self._Amatrix[i][j]

        #raise NotImplemented("Function has not been implemented yet...")

    def nearestW(self, w):

        if w < self.wstart or w > self.wend:
            raise OutOfRange('Value %f is out of range: [%f:%f]' % (w, self.wstart, self.wend))

        return np.argmin(np.abs(self.wave - w))


class LineProfile(Amatrix):

    lpx = None
    lpy = None
    lperr = None

    lpdx = 0.0 # Resolution in km/s

    c_kms = 299792.458  # speed of light in km/s

    def initProfile(self, val=None, err=None):

        wcenter = (self.wstart + self.wend) / 2.
        self.lpx = np.arange((self.wstart - wcenter) / wcenter * self.c_kms,
                             (self.wend - wcenter) / wcenter * self.c_kms,
                             self.wres / wcenter * self.c_kms)
        self.lpy = np.zeros_like(self.lpx)
        self.lperr = np.zeros_like(self.lpx)

        if val and len(val) == len(self.lpy):
            self.lpy = np.array(val)

        if val and len(val) == len(self.lpy):
            self.lpy = np.array(val)

        self.lpdx = dx

    def loadProfile(self, profile, err=None):

        if len(profile) == len(self.lpy):
            self.lpy = profile

        if err and len(err) == len(self.lperr):
            self.lperr = err

            # def nearestV(self,v):
            #
            # if v < self.wstart or v > self.wend:
            #         raise OutOfRange('Value %f is out of range: [%f:%f]'%(w,self.wstart,self.wend))
            #
            #     return np.argmin(np.abs(self.wave - w))


class LineMaker(LineProfile):
    def makeSpec(self,start,end):
        istart = self.nearestW(start)
        iend = self.nearestW(end)
        # spec = np.zeros_like(wave)

        return np.dot(self.matrix[:, istart:iend], self.lpy[istart:iend])
