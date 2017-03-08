#!/usr/bin/env python
# encoding: utf-8

import os
import fcntl

import numpy as np
import pyfits as fits

import lsst.afw.image
import lsst.afw.geom
import lsst.afw.math
import lsst.afw.cameraGeom
import lsst.afw.coord
import lsst.pex.config as lsstConfig

from lsst.pipe.tasks.fakes import FakeSourcesConfig, FakeSourcesTask

import FakeSourceLib as fsl
import makeFakeGalaxy as makeFake


class PositionGalSimFakesConfig(FakeSourcesConfig):
    galList = lsstConfig.Field(dtype=str,
                               doc="catalog of galaxies to add")
    maxMargin = lsstConfig.Field(dtype=int, default=600,
                                 optional=True,
                                 doc="Size of margin")
    seed = lsstConfig.Field(dtype=int, default=1,
                            doc="Seed for random number generator")
    addShear = lsstConfig.Field(dtype=bool, default=False,
                                doc='include shear in the galaxies')
    addMask = lsstConfig.Field(dtype=bool, default=False,
                               doc='add FAKE mask plane')
    sersic_prec = lsstConfig.Field(dtype=float, default=0.0,
                                   doc='The desired precision for n')
    cosStr = 'Use Galsim.COSMOSlog()'
    serStr = 'Single sersic galaxies added'
    dSerStr = 'Double sersic galaxies added'
    realStr = 'Real HST galaxy images added'
    galType = lsstConfig.ChoiceField(dtype=str, default='sersic',
                                     allowed={'dsersic': dSerStr,
                                              'sersic': serStr,
                                              'real': realStr,
                                              'cosmos': cosStr},
                                     doc='type of GalSim galaxies to add')
    exclusionLevel = lsstConfig.ChoiceField(dtype=str, default='none',
                                            allowed={'none': "None",
                                                     'marginal': "Marginal",
                                                     'bad_stamp': "Bad Stamp",
                                                     'bad_fits': "Bad Fits"},
                                            doc='Exclusion level')


class PositionGalSimFakesTask(FakeSourcesTask):
    ConfigClass = PositionGalSimFakesConfig

    def __init__(self, **kwargs):
        FakeSourcesTask.__init__(self, **kwargs)
        print "RNG seed:", self.config.seed
        self.rng = lsst.afw.math.Random(self.config.seed)
        self.npRand = np.random.RandomState(self.config.seed)
        self.galData = fits.open(self.config.galList)[1].data

    def run(self, exposure, background):
        self.log.info("Adding fake galaxies at real positions")
        PARENT = lsst.afw.image.PARENT
        psf = exposure.getPsf()
        md = exposure.getMetadata()
        calib = exposure.getCalib()
        expBBox = exposure.getBBox(PARENT)
        wcs = exposure.getWcs()
        skyToPixelMatrix = (wcs.getLinearTransform().invert().getMatrix() /
                            3600.0)

        """Deal with the skipped ones."""
        skipLog = 'runAddFake.skipped'
        if not os.path.isfile(skipLog):
            os.system('touch ' + skipLog)

        if self.config.galType is 'cosmos':
            import galsim
            exLevel = self.config.exclusionLevel
            cosmosCat = galsim.COSMOSCatalog(exclusion_level=exLevel)
        else:
            cosmosCat = None

        for igal, gal in enumerate(self.galData):
            try:
                galident = gal["ID"]
            except KeyError:
                galident = igal + 1

            try:
                flux = calib.getFlux(float(gal['mag']))
            except KeyError:
                raise KeyError("No mag column in %s" % self.config.galList)

            try:
                coordAdd = lsst.afw.geom.Point2D(gal['RA'], gal['DEC'])
                galCoord = lsst.afw.coord.Coord(coordAdd)
            except KeyError:
                raise("No RA/DEC column in %s table" % self.config.galList)

            galXY = wcs.skyToPixel(galCoord)
            bboxI = exposure.getBBox(PARENT)
            bboxI.grow(self.config.maxMargin)
            if not bboxI.contains(lsst.afw.geom.Point2I(galXY)):
                # Will just skip this object
                continue

            # Check the magnitude
            if gal['mag'] <= 0:
                self.log.info("Mag <= 0: Skipping %d" % galident)
                self.log.info("  mag: %7.3d" % gal['mag'])
                with open(skipLog, "a") as slog:
                    try:
                        fcntl.flock(slog, fcntl.LOCK_EX)
                        slog.write("%8d , negMag\n" % galident)
                        fcntl.flock(slog, fcntl.LOCK_UN)
                    except IOError:
                        continue
                continue

            # This is extrapolating for the PSF, probably not a good idea
            #  Return an Image of the PSF, in a form suitable for convolution.
            #  The returned image is normalized to sum to unity.
            psfImage = psf.computeKernelImage(galXY)
            try:
                addShear = self.config.addShear
                prec = self.config.sersic_prec
                galType = self.config.galType
                if self.config.galType is not 'cosmos':
                    galArray = makeFake.makeGalaxy(flux, gal,
                                                   psfImage.getArray(),
                                                   galType=galType,
                                                   cosmosCat=None,
                                                   calib=None,
                                                   addShear=addShear,
                                                   transform=skyToPixelMatrix)
                else:
                    galArray = makeFake.makeGalaxy(flux, gal,
                                                   psfImage.getArray(),
                                                   cosmosCat=cosmosCat,
                                                   calib=calib,
                                                   galType=galType,
                                                   addShear=addShear,
                                                   sersic_prec=prec,
                                                   transform=skyToPixelMatrix)
            except IndexError as ierr:
                self.log.info("GalSim Index Error: Skipping %d" % galident)
                self.log.info(ierr.message)
                with open(skipLog, "a") as slog:
                    try:
                        fcntl.flock(slog, fcntl.LOCK_EX)
                        slog.write("%8d , galsimI\n" % galident)
                        fcntl.flock(slog, fcntl.LOCK_UN)
                    except IOError:
                        continue
                continue
            except KeyError as kerr:
                self.log.info("GalSim Key Error: Skipping %d" % galident)
                self.log.info(kerr.message)
                with open(skipLog, "a") as slog:
                    try:
                        fcntl.flock(slog, fcntl.LOCK_EX)
                        slog.write("%8d , galsimK\n" % galident)
                        fcntl.flock(slog, fcntl.LOCK_UN)
                    except IOError:
                        continue
                continue
            except ValueError as verr:
                self.log.info("GalSim Value Error: Skipping %d" % galident)
                self.log.info(verr.message)
                with open(skipLog, "a") as slog:
                    try:
                        fcntl.flock(slog, fcntl.LOCK_EX)
                        slog.write("%8d , galsimV\n" % galident)
                        fcntl.flock(slog, fcntl.LOCK_UN)
                    except IOError:
                        continue
                continue
            except RuntimeError as rerr:
                self.log.info("GalSim Runtime Error: Skipping %d" % galident)
                self.log.info(rerr.message)
                with open(skipLog, "a") as slog:
                    try:
                        fcntl.flock(slog, fcntl.LOCK_EX)
                        slog.write("%8d , galsimR\n" % galident)
                        fcntl.flock(slog, fcntl.LOCK_UN)
                    except IOError:
                        continue
                continue
            except Exception as uerr:
                self.log.info("Unexpected Error: Skipping %d" % galident)
                self.log.info(uerr.message)
                with open(skipLog, "a") as slog:
                    try:
                        fcntl.flock(slog, fcntl.LOCK_EX)
                        slog.write("%8d , Unexpected\n" % galident)
                        fcntl.flock(slog, fcntl.LOCK_UN)
                    except IOError:
                        continue
                continue

            galImage = lsst.afw.image.ImageF(galArray.astype(np.float32))
            galBBox = galImage.getBBox(PARENT)
            galX0 = (galXY.getX() - galBBox.getWidth()/2.0 + 0.5)
            galY0 = (galXY.getY() - galBBox.getHeight()/2.0 + 0.5)
            galImage = lsst.afw.math.offsetImage(galImage,
                                                 galX0, galY0,
                                                 'lanczos3')
            galBBox = galImage.getBBox(PARENT)

            # Check that we're within the larger exposure, otherwise crop
            parentBox = galImage.getBBox(PARENT)
            if expBBox.contains(parentBox) is False:
                newBBox = galImage.getBBox(PARENT)
                newBBox.clip(expBBox)
                if newBBox.getArea() <= 0:
                    self.log.info("BBoxEdge Error: Skipping %d" % galident)
                    with open(skipLog, "a") as slog:
                        try:
                            fcntl.flock(slog, fcntl.LOCK_EX)
                            slog.write("%8d , bboxEdge\n" % galident)
                            fcntl.flock(slog, fcntl.LOCK_UN)
                        except IOError:
                            continue
                    continue
                self.log.info("Cropping FAKE%d from %s to %s" % (galident,
                              str(galBBox), str(newBBox)))
                galImage = galImage.Factory(galImage, newBBox,
                                            PARENT)
                galBBox = newBBox

            # Add Noise: Optional?
            galMaskedImage = fsl.addNoise(galImage, exposure.getDetector(),
                                          rand_gen=self.npRand)

            # Put information of the added fake galaxies into the header
            md.set("FAKE%s" % str(galident), "%.3f, %.3f" % (galXY.getX(),
                                                             galXY.getY()))
            self.log.info("Adding fake %s at: %.1f,%.1f" % (str(galident),
                                                            galXY.getX(),
                                                            galXY.getY()))

            galMaskedImage.getMask().set(self.bitmask)
            try:
                galMaskedImage.getMask().removeAndClearMaskPlane('FAKE',
                                                                 True)
            except Exception:
                pass
            try:
                galMaskedImage.getMask().removeAndClearMaskPlane('CROSSTALK',
                                                                 True)
            except Exception:
                pass
            try:
                galMaskedImage.getMask().removeAndClearMaskPlane('UNMASKEDNAN',
                                                                 True)
            except Exception:
                pass

            maskedImage = exposure.getMaskedImage()
            try:
                maskedImage.getMask().removeAndClearMaskPlane('CROSSTALK',
                                                              True)
            except Exception:
                pass
            try:
                maskedImage.getMask().removeAndClearMaskPlane('UNMASKEDNAN',
                                                              True)
            except Exception:
                pass
            try:
                maskedImage.getMask().removeAndClearMaskPlane('FAKE', True)
            except Exception:
                pass

            BBox = galMaskedImage.getBBox(PARENT)
            subMaskedImage = maskedImage.Factory(exposure.getMaskedImage(),
                                                 BBox,
                                                 PARENT)
            subMaskedImage += galMaskedImage

            """
            #
            galMaskedImage.getMask().set(self.bitmask)

            maskedImage = exposure.getMaskedImage()
            try:
                maskedImage.getMask().removeAndClearMaskPlane('CROSSTALK',
                                                              True)
            except Exception:
                pass
            try:
                maskedImage.getMask().removeAndClearMaskPlane('UNMASKEDNAN',
                                                              True)
            except Exception:
                pass
            try:
                maskedImage.getMask().removeAndClearMaskPlane('FAKE', True)
            except Exception:
                pass
            """
