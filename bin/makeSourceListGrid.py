#!/usr/bin/env python

"""
Generate grid of RA, DEC for fake objects.
Author: Ryoma Murata : 2016-04-15.
"""

import os
import warnings

import numpy as np

import astropy.table

import lsst.pipe.base as pipeBase
import lsst.pex.config as pexConfig
import lsst.pipe.tasks.coaddBase as coaddBase


def InputFakesGrid(ra_min, ra_max, dec_min, dec_max, separation_angle):
    '''
    Input:
    ra_min, ra_max, dec_min, dec_max: boundary positions (Unit: deg)
    separation angle: the angle between grids (Unit: arcsec)

    Output:
    ra, min: (Unit: deg)
    '''

    # start positions.
    Dec_start = dec_min
    RA_now, Dec_now = ra_min, dec_min

    # get RA at first.
    RA_first = []
    i = 0
    while True:
        RA_first.append(RA_now)
        RA_now = grid_RA(RA_now, Dec_now, separation_angle)

        i += 1
        if RA_now > ra_max:
            break
    RA_first = np.array(RA_first)

    # result array.
    ra, dec = [], []
    # get ra, dec.
    for i in range(RA_first.size):
        while True:
            ra.append(RA_first[i])
            dec.append(grid_Dec(RA_first[i], Dec_now, separation_angle))
            Dec_now = dec[-1]
            if Dec_now > dec_max:
                Dec_now = Dec_start
                break

    ra, dec = np.array(ra), np.array(dec)

    return ra, dec


def InputFakesGrid_withBlock(ra_min, ra_max, dec_min, dec_max,
                             separation_angle):
    '''
    Input:
    ra_min, ra_max, dec_min, dec_max: boundary positions (Unit: deg)
    separation angle: the angle between grids (Unit: arcsec)

    Output:
    ra, min: (Unit: deg)
    assign_model_num
    '''
    ra_pre, dec_pre = InputFakesGrid(ra_min, ra_max,
                                     dec_min, dec_max, (separation_angle * 2.))

    ra, dec = [], []
    assign_model_num = []

    for i in range(ra_pre.size):
        # Original
        ra.append(ra_pre[i])
        dec.append(dec_pre[i])
        assign_model_num.append(i)

        # Upper
        ra.append(grid_RA(ra_pre[i], dec_pre[i], separation_angle))
        dec.append(dec_pre[i])
        assign_model_num.append(i)

        # Right
        ra.append(ra_pre[i])
        dec.append(grid_Dec(ra_pre[i], dec_pre[i], separation_angle))
        assign_model_num.append(i)

        # Upper right
        ra.append(grid_RA(ra_pre[i], dec_pre[i], separation_angle))
        dec.append(grid_Dec(ra_pre[i], dec_pre[i], separation_angle))
        assign_model_num.append(i)

    # The result.
    ra = np.array(ra)
    dec = np.array(dec)
    assign_model_num = np.array(assign_model_num)

    return ra, dec, assign_model_num


def grid_RA(RA_in, Dec_in, theta):
    '''
    Input:
    RA_in, Dec_in: reference positions (Unit: deg)
    theta: separation angle (Unit: arcsec)

    Output:
    ra_next: next to RA_in (Unit: deg)
    '''
    # Degree Unit.
    RA_in *= (np.pi / 180.)
    Dec_in *= (np.pi / 180.)
    Dec_out = Dec_in
    theta *= (np.pi / 180. / 3600.)
    ra_next = (RA_in + np.arccos((np.cos(theta) -
                                  np.sin(Dec_in) *
                                  np.sin(Dec_out)) / (np.cos(Dec_in) *
                                                      np.cos(Dec_out))))
    ra_next *= (180. / np.pi)

    return ra_next


def grid_Dec(RA_in, Dec_in, theta):
    '''
    Input:
    RA_in, Dec_in: reference positions (Unit: deg)
    theta: separation angle (Unit: arcsec)

    Output:
    dec_next: next to Dec_in (Unit: deg)
    '''
    # Degree Unit.
    RA_in *= (np.pi / 180.)
    Dec_in *= (np.pi / 180.)
    RA_out = RA_in
    theta *= (np.pi / 180. / 3600.)

    A, B = np.sin(Dec_in), np.cos(Dec_in) * np.cos(RA_in - RA_out)
    phi = np.arctan2(- A, B)

    dec_next = (np.arccos(np.cos(theta) /
                          np.sqrt(A**2. + B**2.)) - phi) * (180. / np.pi)

    return dec_next


class MakeFakeInputsConfig(pexConfig.Config):
    coaddName = pexConfig.ChoiceField(
        dtype=str,
        doc="Type of data to use",
        default="deep",
        allowed={"deep": "deepCoadd"}
        )

    inputCat = pexConfig.Field(
        doc="input galaxy catalog, if none just return ra/dec list",
        dtype=str,
        optional=True, default=None)
    outDir = pexConfig.Field(doc='output directory for catalogs',
                             dtype=str,
                             optional=True, default='.')
    acpMask = pexConfig.Field(doc='region to include',
                              dtype=str,
                              optional=True, default='')
    rejMask = pexConfig.Field(doc='region to mask out',
                              dtype=str,
                              optional=True, default='')
    innerTract = pexConfig.Field(doc='only add to the inner Tract region',
                                 dtype=bool,
                                 optional=True, default=False)
    uniqueID = pexConfig.Field(doc='Use the index as unique ID',
                               dtype=bool,
                               optional=True, default=True)
    theta_grid = pexConfig.Field(doc='Grid separation in arcsec)',
                                 dtype=float, optional=False, default=25)


class MakeFakeInputsTask(pipeBase.CmdLineTask):
    """a task to make an input catalog of fake sources for a dataId"""

    _DefaultName = 'makeFakeInputs'
    ConfigClass = MakeFakeInputsConfig

    def run(self, dataRef):
        skyMap = dataRef.get('deepCoadd_skyMap', immediate=True)
        tractId = dataRef.dataId['tract']
        tract = skyMap[tractId]
        angle = self.config.theta_grid
        ra_vert, dec_vert = zip(*tract.getVertexList())
        ra_vert = sorted(ra_vert)
        dec_vert = sorted(dec_vert)
        ra0 = ra_vert[0].asDegrees()
        ra1 = ra_vert[-1].asDegrees()
        dec0 = dec_vert[0].asDegrees()
        dec1 = dec_vert[-1].asDegrees()

        if self.config.innerTract:
            ra0 += 0.0167
            ra1 -= 0.0167
            dec0 += 0.0167
            dec1 -= 0.0167

        raArr, decArr = InputFakesGrid(ra0, ra1, dec0, dec1,
                                       self.config.theta_grid)
        nFakes = raArr.size

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

                # Keep a log of the deleted ra, dec
                ra_deleted = raArr[np.invert(useful)],
                dec_deleted = decArr[np.invert(useful)]
                deleteLog = 'src_%d_radec_grid_%0.1farcsec_deleted' % (tractId,
                                                                       angle)
                np.save(os.path.join(self.config.outDir, deleteLog),
                        [ra_deleted, dec_deleted])
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
                print "## Rename the ID column"
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
                    outFits = 'src_%d_radec_grid_%0.1fasec_%s.fits' % (tractId,
                                                                       angle,
                                                                       filt)
                    outFits = os.path.join(self.config.outDir, outFits)
                    outTab.write(outFits, overwrite=True)
            else:
                outFits = 'src_%d_radec_grid_%0.1fasec.fits' % (tractId,
                                                                angle)
                outTab.write(os.path.join(self.config.outDir, outFits),
                             overwrite=True)
        else:
            outFits = 'src_%d_radec_only_grid_%0.1fasec.fits' % (tractId,
                                                                 angle)
            outTab.write(os.path.join(self.config.outDir, outFits),
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
