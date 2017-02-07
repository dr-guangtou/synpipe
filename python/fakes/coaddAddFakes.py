#!/usr/bin/env python
# encoding: utf-8

import os
# import math
import fcntl
# import collections

import lsst.pex.config
# import lsst.afw.cameraGeom as afwCg
from lsst.pex.config import Config, Field

from lsst.pipe.base import ArgumentParser
from lsst.pipe.tasks.fakes import DummyFakeSourcesTask

import hsc.pipe.base.butler as hscButler
# from hsc.pipe.base.butler import getDataRef
from hsc.pipe.tasks.stack import TractDataIdContainer

from hsc.pipe.base.pool import abortOnError, Pool, Debugger
from hsc.pipe.base.parallel import BatchPoolTask


"""
DummyFakeSourcesTask:

A stand-in for FakeSourcesTask that doesn't do anything, to be used
as the default (to disable fake injection) anywhere FakeSourcesTask
could be used.
"""

Debugger().enabled = True


class coaddAddFakesConfig(lsst.pex.config.Config):
    """Configs of the addFakeTask."""
    coaddName = Field(dtype=str, default="deep", doc="Name of coadd")
    fakes = lsst.pex.config.ConfigurableField(
        target=DummyFakeSourcesTask,
        doc="Injection of fake sources to processed Patches"
    )
    ignorePatchList = lsst.pex.config.ListField(dtype=int, default=[],
                                                doc="List of Patches \
                                                        to ignore")


def unpickle(factory, args, kwargs):
    """Unpickle something by calling a factory"""
    return factory(*args, **kwargs)


class coaddAddFakesTask(BatchPoolTask):
    """
    Add fakes to entire exposure at once.

    Parameters:
    """
    RunnerClass = hscButler.ButlerTaskRunner
    ConfigClass = coaddAddFakesConfig
    _DefaultName = "CoaddAddFakes"

    """ Song Huang; Log to keep record of the missing CCDs """
    missingLog = 'runCoaddAddFake.missingPatch'
    if not os.path.isfile(missingLog):
        dum = os.system('touch ' + missingLog)

    # we need to kill each of these methods so the users won't
    # mess with persisted configs and version info
    def _getConfigName(self):
        return None

    def _getEupsVersionsName(self):
        return None

    def _getMetadataName(self):
        return None

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        calls BatchPoolTask construtor, and setups up fakes subTask
        """
        super(coaddAddFakesTask, self).__init__(*args, **kwargs)
        self.makeSubtask("fakes")

    def __reduce__(self):
        """Pickler"""
        return unpickle, (self.__class__, [], dict(config=self.config,
                                                   name=self._name,
                                                   parentTask=self._parentTask,
                                                   log=self.log,
                                                   butler=self.butler))

    @classmethod
    def batchWallTime(cls, time, parsedCmd, numNodes, numProcs):
        """
        Over-ridden method that gives the requested wall time for the method.

        Probably not necessary here as this task is fast
        """
        """TODO: Not sure if this is correct"""
        # numCcds = sum(1 for raft in parsedCmd.butler.get("camera")
        #               for ccd in afwCg.cast_Raft(raft))
        numTargets = 0
        for refList in parsedCmd.id.refList:
            numTargets += len(refList)
        return (time * numTargets / float(numNodes * numProcs))

    @classmethod
    def _makeArgumentParser(cls, *args, **kwargs):
        """
        Make the argument parser.

        Modified by Song Huang; To work on coadd images
        """
        kwargs.pop("doBatch", False)
        parser = ArgumentParser(name=cls._DefaultName, *args, **kwargs)
        parser.add_id_argument("--id", "deepCoadd_calexp",
                               help="data ID, e.g. --id tract=12345",
                               ContainerClass=TractDataIdContainer)
        return parser

    @abortOnError
    def run(self, patchRefList, butler):
        """
        Set up the pool and scatters the processing of the individual Patches.

        """
        for patchRef in patchRefList:
            if patchRef:
                butler = patchRef.getButler()
                break
        else:
            raise RuntimeError("No valid patch")

        pool = Pool(self._DefaultName)
        pool.cacheClear()
        pool.storeSet(butler=butler)

        patchRefList = [patchRef for patchRef in patchRefList if
                        patchRef.datasetExists(self.config.coaddName +
                                               "Coadd_calexp") and
                        patchRef.datasetExists(self.config.coaddName +
                                               "Coadd_det")]
        dataIdList = [patchRef.dataId for patchRef in patchRefList]

        # Group by patch
        patches = {}
        tract = None
        for patchRef in patchRefList:
            dataId = patchRef.dataId
            if tract is None:
                tract = dataId['tract']
            else:
                assert tract == dataId['tract']

            patch = dataId["patch"]
            if patch not in patches:
                patches[patch] = []
            patches[patch].append(dataId)

        # Scatter: process CCDs independently
        outList = pool.map(self.process, dataIdList)

        numGood = sum(1 for s in outList if s == 0)
        if numGood == 0:
            self.log.warn("Failed on ALL Patches!")
            return

    def process(self, cache, dataId):
        """
        Add fakes to individual Patch.

        Return None if we are skipping the Patch
        """
        cache.result = None
        ignorePatchList = self.config.ignorePatchList
        #if dataId["patch"] in ignorePatchList:
        #    self.log.warn("Ignoring %s Patch" % (dataId,))
        #    return None
        """
        Try to deal with missing CCDs gracefully
        Song Huang
        """
        #try:
        self.log.info("Reading...%s" % (dataId,))
        dataRef = hscButler.getDataRef(cache.butler, dataId,
                                       self.config.coaddName + 'Coadd_calexp')

        with self.logOperation("processing %s" % (dataId,)):
            self.log.info("Loading... %s" % (dataId,))
            exposure = dataRef.get(self.config.coaddName + 'Coadd_calexp',
                                   immediate=True)
            self.log.info("Running... %s" % (dataId,))
            self.fakes.run(exposure, None)
            self.log.info("Finishing... %s" % (dataId,))

            """ Remove unused mask plane CR, and UNMASKEDNAN """
            self.log.info("Removing unused mask plane")
            maskPlane = exposure.getMaskedImage().getMask()
            try:
                maskPlane.removeAndClearMaskPlane('CROSSTALK', True)
            except Exception:
                self.log.info("Can not remove the CROSSTALK plane")
            try:
                maskPlane.removeAndClearMaskPlane('UNMASKEDNAN', True)
            except Exception:
                self.log.info("Can not remove the UNMASKEDNAN plane")
            dataRef.put(exposure, "deepCoadd_calexp")
        return 0
        #except Exception, errMsg:
        #    with open(self.missingLog, "a") as mlog:
        #        try:
        #            mlog.write("%s !" % (dataId))
        #            fcntl.flock(mlog, fcntl.LOCK_UN)
        #        except IOError:
        #            pass
        #    self.log.warn(str(errMsg))
        #    self.log.warn("Something is wrong for %s" % (dataId,))
        #    return None
