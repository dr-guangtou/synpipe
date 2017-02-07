#!/usr/bin/env python
# encoding: utf-8

import numpy as np

import pyfits as fits

import lsst.afw.geom as afwGeom
import lsst.afw.math as afwMath
import lsst.afw.coord as afwCoord
import lsst.afw.image as afwImage
import lsst.pex.config as afwConfig

from lsst.pipe.tasks.fakes import FakeSourcesConfig, FakeSourcesTask

import FakeSourceLib as fsl


class PositionStarFakesCoaddConfig(FakeSourcesConfig):
    starList = afwConfig.Field(dtype=str,
                               doc="Catalog of stars with mags ra/dec")
    seed = afwConfig.Field(dtype=int, default=1,
                           doc="Seed for random number generator")


class PositionStarFakesCoaddTask(FakeSourcesTask):
    ConfigClass = PositionStarFakesCoaddConfig

    def __init__(self, **kwargs):
        FakeSourcesTask.__init__(self, **kwargs)
        print "RNG seed:", self.config.seed
        self.rng = afwMath.Random(self.config.seed)
        self.npRand = np.random.RandomState(self.config.seed)
        try:
            self.starData = fits.open(self.config.starList)[1].data
        except Exception:
            raise

    def run(self, exposure, background):

        self.log.info("Adding fake stars at real positions")
        psf = exposure.getPsf()
        psfBBox = psf.computeImage().getBBox()
        margin = max(psfBBox.getWidth(), psfBBox.getHeight())/2 + 1

        PARENT = afwImage.PARENT
        md = exposure.getMetadata()
        expBBox = exposure.getBBox(PARENT)
        wcs = exposure.getWcs()

        for istar, star in enumerate(self.starData):
            try:
                starident = star["ID"]
            except KeyError:
                starident = istar + 1

            try:
                flux = exposure.getCalib().getFlux(float(star['mag']))
            except KeyError:
                raise KeyError("No mag column in %s" % self.config.starList)

            try:
                starCoord = afwCoord.Coord(afwGeom.Point2D(star['RA'],
                                                           star['DEC']))
            except KeyError:
                raise("No RA/DEC column in %s table" % self.config.starList)

            starXY = wcs.skyToPixel(starCoord)
            bboxI = exposure.getBBox(PARENT)
            bboxI.grow(margin)
            if not bboxI.contains(afwGeom.Point2I(starXY)):
                continue

            starImage = psf.computeImage(starXY)
            starImage *= flux
            starBBox = starImage.getBBox(PARENT)

            # Check that we're within the larger exposure, otherwise crop
            if expBBox.contains(starBBox) is False:
                newBBox = starImage.getBBox(PARENT)
                newBBox.clip(expBBox)
                if newBBox.getArea() <= 0:
                    self.log.info("Skipping fake %d" % starident)
                    continue
                self.log.info("Cropping FAKE%d from %s to %s" % (starident,
                              str(starBBox), str(newBBox)))
                starImage = starImage.Factory(starImage, newBBox, PARENT)
                starBBox = newBBox

            #starMaskedImage = fsl.addNoise(starImage.convertF(),
            #                               exposure.getDetector(),
            #                               rand_gen=self.npRand)
            #starMaskedImage = starImage

            #starMaskedImage.getMask().set(self.bitmask)

            md.set("FAKE%s" % str(starident), "%.3f, %.3f" % (starXY.getX(),
                                                              starXY.getY()))
            self.log.info("Adding fake %s at: %.1f,%.1f" % (str(starident),
                                                            starXY.getX(),
                                                            starXY.getY()))

            maskedImage = exposure.getMaskedImage()
            BBox = starImage.getBBox(PARENT)
            subMaskedImage = maskedImage.Factory(exposure.getMaskedImage(),
                                                 BBox,
                                                 PARENT)
            subMaskedImage += starImage
