#!/usr/bin/env python
# encoding: utf-8

import os
import argparse
import itertools
import numpy as np
import lsst.daf.persistence as dafPersist
from distutils.version import StrictVersion


def tractFindVisits(rerun, tract, filter='HSC-I', patch=None,
                    dataDir='/lustre/Subaru/SSP/rerun/'):
    """Return the list of input Visits to coadd."""
    butler = dafPersist.Butler(os.path.join(dataDir, rerun))

    pipeVersion = dafPersist.eupsVersions.EupsVersions().versions['hscPipe']
    if StrictVersion(pipeVersion) >= StrictVersion('3.9.0'):
        coaddData = "deepCoadd_calexp"
    else:
        coaddData = "deepCoadd"

    if patch is not '':
        """
        Only 1 Patch is required
        """
        coadd = butler.get(coaddData, dataId={"tract": tract,
                                              "patch": patch,
                                              "filter": filter},
                           immediate=True)
        ccdInputs = coadd.getInfo().getCoaddInputs().ccds
        visits = np.unique(ccdInputs.get("visit"))
        print "\n# Visits for Tract=%d Filter=%s Patch=%s\n" % (tract,
                                                                filter,
                                                                patch)
    else:
        """
        Go through all the possible patches
        """
        visits = np.empty([0], dtype=int)
        for pa in itertools.combinations_with_replacement((np.arange(9)), 2):
            patch = str(pa[0]) + ',' + str(pa[1])
            try:
                coadd = butler.get(coaddData, dataId={"tract": tract,
                                                      "patch": patch,
                                                      "filter": filter},
                                   immediate=True)
            except Exception:
                continue
            ccdInputs = coadd.getInfo().getCoaddInputs().ccds
            vTemp = np.unique(ccdInputs.get("visit"))
            visits = np.unique(np.append(visits, vTemp))

        for pa in itertools.combinations_with_replacement((np.arange(9)), 2):
            patch = str(pa[1]) + ',' + str(pa[0])
            try:
                coadd = butler.get(coaddData, dataId={"tract": tract,
                                                      "patch": patch,
                                                      "filter": filter},
                                   immediate=True)
            except Exception:
                continue
            ccdInputs = coadd.getInfo().getCoaddInputs().ccds
            vTemp = np.unique(ccdInputs.get("visit"))
            visits = np.unique(np.append(visits, vTemp))

        print "\n# Input visits for Tract=%d Filter=%s\n" % (tract, filter)

    line = ''
    print " # Input CCDs includes %d Visits\n" % len(visits)
    for vv in visits:
        line = line + str(vv) + '^'

    print line[:-1] + '\n'

    return visits


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("rerun", help="Name of the data rerun")
    parser.add_argument("tract", help="Tract number", type=int)
    parser.add_argument('--dataDir', '-d', dest='dataDir',
                        help="Data location",
                        default='/lustre/Subaru/SSP/rerun/')
    parser.add_argument('--filter', '-f', dest='filter',
                        help="Filter name",
                        default='HSC-I')
    parser.add_argument('--patch', '-p', dest='patch',
                        help="Patch ID", default='')

    args = parser.parse_args()

    tractFindVisits(args.rerun, args.tract, filter=args.filter,
                    patch=args.patch, dataDir=args.dataDir)
