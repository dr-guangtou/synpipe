import lsst.afw.image
import lsst.afw.geom
import lsst.afw.math
import lsst.pex.config
from lsst.pipe.tasks.fakes import FakeSourcesConfig, FakeSourcesTask

import FakeSourceLib as fsl
import numpy as np

class RandomStarFakeSourcesConfig(FakeSourcesConfig):
    nStars = lsst.pex.config.Field(dtype=int, default=1,
                                   doc="Number of stars to add")
    magnitude = lsst.pex.config.Field(dtype=float, default=20.0,
                                      doc="Magnitude of all stars to be added")
    margin = lsst.pex.config.Field(dtype=int, default=None, optional=True,
                                   doc="Size of margin at edge that should not be added")
    seed = lsst.pex.config.Field(dtype=int, default=0,
                                 doc="Seed for random number generator")


class RandomStarFakeSourcesTask(FakeSourcesTask):
    ConfigClass = RandomStarFakeSourcesConfig

    def __init__(self, **kwargs):
        FakeSourcesTask.__init__(self, **kwargs)
        print "RNG seed:", self.config.seed
        self.rng = lsst.afw.math.Random(self.config.seed)
        self.npRand = np.random.RandomState(self.config.seed)

    def run(self, exposure, background):

        self.log.info("Adding fake random stars")
        psf = exposure.getPsf()
        psfBBox = psf.computeImage().getBBox()
        margin = max(psfBBox.getWidth(), psfBBox.getHeight())/2 + 1
        if self.config.margin is not None:
            if self.config.margin < margin:
                raise ValueError("margin is not large enough for PSF")
        bboxI = exposure.getBBox(lsst.afw.image.PARENT)
        bboxI.grow(-margin)
        bboxD = lsst.afw.geom.BoxD(bboxI)
        flux = exposure.getCalib().getFlux(self.config.magnitude)
        md = exposure.getMetadata()
        for i in range(self.config.nStars):
            x = self.rng.flat(bboxD.getMinX(), bboxD.getMaxX())
            y = self.rng.flat(bboxD.getMinY(), bboxD.getMaxY())
            md.set("FAKE%d" % i, "%.3f, %.3f" % (x, y))
            self.log.info("Adding fake at: %.1f,%.1f"% (x, y))
            psfImage = psf.computeImage(lsst.afw.geom.Point2D(x, y))
            psfImage *= flux
            psfMaskedImage = fsl.addNoise(psfImage.convertF(), exposure.getDetector(), rand_gen=self.npRand)

            mask = psfMaskedImage.getMask()
            mask.set(self.bitmask)

            # the line below would work if the subimage call worked in PARENT coordinates.
            # Since it doesn't at present, we have to do the longer call below.
            # subMaskedImage = exposure.getMaskedImage()[psfImage.getBBox(lsst.afw.image.PARENT)]
            subMaskedImage = exposure.getMaskedImage().Factory(exposure.getMaskedImage(),
                                                               psfImage.getBBox(lsst.afw.image.PARENT),
                                                               lsst.afw.image.PARENT)
            subMaskedImage += psfMaskedImage
