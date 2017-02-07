#!/usr/bin/env python
"""
matchFakes.py
matches fakes based on position stored in the calibrated exposure image header
"""

import lsst.daf.persistence as dafPersist
from lsst.afw.table.tableLib import SourceCatalog
import numpy as np
import argparse
import re
import collections

def getFakeSources(rootdir, dataId, tol=0.1):
    """Get list of sources which agree in position with fake ones with tol
    """
    butler = dafPersist.Butler(rootdir)

    sources = butler.get('src', dataId)
    cal_md  = butler.get('calexp_md', dataId)

    # Get the X, Y locations of objects on the CCD
    srcX, srcY = sources.getX(), sources.getY()
    # Get the zeropoint
    zeropoint = 2.5*np.log10(cal_md.get("FLUXMAG0"))
    # Get the PSF flux and its error
    flux, ferr = sources.getPsfFlux(), sources.getPsfFluxErr()
    # Convert them into magnitude and its error
    mag,  merr = 2.5*np.log10(flux), 2.5/np.log(10)*(ferr/flux)
    mag = zeropoint - mag

    # X, Y locations of the fake stars
    fakeXY   = collections.defaultdict(tuple)
    # Regular Expression
    fakename = re.compile('FAKE([0-9]+)')
    for card in cal_md.names():
        m = fakename.match(card)
        if m is not None:
            x,y = map(float, (cal_md.get(card)).split(','))
            fakeXY[int(m.group(1))] = (x,y)

    srcIndex = collections.defaultdict(list)
    for fid, fcoord  in fakeXY.items():
        matched = ((np.abs(srcX-fcoord[0]) < tol) &
                   (np.abs(srcY-fcoord[1]) < tol))
        s1 = sources.subset(matched)
        srcIndex[fid] = np.where(matched)[0]

    #srcList    = None
    srcPsfMag  = []
    srcPsfMerr = []
    matchX     = []
    matchY     = []
    for s in srcIndex.values():
        #for ss in s:
        #if srcList is None:
        #   srcList = SourceCatalog(sources.getSchema())
        #   srcList.append(sources[ss])
        #
        if len(s) > 0:
            ss = s[0]
            srcPsfMag.append(mag[ss])
            srcPsfMerr.append(merr[ss])
            matchX.append(srcX[ss])
            matchY.append(srcY[ss])
        else:
            srcPsfMag.append(0)
            srcPsfMerr.append(0)
            matchX.append(0)
            matchY.append(0)

    return srcIndex, fakeXY, matchX, matchY, srcPsfMag, srcPsfMerr


def main():

    #TODO: this should use the LSST/HSC conventions
    parser = argparse.ArgumentParser()
    parser.add_argument('rootDir', help='root dir of data repo')
    parser.add_argument('visit', help='id of visit', type=int)
    parser.add_argument('ccd', help='id of ccd', type=int)
    args = parser.parse_args()

    #(starIndex,starList) = getFakeSources(args.rootDir, {'visit':args.visit, 'ccd':args.ccd})
    (starIndex, fakeXY, matchX, matchY, starPsfMag, starPsfMerr) = getFakeSources(args.rootDir,
                                                                                  {'visit':args.visit, 'ccd':args.ccd})

    nInject = len(fakeXY)
    nMatch  = len(np.argwhere(starPsfMag))
    print "# Number of Injected Stars : %d" % nInject
    print "# Number of Matched  Stars : %d" % nMatch
    print "# Visit = %d   CCD = %d" % (args.visit, args.ccd)
    print "# FakeX  FakeY  PSFMag  PSFMagErr  Deblend "

    for i in range(nInject):
       #print starIndex[i][0], starList[i]['flux.psf']
       if len(starIndex[i]) > 1:
           deblend = "blended"
       elif starPsfMag[i] > 0:
           deblend = "isolate"
       else:
           deblend = "nomatch"

       injectXY = fakeXY[i]

       print "%6.1d   %6.1d   %7.3f  %6.3f  %s" % (injectXY[0], injectXY[1],
                                            starPsfMag[i], starPsfMerr[i], deblend)


if __name__=='__main__':
    main()
