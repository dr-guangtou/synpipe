#!/usr/bin/env python

import re
import os
import argparse
import collections

import numpy as np
import matplotlib.pyplot as pyplot

import lsst.daf.persistence as dafPersist

from lsst.afw.table import SourceCatalog, SchemaMapper


def getGalaxy(rootdir, visit, ccd, tol):
    """Get list of sources which agree in position with fake ones with tol
    """
    # Call the butler
    butler = dafPersist.Butler(rootdir)
    dataId = {'visit': visit, 'ccd': ccd}
    tol = float(tol)

    # Get the source catalog and metadata
    sources = butler.get('src', dataId)
    cal_md = butler.get('calexp_md', dataId)

    # Get the X, Y locations of objects on the CCD
    srcX, srcY = sources.getX(), sources.getY()
    # Get the zeropoint
    zeropoint = (2.5 * np.log10(cal_md.get("FLUXMAG0")))
    # Get the parent ID
    parentID = sources.get('parent')
    # Check the star/galaxy separation
    extendClass = sources.get('classification.extendedness')
    # Get the nChild
    nChild = sources.get('deblend.nchild')

    # For Galaxies: Get these parameters
    # 1. Get the Kron flux and its error
    fluxKron, ferrKron = sources.get('flux.kron'), sources.get('flux.kron.err')
    magKron = (zeropoint - 2.5 * np.log10(fluxKron))
    merrKron = (2.5 / np.log(10) * (ferrKron / fluxKron))
    # X, Y locations of the fake galaxies
    fakeList = collections.defaultdict(tuple)
    # Regular Expression
    # Search for keywords like FAKE12
    fakename = re.compile('FAKE([0-9]+)')
    # Go through all the keywords
    counts = 0
    for card in cal_md.names():
        # To see if the card matches the pattern
        m = fakename.match(card)
        if m is not None:
            # Get the X,Y location for fake object
            x, y = map(float, (cal_md.get(card)).split(','))
            # Get the ID or index of the fake object
            fakeID = int(m.group(1))
            fakeList[counts] = [fakeID, x, y]
            counts += 1

    # Match the fake object to the source list
    srcIndex = collections.defaultdict(list)
    for fid, fcoord in fakeList.items():
        separation = np.sqrt(np.abs(srcX-fcoord[1])**2 +
                             np.abs(srcY-fcoord[2])**2)
        matched = (separation <= tol)
        matchId = np.where(matched)[0]
        matchSp = separation[matchId]
        sortId = [matchId for (matchSp, matchId) in
                  sorted(zip(matchSp, matchId))]
        # DEBUG:
        # print fid, fcoord, matchId
        # print sortId, sorted(matchSp), matchId
        # Select the index of all matched object
        srcIndex[fid] = sortId

    # Return the source list
    mapper = SchemaMapper(sources.schema)
    mapper.addMinimalSchema(sources.schema)
    newSchema = mapper.getOutputSchema()
    newSchema.addField('fakeId', type=int,
                       doc='id of fake source matched to position')
    srcList = SourceCatalog(newSchema)
    srcList.reserve(sum([len(s) for s in srcIndex.values()]))

    # Return a list of interesting parameters
    srcParam = []
    nFake = 0
    for matchIndex in srcIndex.values():
        # Check if there is a match
        if len(matchIndex) > 0:
            # Only select the one with the smallest separation
            # TODO: actually get the one with minimum separation
            ss = matchIndex[0]
            fakeObj = fakeList[nFake]
            diffX = srcX[ss] - fakeObj[1]
            diffY = srcY[ss] - fakeObj[2]
            paramList = (fakeObj[0], fakeObj[1], fakeObj[2],
                         magKron[ss], merrKron[ss], diffX, diffY,
                         parentID[ss], nChild[ss], extendClass[ss])
            srcParam.append(paramList)
        else:
            fakeObj = fakeList[nFake]
            paramList = (fakeObj[0], fakeObj[1], fakeObj[2],
                         0, 0, -1, -1, -1, -1, -1)
            srcParam.append(paramList)
        # Go to another fake object
        nFake += 1

    # Make a numpy record array
    srcParam = np.array(srcParam, dtype=[('fakeID', int),
                                         ('fakeX', float),
                                         ('fakeY', float),
                                         ('magKron', float),
                                         ('errKron', float),
                                         ('diffX', float),
                                         ('diffY', float),
                                         ('parentID', int),
                                         ('nChild', int),
                                         ('extendClass', float)])

    return srcIndex, srcParam, srcList, zeropoint


def getExpArray(root, visit, ccd, filter=None):

    # make a butler and specify your dataId
    butler = dafPersist.Butler(root)
    if filter:
        dataId = {'tract': visit,
                  'patch': ccd,
                  'filter': filter}
        prefix = "deepCoadd_"
    else:
        dataId = {'visit': visit,
                  'ccd': int(ccd)}
        prefix = ""

    # get the exposure from the butler
    exposure = butler.get(prefix+'calexp', dataId)

    # get the maskedImage from the exposure, and the image from the mimg
    mimg = exposure.getMaskedImage()
    img = mimg.getImage()

    # convert to a numpy ndarray
    return img.getArray()


def getNoMatchXY(rootDir, visit, ccd):
    # TODO: Need to be organized
    (fakeIndex, fakeParam, fakeList, zp) = getGalaxy(rootDir,
                                                     visit, ccd, 2.0)
    fakeX = fakeParam['fakeX']
    fakeY = fakeParam['fakeY']
    fakeMag = fakeParam['magKron']
    nFakes = len(fakeX)
    nNoMatch = (nFakes - len(np.argwhere(fakeMag)))
    noMatchX = []
    noMatchY = []
    badKronX = []
    badKronY = []
    for i in range(nFakes):
        if np.isnan(fakeMag[i]):
            badKronX.append(fakeX[i])
            badKronY.append(fakeY[i])
        elif (fakeMag[i] > 0):
            pass
        else:
            noMatchX.append(fakeX[i])
            noMatchY.append(fakeY[i])

    if len(noMatchX) is not nNoMatch:
        raise Exception("Something is wrong about the number of noMatch")

    return noMatchX, noMatchY, fakeX, fakeY, badKronX, badKronY


def main(root1, root2, visit, ccd, root=None, showMatch=False):

    # get the name of the rerun
    rerun = os.path.split(root2)[-1]
    if rerun is '':
        rerun = 'synpipe'

    # get the image array before the fake objects are added
    if root is not None:
        root1 = os.path.join(root, root1)
        root2 = os.path.join(root, root2)

    imgBefore = getExpArray(root1, visit, ccd)
    imgAfter = getExpArray(root2, visit, ccd)

    # get the difference between the two image
    imgDiff = (imgAfter - imgBefore)

    # get the X, Y lists of noMatch stars
    if showMatch:
        noMatches = getNoMatchXY(root2, visit, ccd)
        noMatchX, noMatchY, fakeX, fakeY, badKronX, badKronY = noMatches

    # stretch it with arcsinh and make a png with pyplot
    fig, axes = pyplot.subplots(1, 3, sharex=True,
                                sharey=True,
                                figsize=(15, 10))
    pyplot.subplots_adjust(left=0.04, bottom=0.03,
                           right=0.99, top=0.97,
                           wspace=0.01, hspace=0.01)

    imgs = imgBefore, imgAfter, imgDiff
    titles = "Before", "After", "Diff"
    for i in range(3):
        print '### Plot : ', i
        axes[i].imshow(np.arcsinh(imgs[i]), cmap='gray')
        axes[i].set_title(titles[i])
        if showMatch:
            area1 = np.pi * 6 ** 2
            # area2 = np.pi * 4 ** 2
            axes[i].scatter(fakeX, fakeY, s=area1, facecolors='none',
                            edgecolors='g', alpha=0.9)

    pyplot.gcf().savefig("%s-%d-%s.png" % (rerun, visit, str(ccd)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("root1",
                        help="Root directory of data before adding fakes!")
    parser.add_argument("root2",
                        help="Root directory of data after adding fakes")
    parser.add_argument("visit", type=int, help="Visit to show")
    parser.add_argument("ccd", type=int, help="CCD to show")
    parser.add_argument("-r", "--root",
                        help="Master root directory",
                        default=None)
    args = parser.parse_args()

    main(args.root1, args.root2, args.visit, args.ccd,
         root=args.root)
