__author__ = 'tiago'

import numpy as np

class LineID():

    id = None
    center = None # Wavelenght
    depth = None

    nlines = 0

class LineProfile():

    lpx = None
    lpy = None
    lperr = None

    lpdx = 0.0 # Resolution in km/s

    def initProfile(self,x0,x1,dx,val=None,err=None):

        self.lpx = np.arange(x0,x1,dx)
        self.lpy = np.zeros_like(self.lpx)
        self.lperr = np.zeros_like(self.lpx)

        if val and len(val) == len(self.lpy):
            self.lpy = np.array(val)

        if val and len(val) == len(self.lpy):
            self.lpy = np.array(val)

        self.lpdx = dx

    def loadProfile(self):

class LineMaker(LineID,LineProfile):

    Amatrix = None



    def makeSpec(self,start,end):

        # spec = np.zeros_like(wave)
        return 0