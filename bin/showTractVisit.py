#!/usr/bin/env python

import re
import random
import argparse
import matplotlib.pyplot as pyplot

import lsst.afw.geom as afwGeom
import lsst.afw.image as afwImage
import lsst.afw.cameraGeom as camGeom
import lsst.daf.persistence as dafPersist


def bboxToRaDec(bbox, wcs):
    """Get the corners of a BBox and convert them to lists of RA and Dec."""
    corners = []
    for corner in bbox.getCorners():
        p = afwGeom.Point2D(corner.getX(), corner.getY())
        coord = wcs.pixelToSky(p).toIcrs()
        corners.append([coord.getRa().asDegrees(), coord.getDec().asDegrees()])
    ra, dec = zip(*corners)
    return ra, dec


def percent(values, p=0.5):
    """Return a value a faction of the way between the min and max values."""
    m = min(values)
    interval = max(values) - m
    return m + p*interval


def main(butler, tract, visits, ccds=None,
        showPatch=False, singleVisit=False, filter="HSC-I"):
    """Plot the visits/CCDs belong to certain Tract."""
    #  draw the CCDs
    ras, decs = [], []
    for i_v, visit in enumerate(visits):
        print i_v, visit
        visitColor = "#%06x" % random.randint(0, 0xFFFFFF)
        ccdList = [camGeom.cast_Ccd(ccd) for ccd in
                   camGeom.cast_Raft(butler.get("camera")[0])]
        for ccd in ccdList:
            bbox = ccd.getAllPixels()
            ccdId = ccd.getId().getSerial()

            if (ccds is None or ccdId in ccds) and ccdId < 104:
                dataId = {'tract': tract, 'visit': visit, 'ccd': ccdId}
                try:
                    wcs = afwImage.makeWcs(butler.get("calexp_md", dataId))
                except:
                    pass
                ra, dec = bboxToRaDec(bbox, wcs)
                ras += ra
                decs += dec
                if singleVisit:
                    color = 'r'
                else:
                    color = visitColor
                pyplot.fill(ra, dec, fill=True, alpha=0.3,
                            color=color, edgecolor=color)

    buff = 0.1
    xlim = max(ras)+buff, min(ras)-buff
    ylim = min(decs)-buff, max(decs)+buff

    # draw the skymap
    if showPatch:
        skymap = butler.get('deepCoadd_skyMap', {'tract': tract})
        tt = skymap[tract]
        for patch in tt:
            ra, dec = bboxToRaDec(patch.getInnerBBox(), tt.getWcs())
            pyplot.fill(ra, dec, fill=False, edgecolor='k', lw=1,
                        linestyle='dashed')
            if (xlim[1] < percent(ra) < xlim[0]) and (
               ylim[0] < percent(dec) < ylim[1]):
                        pyplot.text(percent(ra), percent(dec, 0.9),
                                    str(patch.getIndex()),
                                    fontsize=6,
                                    horizontalalignment='center',
                                    verticalalignment='top')

    # add labels as save
    ax = pyplot.gca()
    ax.set_xlabel("R.A. (deg)")
    ax.set_ylabel("Decl. (deg)")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    fig = pyplot.gcf()

    if singleVisit:
        fig.savefig("%s_patches_%s_%s.png" % (tract, visit, filter))
    else:
        fig.savefig("%s_patches_%s.png" % (tract, filter))

    fig.clear()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Root directory of data repository")
    parser.add_argument("tract", type=int, help="Tract to show")
    parser.add_argument("visits", help="visit to show")
    parser.add_argument("-c", "--ccds", help="specify CCDs")
    parser.add_argument("-f", "--filter", help="filter",
                        default='HSC-I')
    parser.add_argument("-p", "--showPatch", action='store_true',
                        default=False,
                        help="Show the patch boundaries")
    parser.add_argument("-s", "--singleVisit", action='store_true',
                        default=False,
                        help="Show one visit at a time")
    args = parser.parse_args()

    def idSplit(id):
        if id is None:
            return id
        ids = []
        for r in id.split("^"):
            m = re.match(r"^(\d+)\.\.(\d+):?(\d+)?$", r)
            if m:
                limits = [int(v) if v else 1 for v in m.groups()]
                limits[1] += 1
                ids += range(*limits)
            else:
                ids.append(int(r))
        return ids

    visits = idSplit(args.visits)

    butler = dafPersist.Butler(args.root)

    if not args.singleVisit:
        main(butler, args.tract, visits=idSplit(args.visits),
             ccds=idSplit(args.ccds),
             showPatch=args.showPatch,
             singleVisit=args.singleVisit,
             filter=args.filter)
    else:
        for vv in visits:
            main(butler, args.tract, visits=[vv],
                 ccds=idSplit(args.ccds),
                 showPatch=args.showPatch,
                 singleVisit=args.singleVisit,
                 filter=args.filter)
