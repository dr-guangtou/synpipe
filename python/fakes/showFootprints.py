#!/usr/bin/env python
"""
function to show a list of src footprints in a mosaic
"""

import argparse

import lsst.afw.image
import lsst.daf.persistence
import lsst.afw.display.ds9 as ds9
import lsst.afw.display.utils

import matchFakes

import numpy.random


def getMosaic(sources, exposure, idname):
    """
    make a ds9 mosaic for the given source list from the given exposure

    stolen from psfMosaic.py on the sphinx documentation
    """
    img = exposure.getMaskedImage().getImage()
    subImages = []
    labels = []
    for src in sources:
        footBBox = src.getFootprint().getBBox()
        subimg = lsst.afw.image.ImageF(img, footBBox,
                                       lsst.afw.image.PARENT, True)
        footMask = lsst.afw.image.ImageU(footBBox)
        src.getFootprint().insertIntoImage(footMask, 1, footBBox)
        subimg *= footMask.convertF()
        subImages.append(subimg)
        labels.append('ID=%s' % str(src.get(idname)))

    m = lsst.afw.display.utils.Mosaic()
    m.setGutter(2)
    m.setBackground(0)
    m.setMode("square")

    # create the mosaic
    for img in subImages:
        m.append(img)
    mosaic = m.makeMosaic()

    # display it with labels in ds9
    ds9.mtv(mosaic)
    m.drawLabels(labels)


def main(root, visit, ccd, fakes=None, blends=False, listobj=16, filt=None):

    butler = lsst.daf.persistence.Butler(root)
    dataId = {'visit': visit,
              'ccd': int(ccd)} if filt is None else {'tract': visit,
                                                     'patch': ccd,
                                                     'filter': filt}

    if fakes is not None:
        src = matchFakes.getFakeSources(butler, dataId,
                                        extraCols=('zeropoint'),
                                        radecMatch=fakes)
    else:
        src = butler.get('src' if filt is None else 'deepCoadd-src', dataId)
    if not blends:
        src = [s for s in src if ((s.get('deblend.nchild') == 0) &
                                  (s.get('parent') == 0))]
    else:
        src = [s for s in src if (s.get('deblend.nchild') == 0)]

    exposure = butler.get('calexp' if filt is None else 'deepCoadd', dataId)

    if type(listobj) is int:
        listobj = numpy.random.choice(range(len(src)), listobj, False)

    srcList = [src[i] for i in listobj]

    getMosaic(srcList, exposure, 'fakeId' if fakes else 'id')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root', help="Root directory of data repository")
    parser.add_argument("visit", type=int, help="Visit or tract")
    parser.add_argument("ccd", type=str, help="CCD or patch")
    parser.add_argument('-d', '--band', default=None,
                        help='HSC filter, used with tract/patch')
    parser.add_argument('-f', '--fake', default=None,
                        help='show fake sources, using -f as catalog')
    parser.add_argument('-n', '--number', dest='num',
                        help='number of objects to show',
                        default=16, type=int)
    parser.add_argument('-b', '--blends', action='store_true',
                        default=False, help='show blended systems')

    args = parser.parse_args()

    main(args.root, args.visit, args.ccd,
         fakes=args.fake, listobj=args.num,
         blends=args.blends, filt=args.band)
