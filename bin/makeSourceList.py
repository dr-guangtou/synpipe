#!/usr/bin/env python
"""make a source catalog of galaxies, possibly with shear."""
import os
import warnings

import numpy as np

import astropy.table

import lsst.pipe.base as pipeBase
import lsst.pex.config as pexConfig
import lsst.pipe.tasks.coaddBase as coaddBase

import fakes.makeRaDecCat as makeRaDecCat


class MakeFakeInputsConfig(pexConfig.Config):
    """Parse input for MakeFakeInputTask."""

    coaddName = pexConfig.ChoiceField(
        dtype=str,
        doc="Type of data to use",
        default="deep",
        allowed={"deep": "deepCoadd"}
        )
    rhoFakes = pexConfig.Field(doc="number of fakes per patch", dtype=int,
                               optional=False, default=500)
    inputCat = pexConfig.Field(
        doc="input galaxy catalog, if none just return ra/dec list",
        dtype=str,
        optional=True, default=None)
    outDir = pexConfig.Field(doc='output directory for catalogs',
                             dtype=str,
                             optional=True, default='.')
    rad = pexConfig.Field(doc="minimum distance between fake objects",
                          dtype=float, optional=True, default=None)
    acpMask = pexConfig.Field(doc='region to include',
                              dtype=str,
                              optional=True, default='')
    rejMask = pexConfig.Field(doc='region to mask out',
                              dtype=str,
                              optional=True, default='')
    innerTract = pexConfig.Field(doc='Only add to the inner Tract region',
                                 dtype=bool, optional=True, default=False)
    uniqueID = pexConfig.Field(doc='Use the index as unique ID',
                               dtype=bool, optional=False, default=True)


class MakeFakeInputsTask(pipeBase.CmdLineTask):

    """a task to make an input catalog of fake sources for a dataId."""

    _DefaultName = 'makeFakeInputs'
    ConfigClass = MakeFakeInputsConfig

    def run(self, dataRef):
        """Make input catalogs."""
        skyMap = dataRef.get('deepCoadd_skyMap', immediate=True)
        tractId = dataRef.dataId['tract']
        tract = skyMap[tractId]
        extPatch = tract.getNumPatches()
        nPatch = extPatch.getX() * extPatch.getY()
        nFakes = self.config.rhoFakes * nPatch
        ra_vert, dec_vert = zip(*tract.getVertexList())
        ra_vert = sorted(ra_vert)
        dec_vert = sorted(dec_vert)
        ra0 = ra_vert[0].asDegrees()
        ra1 = ra_vert[-1].asDegrees()
        dec0 = dec_vert[0].asDegrees()
        dec1 = dec_vert[-1].asDegrees()

        """
        Added by Song Huang 2016-09-02
        Tracts in the Deep and Wide layers are defined to have overlaps
        between the two adjacent Tracts: 1 arcmin ~ 0.01667 deg
        """
        if self.config.innerTract:
            # ra0 += 0.0167
            # ra1 -= 0.0167
            # dec0 += 0.0167
            # dec1 -= 0.0167
            ra0 += 0.09
            ra1 -= 0.09
            dec0 += 0.09
            dec1 -= 0.09

        radUse = self.config.rad
        raArr, decArr = np.array(zip(*makeRaDecCat.getRandomRaDec(nFakes,
                                                                  ra0,
                                                                  ra1,
                                                                  dec0,
                                                                  dec1,
                                                                  rad=radUse)))
        """
        Added by Song Huang 2016-09-01
        Filter the random RA, DEC using two filters
        """
        if (self.config.acpMask != '') or (self.config.rejMask != ''):
            try:
                from shapely import wkb
                from shapely.geometry import Point
                from shapely.prepared import prep

                # Filter through the accept mask
                acpUse = self.config.acpMask
                if (acpUse != '') and os.path.isfile(acpUse):
                    print "## Filter through : %s" % acpUse
                    acpWkb = open(acpUse, 'r')
                    acpRegs = wkb.loads(acpWkb.read().decode('hex'))
                    acpPrep = prep(acpRegs)
                    acpWkb.close()
                    inside = np.asarray(map(lambda x, y:
                                            acpPrep.contains(Point(x, y)),
                                        raArr, decArr))
                else:
                    inside = np.isfinite(raArr)

                # Filter through the reject mask
                rejUse = self.config.rejMask
                if (rejUse != '') and os.path.isfile(rejUse):
                    print "## Filter through : %s" % rejUse
                    rejWkb = open(rejUse, 'r')
                    rejRegs = wkb.loads(rejWkb.read().decode('hex'))
                    rejPrep = prep(rejRegs)
                    rejWkb.close()
                    masked = np.asarray(map(lambda x, y:
                                            rejPrep.contains(Point(x, y)),
                                        raArr, decArr))
                else:
                    masked = np.isnan(raArr)

                useful = np.asarray(map(lambda x, y: x and (not y),
                                    inside, masked))
                ra, dec = raArr[useful], decArr[useful]

                print "## %d out of %d objects left" % (len(ra), len(raArr))

            except ImportError:
                warnings.warn('Can not import Shapely, no filter performed!')
                ra, dec = raArr, decArr
        else:
            ra, dec = raArr, decArr

        # Number of fakes that will be added
        nFakes = len(ra)
        # Create an empty astropy.Table object
        outTab = astropy.table.Table()
        # Add columns for Ra, Dec
        outTab.add_column(astropy.table.Column(name="RA", data=ra))
        outTab.add_column(astropy.table.Column(name="Dec", data=dec))
        if self.config.inputCat is not None:
            galData = astropy.table.Table().read(self.config.inputCat)
            randInd = np.random.choice(range(len(galData)), size=nFakes)
            mergedData = galData[randInd]

            for colname in mergedData.columns:
                colAdd = astropy.table.Column(name=colname,
                                              data=mergedData[colname])
                outTab.add_column(colAdd)

            # Replace ID with a unique integer (using index)
            if ('ID' in outTab.colnames) and (self.config.uniqueID):
                outTab.rename_column('ID', 'modelID')
                outTab.add_column(astropy.table.Column(name="ID",
                                  data=np.arange(len(outTab))))
            elif ('ID' not in outTab.colnames):
                outTab.add_column(astropy.table.Column(name="ID",
                                  data=np.arange(len(outTab))))

            # Generate multiBand catalog at the same time
            magList = [col for col in galData.colnames if 'mag_' in col]
            if len(magList) >= 1:
                print "Find magnitude in %d band(s)" % len(magList)
                for mag in magList:
                    try:
                        outTab.remove_column('mag')
                    except KeyError:
                        pass
                    outTab.add_column(astropy.table.Column(name='mag',
                                      data=mergedData[mag]))
                    filt = mag.split('_')[1].upper()
                    outFits = os.path.join(self.config.outDir,
                                           'src_%d_radec_%s.fits' % (tractId,
                                                                     filt))
                    outTab.write(outFits, overwrite=True)
            else:
                outTab.write(os.path.join(self.config.outDir,
                                          'src_%d_radec.fits' % tractId),
                             overwrite=True)
        else:
            outTab.write(os.path.join(self.config.outDir,
                                      'src_%d_radec_only.fits' % tractId),
                         overwrite=True)

    @classmethod
    def _makeArgumentParser(cls, *args, **kwargs):
        parser = pipeBase.ArgumentParser(name="makeFakeInputs",
                                         *args, **kwargs)
        parser.add_id_argument("--id", datasetType="deepCoadd",
                               help="data ID, e.g. --id tract=0",
                               ContainerClass=coaddBase.CoaddDataIdContainer)

        return parser

    # Don't forget to overload these
    def _getConfigName(self):
        return None

    def _getEupsVersionsName(self):
        return None

    def _getMetadataName(self):
        return None


if __name__ == '__main__':
    MakeFakeInputsTask.parseAndRun()
