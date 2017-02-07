import random
import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
import lsst.afw.table as afwTable
import lsst.afw.image as afwImage
import lsst.meas.algorithms as measAlg
import lsst.afw.detection as afwDetect

#WARNING: if you want to add configuration variables (maybe how close you are
#to a fake object), you will need to deal with the fact that the configuration
#for a retargeted subtask (like this one) blows away any overrides in setDefault of
#the parent task (processCoadd in this case) and, it seems any camera specific
#overrides in $OBS_SUBARU/config/hsc/processCcd.py.
#See https://dev.lsstcorp.org/trac/ticket/2282 for more details
#I think you need something like cmdLineTask.applyOverrides to deal with this

class OnlyFakesDetectionConfig(measAlg.SourceDetectionTask.ConfigClass):
    dummyVar = pexConfig.Field(doc='Dummy config variable, does nothing',
                               dtype=bool, default=True)

class OnlyFakesDetectionTask(measAlg.SourceDetectionTask):
    """This task serves culls the source list to sources which overlap with fakes"""

    ##WARNING: we are using the parent configuration class instead of the
    ##OnlyFakesDetectionConfig to avoid having to fix overridden config parameters
    ##from processCoaddConfig.setDefaults and from the camera-specific $OBS_SUBARU/config
    ConfigClass = measAlg.SourceDetectionConfig

    def makeSourceCatalog(self, table, exposure, doSmooth=True, sigma=None, clearMask=True):
        if self.negativeFlagKey is not None and self.negativeFlagKey not in table.getSchema():
            raise ValueError("Table has incorrect Schema")

        # detect the footprints as usual
        fpSets = self.detectFootprints(exposure=exposure, doSmooth=doSmooth, sigma=sigma,
                                       clearMask=clearMask)

        #ignore objects whose footprints do NOT overlap with the 'FAKE' mask
        mask = exposure.getMaskedImage().getMask()
        fakebit = mask.getPlaneBitMask('FAKE')
        fpPos = fpSets.positive.getFootprints()
        removes = []
        for i_foot, foot in enumerate(fpPos):
            footTmp = afwDetect.Footprint(foot)
            footTmp.intersectMask(mask, fakebit)
            if footTmp.getArea() == foot.getArea():
                removes.append(i_foot)
        removes = sorted(removes, reverse=True)
        for r in removes:
            del fpPos[r]

        self.log.info("Found %d sources near fake footprints"% len(fpPos))

        fpSets.numPos = len(fpPos)
        if fpSets.negative:
            del fpSets.negative.getFootprints()[0:]
            fpSets.negative = None

        # make sources
        sources = afwTable.SourceCatalog(table)
        table.preallocate(fpSets.numPos)
        if fpSets.positive:
            fpSets.positive.makeSources(sources)

        return pipeBase.Struct(sources=sources, fpSets=fpSets)

