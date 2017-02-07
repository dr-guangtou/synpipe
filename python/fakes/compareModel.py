#!/usr/bin/env python
"""
Compare the input fake galaxy model to the output one
"""
import argparse

import numpy as np

import astropy.table

import lsst.pipe.base
import lsst.afw.table
import lsst.afw.geom.ellipses
import lsst.daf.persistence as dafPersist

from matchFakes import getFakeSources


def getParams(record, galType='sersic'):
    """
    return the semi-major axis, axis ratio and position angle (in degrees)
    """
    fluxType = {'dev': 'cmodel.dev',
                'exp': 'cmodel.exp',
                'sersic': 'cmodel',
                'cmodel': 'cmodel'}[galType]

    e = lsst.afw.geom.ellipses.Axes(record.get(fluxType + '.ellipse'))
    q = (e.getB() / e.getA())
    reff = e.getA()
    pa = (e.getTheta() * 180.0 / np.pi)
    return reff, q, pa


def getMag(record, fluxType='cmodel'):
    """
    return the magnitude and error
    """
    flux, fluxerr = record.get(fluxType), record.get(fluxType+'.err')
    mag, magerr = -2.5 * np.log10(flux), 2.5/np.log(10.0)*fluxerr/flux
    mag += record.get('zeropoint')
    return mag, magerr


def writeNumpyTable(fakeTable):
    """Writes output to numpy
    """
    npTable = np.recarray(len(fakeTable),
                          dtype={'names':['id', 'fakeid', 'visit', 'ccd',
                                          'cmodelMag', 'expMag',
                                          'devMag',
                                          'expReff', 'devReff',
                                          'expBA', 'devBA',
                                          'expPosAng', 'devPosAng',
                                          'cmodelMagErr', 'expMagErr',
                                          'devMagErr', 'nchild', 'parent'],
                                 'formats':[long, int, int, int,
                                            float, float,
                                            float, float, float, float,
                                            float, float, float, float,
                                            float, float, int, long]})
    for indFake, fake in enumerate(fakeTable):
        npTable[indFake]['id'] = fake.get('id')
        npTable[indFake]['fakeid'] = fake.get('fakeId')
        npTable[indFake]['ccd'] = fake.get('ccd')
        npTable[indFake]['visit'] = fake.get('visit')
        nameMatch = {'sersic':'cmodel',
                     'exp':'cmodel.exp',
                     'cmodel':'cmodel',
                     'dev':'cmodel.dev'}
        for name in ('cmodel', 'exp', 'dev'):
            m1, m2 = getMag(fake, nameMatch[name]+'.flux')
            npTable[indFake][name+'Mag'] = m1
            npTable[indFake][name+'MagErr'] = m2
        for name in ('exp', 'dev'):
            params = getParams(fake, name)
            npTable[indFake][name+'Reff'] = params[0]
            npTable[indFake][name+'BA'] = params[1]
            npTable[indFake][name+'PosAng'] = params[2]
        npTable[indFake]['nchild'] = fake.get('deblend.nchild')
        npTable[indFake]['parent'] = fake.get('parent')
    return npTable


def main(root, visit, ccds, galType='sersic', output='outputs/'):
    """
    main function for controlling fake source comparison
    """
    butler = dafPersist.Butler(root)
    fakeTable = None
    for ccd in ccds:
        dataId = {'visit':visit, 'ccd':ccd}
        try:
            temp = getFakeSources(butler, dataId, tol=1.0,
                                  visit=True, ccd=True)
        except:
            continue
        if fakeTable is None:
            fakeTable = temp.copy(True)
        else:
            fakeTable.extend(temp, True)

    npTable = writeNumpyTable(fakeTable)
    rerunName = root.split('/')[-2]
    fitsTable = astropy.table.Table(npTable).write(output+'/'+rerunName+
                                             '_galMags.txt', format='ascii')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root', help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit")
    parser.add_argument("--ccd", nargs='+', type=int, help="CCD(s)")
    parser.add_argument('-g', '--galtype', type=str, dest='galType',
                        choices=['exp', 'dev', 'sersic'])
    parser.add_argument('-o', '--outputpath', dest='outpath',
                        help='path for output')
    args = parser.parse_args()

    main(args.root, args.visit, args.ccd, galType=args.galType,
         output=args.outpath)
