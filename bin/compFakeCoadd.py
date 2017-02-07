#!/usr/bin/env python

import re
import os
import argparse

import collections
import numpy as np
import pyfits as fits
import matplotlib.pyplot as pyplot

import lsst.daf.persistence as dafPersist
import lsst.afw.geom.ellipses as geomEllip
from lsst.afw.table import SourceCatalog, SchemaMapper

from distutils.version import StrictVersion

def zscale(img, contrast=0.25, samples=500):

    # Image scaling function form http://hsca.ipmu.jp/hscsphinx/scripts/psfMosaic.html
    ravel = img.ravel()
    if len(ravel) > samples:
        imsort = np.sort(np.random.choice(ravel, size=samples))
    else:
        imsort = np.sort(ravel)

    n = len(imsort)
    idx = np.arange(n)

    med = imsort[n/2]
    w = 0.25
    i_lo, i_hi = int((0.5-w)*n), int((0.5+w)*n)
    p = np.polyfit(idx[i_lo:i_hi], imsort[i_lo:i_hi], 1)
    slope, intercept = p

    z1 = med - (slope/contrast)*(n/2-n*w)
    z2 = med + (slope/contrast)*(n/2-n*w)

    return z1, z2


def getExpArray(root, tract, patch, filter):

    # make a butler and specify your dataId
    butler = dafPersist.Butler(root)
    dataId = {'tract': tract, 'patch':patch, 'filter':filter}

    pipeVersion = dafPersist.eupsVersions.EupsVersions().versions['hscPipe']
    if StrictVersion(pipeVersion) >= StrictVersion('3.9.0'):
        dataType = "deepCoadd_calexp"
    else:
        dataType = "deepCoadd"

    # get the exposure from the butler
    # Ugly work around in case the before and after Reruns are from different hscPipe
    try:
        exposure = butler.get(dataType, dataId, immediate=True)
    except:
        try:
            exposure = butler.get('deepCoadd', dataId, immediate=True)
        except:
            raise

    # get the maskedImage from the exposure, and the image from the mimg
    mimg = exposure.getMaskedImage()
    img = mimg.getImage()

    # convert to a numpy ndarray
    return img.getArray()


def main(root1, root2, tract, patch, filter, root=""):

    # get the name of the rerun
    rerun = os.path.split(root2)[-1]

    # get the image array before the fake objects are added
    imgBefore = getExpArray(root1, tract, patch, filter)
    imgAfter  = getExpArray(root2, tract, patch, filter)

    # get the difference between the two image
    imgDiff = (imgAfter - imgBefore)

    # stretch it with arcsinh and make a png with pyplot
    fig, axes = pyplot.subplots(1, 3, sharex=True, sharey=True, figsize=(16.5,5))
    pyplot.subplots_adjust(left=0.04, bottom=0.04, right=0.99, top=0.95,
                           wspace=0.01, hspace = 0.01)

    imgs   = imgBefore, imgAfter, imgDiff
    titles = "Before", "After", "Diff"
    for i in range(3):
        print '### Plot : ', i
        imin, imax = zscale(imgs[i], contrast=0.10, samples=500)
        axes[i].imshow(np.arcsinh(imgs[i]), interpolation="none",
                vmin=imin, vmax=imax, cmap='gray')
        axes[i].set_title(titles[i])

    pyplot.gcf().savefig("%s-%s-%s-%s.png"%(rerun, str(tract), str(patch), str(filter)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("root1", help="Root directory of data before adding fake objects")
    parser.add_argument("root2", help="Root directory of data after adding fake objects")
    parser.add_argument("tract", type=int, help="Tract to show")
    parser.add_argument("patch", help="Patch to show")
    parser.add_argument("filter", help="Filter to show")
    args = parser.parse_args()

    main(args.root1, args.root2, args.tract, args.patch, args.filter)
