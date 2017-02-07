#!/usr/bin/env python
"""
runMatchFakes.py
matches fakes based on position stored in the calibrated exposure image header
"""

import argparse
import fakes.matchFakes as matchFakes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('rootDir', help='root dir of data repo')
    parser.add_argument('visit',
                        help='id of visit (or tract, if filter is specified)',
                        type=int)
    parser.add_argument('-f', '--filter', dest='filt',
                        help='name of filter, if none assume single visit',
                        default=None)
    parser.add_argument('--ccd', nargs='+', help='id of ccd(s) or patches')
    parser.add_argument('-o', help='outputfilename', default=None,
                        dest='outfile')
    parser.add_argument('-c', help='fake catalog', default=None,
                        dest='fakeCat')
    parser.add_argument('-w', '--overwrite', help='overwrite output file',
                        dest='ow', default=False, action='store_true')
    parser.add_argument('-m', '--multiband',
                        help='Match multiband measurements',
                        dest='multiband', default=False, action='store_true')
    parser.add_argument('-t', '--tolerance', type=float, dest='tol',
                        default=1.0,
                        help='matching radius in PIXELS (default=1.0)')
    parser.add_argument('-p', '--pixelMatch', default=False,
                        action='store_true',
                        help='do a pixel position match based on the header')
    parser.add_argument('-r', '--reffMatch',
                        help='Match the fake sources using tol x Reff',
                        dest='reffMatch', default=False, action='store_true')
    parser.add_argument('--min', '--minRad',
                        help='Min matching radius (pixel) when -r is set',
                        dest='minRad', type=float, default=None)
    parser.add_argument('-j', '--multijobs', type=int,
                        help='Number of jobs run at the same time',
                        dest='multijobs', default=1)
    parser.add_argument('--ra', '--raCol', dest='raCol',
                        help='Name of the column for RA',
                        default='RA')
    parser.add_argument('--dec', '--decCol', dest='decCol',
                        help='Name of the column for Dec',
                        default='Dec')
    args = parser.parse_args()

    if (args.ccd is None) or (len(args.ccd) < 1):
        if args.filt is None:
            args.ccd = range(104)
        else:
            """hack, assumes 11x11 patches per CCD"""
            args.ccd = ['%d,%d' % (x, y) for x in range(11) for y in range(11)]

    matchFakes.returnMatchTable(args.rootDir, args.visit, args.ccd,
                                args.outfile, args.fakeCat,
                                overwrite=args.ow, filt=args.filt,
                                tol=args.tol,
                                pixMatch=args.pixelMatch,
                                multiband=args.multiband,
                                reffMatch=args.reffMatch,
                                multijobs=args.multijobs,
                                minRad=args.minRad,
                                raCol=args.raCol, decCol=args.decCol)
