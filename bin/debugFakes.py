#!/usr/bin/env python
"""
Command-line task that adds fake sources to an already existing (calibrated) exposure.
By default, the fakes is targeted to a dummy task that does nothing, so fakes needs to be retargeted to a task that actually adds sources. 
This task creates a new rerun with fake sources added to the CORR files. You have the option of displaying the outputs in ds9 immediately after creation, but be careful if you multiprocess with that. This is really designed for debugging. If you want a task that adds fakes and scales well use runAddFakes.py
"""

import numpy
import lsst.pipe.base  as pipeBase
import lsst.pex.config as pexConfig
import lsst.daf.persistence as dafPersist
import lsst.pipe.tasks.coaddBase as coaddBase
from lsst.pipe.tasks.fakes import DummyFakeSourcesTask
import lsst.afw.display.ds9 as ds9

class DebugFakesConfig(pexConfig.Config):
    coaddName = pexConfig.ChoiceField(
        dtype   = str,
        doc     = "Type of data to use",
        default = "deep",
        allowed = {"deep"   : "deepCoadd"}
        )
    fakes = pexConfig.ConfigurableField(
        target = DummyFakeSourcesTask,
        doc = "Injection of fake sources for test purposes (retarget to enable)"
    )
    display = pexConfig.Field(dtype=bool, doc='display exposure', default=False)

butlerTarget = "raw"
dataIdContainer  = {
    "raw":              pipeBase.DataIdContainer,
    "src":              pipeBase.DataIdContainer,
    "deepCoadd":        coaddBase.ExistingCoaddDataIdContainer,
    "deepCoadd_skyMap": coaddBase.ExistingCoaddDataIdContainer,
    "wcs":              coaddBase.ExistingCoaddDataIdContainer,
}
    
class DebugFakesTask(pipeBase.CmdLineTask):

    _DefaultName = "DebugFakes"
    ConfigClass  = DebugFakesConfig

    # we need to kill each of these methods so the users won't
    # mess with persisted configs and version info
    def _getConfigName(self):
        return None
    def _getEupsVersionsName(self):
        return None
    def _getMetadataName(self):
        return None

    @classmethod
    def _makeArgumentParser(cls):
        parser = pipeBase.ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument("--id", butlerTarget, help="Data ID, e.g. --id tract=1234 patch=2,2",
                               ContainerClass=dataIdContainer[butlerTarget])
        return parser
    

    def __init__(self, **kwargs):
        pipeBase.CmdLineTask.__init__(self, **kwargs)
        self.makeSubtask("fakes")

    def run(self, dataRef, **kwargs):
        self.log.info("Processing %s" % (dataRef.dataId))
        exposure = dataRef.get('calexp', immediate=True)
        self.fakes.run(exposure, None)
        dataRef.put(exposure, "calexp")
        if self.config.display:
            ds9.mtv(exposure, settings={'scale':'zscale', 'zoom':'to fit',
                                        'mask':'transparency 80', 'wcs':'wcs'})
        return 0


if __name__ == '__main__':
    DebugFakesTask.parseAndRun()

    
