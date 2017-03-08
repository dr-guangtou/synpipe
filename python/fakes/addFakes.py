#!/usr/bin/env python
# encoding: utf-8

import os
import math
import fcntl
import collections

import lsst.pex.config
import lsst.afw.cameraGeom as afwCg

from lsst.pipe.base import ArgumentParser
from lsst.pipe.tasks.fakes import DummyFakeSourcesTask

import hsc.pipe.base.butler as hscButler
from hsc.pipe.base.pool import abortOnError, Pool, Debugger
from hsc.pipe.base.parallel import BatchPoolTask


"""
DummyFakeSourcesTask:

A stand-in for FakeSourcesTask that doesn't do anything, to be used
as the default (to disable fake injection) anywhere FakeSourcesTask
could be used.
"""

Debugger().enabled = True


class addFakesConfig(lsst.pex.config.Config):
    """Configs of the addFakeTask."""

    fakes = lsst.pex.config.ConfigurableField(
        target=DummyFakeSourcesTask,
        doc="Injection of fake sources to processed visits"
    )
    ignoreCcdList = lsst.pex.config.ListField(dtype=int, default=[],
                                              doc="List of CCDs to ignore")


class addFakesTask(BatchPoolTask):
    """
    Add fakes to entire exposure at once.

    Parameters:
    """
    RunnerClass = hscButler.ButlerTaskRunner
    ConfigClass = addFakesConfig
    _DefaultName = "AddFakes"

    """ Song Huang; Log to keep record of the missing CCDs """
    missingLog = 'runAddFake.missingCCD'
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
        super(addFakesTask, self).__init__(*args, **kwargs)
        self.makeSubtask("fakes")

    @classmethod
    def batchWallTime(cls, time, parsedCmd, numNodes, numProcs):
        """
        Over-ridden method that gives the requested wall time for the method.

        Probably not necessary here as this task is fast
        """
        numCcds = sum(1 for raft in parsedCmd.butler.get("camera")
                      for ccd in afwCg.cast_Raft(raft))
        numCycles = int(math.ceil(numCcds/float(numNodes*numProcs)))
        numExps = len(cls.RunnerClass.getTargetList(parsedCmd))
        return time*numExps*numCycles

    @classmethod
    def _makeArgumentParser(cls, *args, **kwargs):
        """
        Make the argument parser.

        this task won't work for tracts/patches as it's currently written
        """
        kwargs.pop("doBatch", False)
        parser = ArgumentParser(name=cls._DefaultName, *args, **kwargs)
        parser.add_id_argument("--id", datasetType="raw", level="visit",
                               help="data ID, e.g. --id visit=12345")
        return parser

    @abortOnError
    def run(self, expRef, butler):
        """
        Set up the pool and scatters the processing of the individual CCDs.

        In processCcd, apparently all nodes (master and slaves) run this
        method, but I don't really get that

        on the gather, we just check that any of the sources ran
        """
        pool = Pool(self._DefaultName)
        pool.cacheClear()
        pool.storeSet(butler=butler)

        dataIdList = dict([(ccdRef.get("ccdExposureId"), ccdRef.dataId)
                           for ccdRef in expRef.subItems("ccd") if
                           ccdRef.datasetExists("raw")])
        dataIdList = collections.OrderedDict(sorted(dataIdList.items()))

        # Scatter: process CCDs independently
        outList = pool.map(self.process, dataIdList.values())
        numGood = sum(1 for s in outList if s == 0)
        if numGood == 0:
            self.log.warn("All CCDs in exposure failed")
            return

    def process(self, cache, dataId):
        """
        Add fakes to individual CCDs.

        Return None if we are skipping the CCD
        """
        cache.result = None
        ignoreCcdList = self.config.ignoreCcdList
        if (dataId["ccd"] in ignoreCcdList) or (dataId['ccd'] > 103):
            self.log.warn("Ignoring %s: CCD in ignoreCcdList" % (dataId,))
            return None
        """
        Try to deal with missing CCDs gracefully
        Song Huang
        """
        try:
            dataRef = hscButler.getDataRef(cache.butler, dataId)
            ccdId = dataRef.get("ccdExposureId")

            with self.logOperation("processing %s (ccdId=%d)" % (dataId,
                                                                 ccdId)):
                self.log.info("Loading... %s - %s" % (dataId, ccdId))
                exposure = dataRef.get('calexp', immediate=True)

                self.log.info("Running... %s - %s" % (dataId, ccdId))
                self.fakes.run(exposure, None)
                self.log.info("Finishing... %s - %s" % (dataId, ccdId))

                """ Remove unused mask plane CR, and UNMASKEDNAN """
                self.log.info("Removing unused mask plane")

                try:
                    exposure.getMaskedImage().getMask().removeAndClearMaskPlane('UNMASKEDNAN', True)
                except Exception:
                    self.log.info("Can not remove the UNMASKEDNAN plane")

                try:
                    exposure.getMaskedImage().getMask().removeAndClearMaskPlane('FAKE', True)
                except Exception:
                    self.log.info("Can not remove the FAKE plane")

                dataRef.put(exposure, "calexp")

            return 0
        except Exception, errMsg:
            with open(self.missingLog, "a") as mlog:
                try:
                    mlog.write("%s  ,  %d\n" % (dataId, ccdId))
                    fcntl.flock(mlog, fcntl.LOCK_UN)
                except IOError:
                    pass
            self.log.warn(str(errMsg))
            self.log.warn("Something is wrong for CCD %s (ccdId=%d)" % (dataId,
                                                                        ccdId))
            return None
