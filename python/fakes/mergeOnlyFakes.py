import copy
import random
import lsst.pex.config      as pexConfig
import lsst.pipe.base       as pipeBase
import lsst.afw.table       as afwTable
import lsst.afw.image       as afwImage
import lsst.meas.algorithms as measAlg
import lsst.afw.detection   as afwDetect
import lsst.pipe.tasks.multiBand as mBand

from lsst.pipe.tasks.coaddBase import getSkyInfo

#WARNING: if you want to add configuration variables (maybe how close you are
#to a fake object), you will need to deal with the fact that the configuration
#for a retargeted subtask (like this one) blows away any overrides in setDefault of
#the parent task (processCoadd in this case) and, it seems any camera specific
#overrides in $OBS_SUBARU/config/hsc/processCcd.py.
#See https://dev.lsstcorp.org/trac/ticket/2282 for more details
#I think you need something like cmdLineTask.applyOverrides to deal with this

# Song Huang

class OnlyFakesMergeConfig(mBand.MeasureMergedCoaddSourcesTask.ConfigClass):
    dummyVar = pexConfig.Field(doc='Dummy config variable, does nothing',
                               dtype=bool, default=True)

class OnlyFakesMergeTask(mBand.MeasureMergedCoaddSourcesTask):
    """This task serves culls the source list to sources which overlap with fakes"""

    ##WARNING: we are using the parent configuration class instead of the
    ##OnlyFakesMergeConfig to avoid having to fix overridden config parameters
    ConfigClass = mBand.MeasureMergedCoaddSourcesConfig

    def run(self, patchRef):
        """Measure and deblend"""

        exposure = patchRef.get(self.config.coaddName + "Coadd", immediate=True)

        """Read in the FAKE mask plane"""
        mask = exposure.getMaskedImage().getMask()
        fakebit = mask.getPlaneBitMask('FAKE')

        sources = self.readSources(patchRef)
        self.log.info("Found %d sources"% len(sources))
        """ignore objects whose footprints do NOT overlap with the 'FAKE' mask"""
        removes = []
        for i_ss, ss in enumerate(sources):
            foot = ss.getFootprint()
            footTmp = afwDetect.Footprint(foot)
            footTmp.intersectMask(mask, fakebit)
            if footTmp.getArea() == foot.getArea():
                removes.append(i_ss)
        removes = sorted(removes, reverse=True)
        for r in removes:
            del sources[r]
        self.log.info("Found %d sources near fake footprints"% len(sources))

        if self.config.doDeblend:
            self.deblend.run(exposure, sources, exposure.getPsf())

            bigKey = sources.schema["deblend.parent-too-big"].asKey()
            numBig = sum((s.get(bigKey) for s in sources)) # catalog is non-contiguous so can't extract column
            if numBig > 0:
                self.log.warn("Patch %s contains %d large footprints that were not deblended" %
                              (patchRef.dataId, numBig))
        self.measurement.run(exposure, sources)
        skyInfo = getSkyInfo(coaddName=self.config.coaddName, patchRef=patchRef)
        self.setPrimaryFlags.run(sources, skyInfo.skyMap, skyInfo.tractInfo, skyInfo.patchInfo,
                                 includeDeblend=self.config.doDeblend)
        self.propagateFlags.run(patchRef.getButler(), sources, self.propagateFlags.getCcdInputs(exposure),
                                exposure.getWcs())
        if self.config.doMatchSources:
            self.writeMatches(patchRef, exposure, sources)

        self.write(patchRef, sources)
