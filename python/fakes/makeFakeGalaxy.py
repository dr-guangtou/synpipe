#!/usr/bin/env python
# encoding: utf-8

import warnings

import numpy as np

import galsim
print galsim.__file__

import pyfits as fits


def makeGalaxy(flux, gal, psfImage,
               galType='sersic', cosmosCat=None,
               drawMethod='no_pixel',
               transform=None, addShear=False,
               calib=None,
               sersic_prec=0.01, addPoisson=False):
    """
    Function called by task to make galaxy images

    INPUTS:
        flux = calibrated total flux
        gal = galaxy parameters in record (np.recarray)
        psfImage = np.ndarray of psfImage
        galType = type of galaxy we want to make, this has to agree
                  with what's in the record array, options now are:
                    'sersic' (single sersic),
                    'dsersic' (double sersic), and
                    'real' (for making galaxies from real HST images)
                    'cosmos' (Using GalSim.COSMOSCatalog)

    All the necessary keywords need to be in the fits catalog,
    including maybe drawMethod and trunc...
    """
    if galType is 'sersic':
        raise ValueError
        return galSimFakeSersic(flux, gal, psfImage=psfImage,
                                trunc=trunc,
                                drawMethod=drawMethod,
                                returnObj=False,
                                transform=transform,
                                addShear=addShear,
                                addPoisson=addPoisson)

    if galType is 'dsersic':
        raise ValueError
        # TODO: addShear option is not available for double Sersic yet
        (comp1, comp2) = parseDoubleSersic(flux, gal)
        return galSimFakeDoubleSersic(comp1, comp2, psfImage=psfImage,
                                      trunc=trunc,
                                      drawMethod=drawMethod,
                                      returnObj=False,
                                      transform=transform,
                                      addShear=addShear,
                                      addPoisson=addPoisson)

    if galType is 'real':
        raise ValueError
        # TODO: For real galaxies, we need to decide which to use: index in the
        # catalog or Object ID.  Now, I just use Index
        (real_galaxy_catalog, index) = parseRealGalaxy(gal)
        if index >= 0:
            index = index
            random = False
        else:
            index = None
            random = True
        return galSimRealGalaxy(flux, real_galaxy_catalog,
                                index=index,
                                psfImage=psfImage,
                                random=random,
                                returnObj=False,
                                drawMethod=drawMethod,
                                transform=transform,
                                addPoisson=addPoisson)

    if galType is 'cosmos':
        if cosmosCat is None or calib is None:
            raise Exception("# No COSMOSCatalog() provided!")
        return galSimFakeCosmos(cosmosCat, calib, gal,
                                psfImage=psfImage,
                                returnObj=False,
                                sersic_prec=sersic_prec,
                                drawMethod=drawMethod,
                                transform=transform,
                                addShear=addShear,
                                addPoisson=addPoisson)


def parseRealGalaxy(gal):
    """Place holder for real galaxi."""
    try:
        index = gal['index']
    except KeyError:
        index = -1

    # Get the catalog name and the directory
    try:
        cat_name = gal['cat_name']
    except KeyError:
        raise KeyError('Can not find the name of the catlog')
    try:
        cat_dir = gal['cat_dir']
    except KeyError:
        cat_dir = None

    real_galaxy_catalog = galsim.RealGalaxyCatalog(cat_name,
                                                   dir=cat_dir)

    return real_galaxy_catalog, index


def parseDoubleSersic(tflux, gal):
    """
    Parse the input total flux [tflux] and parameter record array
    [gal] into two parameter records for each component [comp1, comp2]
    """

    # Check if this is a real 2-Sersic record
    try:
        frac1 = float(gal['b2t'])
    except KeyError:
        raise KeyError("No b2t parameter is found in the record!!")

    # Make sure the flux fraction of the first component is reasonable
    if (frac1 <= 0) or (frac1 >= 1):
        raise Exception("b2t should be > 0 and <1 !!")
    flux1, flux2 = (tflux * frac1), (tflux * (1.0 - frac1))

    # Check, then read in other parameters
    galID = gal["ID"]
    # Effective radius
    try:
        reff1, reff2 = float(gal["reff1"]), float(gal["reff2"])
    except KeyError:
        raise KeyError("reff1 or reff2 is found in the record!!")
    # Sersic index
    try:
        nser1, nser2 = float(gal["sersic_n1"]), float(gal["sersic_n2"])
    except KeyError:
        raise KeyError("sersic_n1 or sersic_n2 is found in the record!!")
    # Axis ratio
    try:
        ba1, ba2 = float(gal["b_a1"]), float(gal["b_a2"])
    except KeyError:
        raise KeyError("b_a1 or b_a2 is found in the record!!")
    # Position angle
    try:
        pa1, pa2 = float(gal["theta1"]), float(gal["theta2"])
    except KeyError:
        raise KeyError("theta1 or theta2 is found in the record!!")

    comp1 = np.array((galID, flux1, nser1, reff1, ba1, pa1),
                     dtype=[('ID', 'int'),
                            ('mag', 'float'),
                            ('sersic_n', 'float'),
                            ('reff', 'float'),
                            ('b_a', 'float'),
                            ('theta', 'float')])
    comp2 = np.array((galID, flux2, nser2, reff2, ba2, pa2),
                     dtype=[('ID', 'int'),
                            ('mag', 'float'),
                            ('sersic_n', 'float'),
                            ('reff', 'float'),
                            ('b_a', 'float'),
                            ('theta', 'float')])

    return comp1, comp2


def arrayToGSObj(imgArr, scale=1.0, norm=False):
    """
    Convert an input 2-D array into a GalSim Image object

    TODO : Check the scale here
            According to the GalSim Doxygen
            If provided, use this as the pixel scale for the Image;
            this will override the pixel scale stored by the provided Image.
            If scale is None, then take the provided image's pixel scale.
            [default: None]
    """
    if norm:
        return galsim.InterpolatedImage(galsim.image.Image(imgArr),
                                        scale=scale,
                                        normalization="flux")
    else:
        return galsim.InterpolatedImage(galsim.image.Image(imgArr),
                                        scale=scale)


def galSimDrawImage(galObj, size=0, scale=1.0, method="no_pixel",
                    addPoisson=False):
    """
    "Draw" a GalSim Object into an GalSim Image using certain method, and with
    certain size

    TODO : Think about the scale here:
      By default scale=None
      According to GalSim Doxygen :
      If provided, use this as the pixel scale for the image. If scale is None
      and image != None, then take the provided image's pixel scale.
      If scale is None and image == None, then use the Nyquist scale.
      If scale <= 0 (regardless of image), then use the Nyquist scale.
    """

    # Generate an "Image" object for the model
    if size > 0:
        imgTemp = galsim.image.Image(size, size)
        galImg = galObj.drawImage(imgTemp, scale=scale, method=method)
    else:
        galImg = galObj.drawImage(scale=scale, method=method)

    # Just an option for test
    if addPoisson:
        galImg.addNoise(galsim.PoissonNoise())

    # Return the Numpy array version of the image
    return galImg.array


def galSimConvolve(galObj, psfObj, size=0, scale=1.0, method="no_pixel",
                   returnObj=False):
    """
    Just do convolution using GalSim

    Make sure the inputs are both GalSim GSObj
    The galaxy model should be the first one, and the PSF object is the second
    one; Returns a imgArr or GSObj
    """
    outObj = galsim.Convolve([galObj, psfObj])

    if returnObj:
        return outObj
    else:
        outArr = galSimDrawImage(galObj, size=size,
                                 scale=scale, method=method)
        return outArr


def galSimAdd(galObjList, size=0, scale=1.0, method="no_pixel",
              returnArr=False):
    """
    Just add a list of GSObjs together using GalSim
    Make sure all elements in the input list are GSObjs
    """
    if len(galObjList) < 2:
        raise Exception("Should be more than one GSObjs to add !")

    outObj = galsim.Add(galObjList)

    if returnArr:
        outArr = galSimDrawImage(outObj, size=size, scale=scale,
                                 method=method)
        return outArr
    else:
        return outObj


def plotFakeGalaxy(galObj, galID=None, suffix=None,
                   size=0, addPoisson=False):

    """
    Generate a PNG image of the model
    By default, the image will be named as 'fake_galaxy.png'
    """

    import matplotlib.pyplot as plt

    if galID is None:
        outPNG = 'fake_galaxy'
    else:
        outPNG = 'fake_galaxy_%i' % galID
    if suffix is not None:
        outPNG = outPNG + '_' + suffix.strip() + '.png'

    plt.figure(1, figsize=(8, 8))

    # Use "fft" just to be fast
    plt.imshow(np.arcsinh(galSimDrawImage(galObj, size=size,
                                          method="no_pixel",
                                          addPoisson=addPoisson,
                                          scale=1.0)))
    plt.savefig(outPNG)


def galSimFakeCosmos(cosmosCat, calib, gal,
                     psfImage=None, plotFake=False,
                     returnObj=True, sersic_prec=0.02,
                     drawMethod='no_pixel', scale=1.0,
                     transform=None, addShear=False,
                     addPoisson=False):
    """
    Generate fake galaxy using galSim.COSMOSCatalog objects.
    """
    # Select the useful parameter catalog
    indexUse = cosmosCat.orig_index
    paramCat = cosmosCat.param_cat
    objectUse = paramCat[indexUse]

    galFound = np.where(objectUse['IDENT'] == gal['COSMOS_ID'])[0]
    if len(galFound) == 0:
        warnings.warn("# Find no match for %d" % gal['COSMOS_ID'])
    elif len(galFound) > 1:
        warnings.warn("# Multiple match for %d" % gal['COSMOS_ID'])

    galIndex = galFound[0]
    cosObj = cosmosCat.makeGalaxy(index=galIndex,
                                  sersic_prec=sersic_prec,
                                  gal_type='parametric')
    hstFlux = cosObj.flux

    # If necessary, apply addtion shear (e.g. for weak lensing test)
    if addShear:
        try:
            g1 = float(gal['g1'])
            g2 = float(gal['g2'])
            cosObj = cosObj.shear(g1=g1, g2=g2)
        except ValueError:
            warnings.warn("Can not find g1 or g2 in the input!\n",
                          " No shear has been added!")

    # Do the transformation from sky to pixel coordinates, if given
    if transform is not None:
        cosObj = cosObj.transform(*tuple(transform.ravel()))

    # TODO : Should check the flux
    """
    The flux of the galaxy corresponds to a 1 second exposure time with the
        Hubble Space Telescope. Users who wish to simulate F814W images with a
        different telescope and an exposure time longer than 1 second should
        multiply by that exposure time, and by the square of the ratio of the
        effective diameter of their telescope compared to that of HST.
        (Effective diameter may differ from the actual diameter if there is
        significant obscuration.)

    The catalog returns objects that are appropriate for HST in 1 second
    exposures.  So for our  telescope we scale up by the relative area and
    exposure time.  Note that what is important is the *effective* area after
    taking into account obscuration.  For HST, the telescope diameter is 2.4
    but there is obscuration (a linear factor of 0.33).  Here, we assume that
    the telescope we're simulating effectively has no obscuration factor.
    We're also ignoring the pi/4 factor since it appears in the numerator and
    denominator, so we use area = diam^2.
    """
    """
    hstEffArea = (2.4 ** 2) * (1.0 - 0.33 ** 2)
    subaruEffArea = (8.2 ** 2) * (1.0 - 0.1 ** 2)
    fluxScaling = (subaruEffArea / hstEffArea)
    """
    hstMag = -2.5 * np.log10(hstFlux) + 25.94
    # hscFlux = 10.0 ** ((27.0 - hstMag) / 2.5)
    hscFlux = calib.getFlux(hstMag)
    # cosObj *= (hscFlux / hstFlux)
    cosObj = cosObj.withFlux(float(hscFlux))

    # Convolve the Sersic model using the provided PSF image
    if psfImage is not None:
        # Convert the PSF Image Array into a GalSim Object
        # Norm=True by default
        psfObj = arrayToGSObj(psfImage, norm=True)
        cosFinal = galsim.Convolve([cosObj, psfObj])
    else:
        cosFinal = cosObj

    # Make a PNG figure of the fake galaxy to check if everything is Ok
    if plotFake:
        plotFakeGalaxy(cosFinal, galID=gal['ID'])

    # Now, by default, the function will just return the GSObj
    if returnObj:
        return cosFinal
    else:
        return galSimDrawImage(cosFinal,
                               method=drawMethod, scale=scale,
                               addPoisson=addPoisson)


def galSimFakeSersic(flux, gal, psfImage=None, scaleRad=False, returnObj=True,
                     expAll=False, devAll=False, plotFake=False, trunc=0,
                     drawMethod="no_pixel", addPoisson=False, scale=1.0,
                     transform=None, addShear=False):
    """
    Make a fake single Sersic galaxy using the galSim.Sersic function

    Inputs: total flux of the galaxy, and a record array that stores the
    necessary parameters [reffPix, nSersic, axisRatio, posAng]

    Output: a 2-D image array of the galaxy model  OR
            a GalSim object of the model

    Options:
        psfImage:     PSF image for convolution
        trunc:        Flux of Sersic models will truncate at trunc * reffPix
                      radius; trunc=0 means no truncation
        drawMethod:   The method for drawImage: ['auto', 'fft', 'real_space']
        addPoisson:   Add Poisson noise
        plotFake:     Generate a PNG figure of the model
        expAll:       Input model will be seen as nSersic=1
        devAll:       Input model will be seen as nSersic=4
        returnObj:    If TRUE, will return the GSObj
    """
    reff = float(gal["reff"])
    posAng = float(gal["theta"])
    axisRatio = float(gal["b_a"])
    nSersic = float(gal["sersic_n"])

    # Truncate the flux at trunc x reff
    if trunc > 0:
        trunc = trunc * reff

    # Make sure Sersic index is not too large
    if nSersic > 6.0:
        raise ValueError("Sersic index is too large! Should be <= 6.0")
    # Check the axisRatio value
    if axisRatio <= 0.05:
        raise ValueError("Axis Ratio is too small! Should be >= 0.05")

    # Make the Sersic model based on flux, re, and Sersic index
    if nSersic == 1.0 or expAll:
        if scaleRad:
            serObj = galsim.Exponential(scale_radius=reff)
        else:
            serObj = galsim.Exponential(half_light_radius=reff)
        if expAll:
            print " * Treated as a n=1 Exponential disk : %d" % (gal["ID"])
    elif nSersic == 4.0 or devAll:
        serObj = galsim.DeVaucouleurs(half_light_radius=reff, trunc=trunc)
        if devAll:
            print " * Treated as a n=4 De Vaucouleurs model: %d" % (gal["ID"])
    elif nSersic <= 0.9:
        serObj = galsim.Sersic(nSersic, half_light_radius=reff)
    else:
        serObj = galsim.Sersic(nSersic, half_light_radius=reff,
                               trunc=trunc)

    # If necessary, apply the Axis Ratio (q=b/a) using the Shear method
    if axisRatio < 1.0:
        serObj = serObj.shear(q=axisRatio, beta=(0.0 * galsim.degrees))

    # If necessary, apply the Position Angle (theta) using the Rotate method
    #    if posAng != 0.0 or posAng != 180.0:
    serObj = serObj.rotate((90.0 - posAng) * galsim.degrees)

    # If necessary, apply addtion shear (e.g. for weak lensing test)
    if addShear:
        try:
            g1 = float(gal['g1'])
            g2 = float(gal['g2'])
            serObj = serObj.shear(g1=g1, g2=g2)
        except ValueError:
            warnings.warn("Can not find g1 or g2 in the input!\n",
                          " No shear has been added!")

    # Do the transformation from sky to pixel coordinates, if given
    if transform is not None:
        serObj = serObj.transform(*tuple(transform.ravel()))

    # Pass the flux to the object
    serObj = serObj.withFlux(float(flux))

    # Convolve the Sersic model using the provided PSF image
    if psfImage is not None:
        # Convert the PSF Image Array into a GalSim Object
        # Norm=True by default
        psfObj = arrayToGSObj(psfImage, norm=True)
        serFinal = galsim.Convolve([serObj, psfObj])
    else:
        serFinal = serObj

    # Make a PNG figure of the fake galaxy to check if everything is Ok
    if plotFake:
        plotFakeGalaxy(serFinal, galID=gal['ID'])

    # Now, by default, the function will just return the GSObj
    if returnObj:
        return serFinal
    else:
        return galSimDrawImage(serFinal, method=drawMethod, scale=scale,
                               addPoisson=addPoisson)


def galSimFakeDoubleSersic(comp1, comp2, psfImage=None, trunc=0,
                           returnObj=True, devExp=False,
                           plotFake=False, drawMethod='auto',
                           addPoisson=False, scale=1.0, transform=None,
                           addShear=False):
    """
    Make a fake double Sersic galaxy using the galSim.Sersic function

    Inputs: total flux of the galaxy, and a record array that stores the
    necessary parameters [reffPix, nSersic, axisRatio, posAng]

    Output: a 2-D image array of the galaxy model  OR
            a GalSim object of the model

    Options:
        psfImage:     PSF image for convolution
        trunc:        Flux of Sersic models will truncate at trunc * reffPix
                      radius; trunc=0 means no truncation
        drawMethod:   The method for drawImage: ['auto', 'fft', 'real_space']
        addPoisson:   Add Poisson noise
        plotFake:     Generate a PNG figure of the model
        devexp:       The first component will be seen as a nSersic=4 bulge;
                      And, the second one will be seen as a nSersic=1 disk
        returnObj:    If TRUE, will return the GSObj
    """

    # Get the flux of both components
    flux1 = float(comp1['mag'])
    flux2 = float(comp2['mag'])
    # tflux = flux1 + flux2

    # If devExp = True : Treat the first component as an n=4 DeVaucouleurs
    #                    and, the second component as an n=1 Exponential disk
    if devExp:
        serModel1 = galSimFakeSersic(flux1, comp1, returnObj=True, devAll=True,
                                     trunc=trunc, addShear=addShear)
        serModel2 = galSimFakeSersic(flux2, comp2, returnObj=True, expAll=True,
                                     trunc=trunc, addShear=addShear)
    else:
        serModel1 = galSimFakeSersic(flux1, comp1, returnObj=True, trunc=trunc,
                                     addShear=addShear)
        serModel2 = galSimFakeSersic(flux2, comp2, returnObj=True, trunc=trunc,
                                     addShear=addShear)

    # Combine these two components
    doubleSersic = galSimAdd([serModel1, serModel2])

    # Do the transformation from sky to pixel coordinates, if given
    if transform is not None:
        doubleSersic = doubleSersic.transform(*tuple(transform.ravel()))

    # Convolve the Sersic model using the provided PSF image
    if psfImage is not None:
        # Convert the PSF Image Array into a GalSim Object
        # Norm=True by default
        psfObj = arrayToGSObj(psfImage, norm=True)
        dserFinal = galsim.Convolve([doubleSersic, psfObj])
    else:
        dserFinal = doubleSersic

    # Make a PNG figure of the fake galaxy to check if everything is Ok
    if plotFake:
        if devExp:
            plotFakeGalaxy(dserFinal, galID=comp1['ID'], suffix='devexp')
        else:
            plotFakeGalaxy(dserFinal, galID=comp1['ID'], suffix='double')

    # Now, by default, the function will just return the GSObj
    if returnObj:
        return dserFinal
    else:
        return galSimDrawImage(dserFinal, method=drawMethod, scale=scale,
                               addPoisson=addPoisson)


def galSimRealGalaxy(flux, real_galaxy_catalog, index=None, psfImage=None,
                     random=False, returnObj=True, plotFake=False,
                     drawMethod='auto', addPoisson=False, scale=1.0,
                     transform=None):
    """
    Real galaxy.
    """

    if index is None:
        random = True
    realObj = galsim.RealGalaxy(real_galaxy_catalog, index=index,
                                random=random)
    index = realObj.index

    # Pass the flux to the object
    realObj = realObj.withFlux(flux)

    # Do the transformation from sky to pixel coordinates, if given
    if transform is not None:
        realObj = realObj.transform(*tuple(transform.ravel()))

    # Convolve the Sersic model using the provided PSF image
    if psfImage is not None:
        # Convert the PSF Image Array into a GalSim Object
        # Norm=True by default
        psfObj = arrayToGSObj(psfImage, norm=True)
        realFinal = galsim.Convolve([realObj, psfObj])
    else:
        realFinal = realFinal

    # Make a PNG figure of the fake galaxy to check if everything is Ok
    if plotFake:
        plotFakeGalaxy(realFinal, galID=index, suffix='realga')

    # Now, by default, the function will just return the GSObj
    if returnObj:
        return realFinal
    else:
        return galSimDrawImage(realFinal, method=drawMethod, scale=scale,
                               addPoisson=addPoisson)


def testMakeFake(galList, asciiTab=False, single=True, double=True, real=True):
    """Test the makeFake functions."""
    # Make a fake Gaussian PSF
    psfGaussian = galsim.Gaussian(fwhm=2.0)
    psfImage = psfGaussian.drawImage().array

    # Test SingleSersic
    if single:
        if asciiTab:
            galData = np.loadtxt(galList, dtype=[('ID', 'int'),
                                                 ('mag', 'float'),
                                                 ('sersic_n', 'float'),
                                                 ('reff', 'float'),
                                                 ('b_a', 'float'),
                                                 ('theta', 'float')])
        else:
            galData = fits.open(galList)[1].data

        for igal, gal in enumerate(galData):

            flux = 10.0 ** ((27.0 - gal['mag']) / 2.5)

            print '\n---------------------------------'
            print " Input Flux : ", flux
            print " Input Parameters : ", gal["sersic_n"], gal["reff"]
            print "                    ", gal["b_a"], gal["theta"]

            galArray = galSimFakeSersic(flux, gal, psfImage=psfImage,
                                        plotFake=True, returnObj=False,
                                        trunc=12.0, drawMethod="no_pixel")

            print " Output Flux : ", np.sum(galArray)
            print " Shape of the Output Array : ", galArray.shape
            print '---------------------------------'

    # Test DoubleSersic
    if double:
        if asciiTab:
            raise Exception("For now, only FITS input is allowed !!")
        else:
            galData = fits.open(galList)[1].data

        for igal, gal in enumerate(galData):

            flux = 10.0 ** ((27.0 - gal['mag']) / 2.5)

            print '\n---------------------------------'
            print " Input Flux : ", flux

            (comp1, comp2) = parseDoubleSersic(flux, gal)

            # TODO: Get error when the axis ratio is small: 0.2?
            # RuntimeError: Solve error: Too many iterations in
            #               bracketLowerWithLimit()
            # It seems like that GalSim has some issues with highly elliptical
            # objects. Although different, see this one:
            # https://github.com/GalSim-developers/GalSim/issues/384
            # It seems that b/a = 0.25 is fine, so right now, just change the
            # lower limit of b/a to 0.25

            print " Flux for Component 1 : ", comp1['mag']
            print " Flux for Component 2 : ", comp2['mag']
            print " Comp 1 Parameters : %5.2f  %8.2f" % (comp1["sersic_n"],
                                                         comp1["reff"])
            print "                     %5.2f  %8.2f" % (comp1["b_a"],
                                                         comp1["theta"])
            print " Comp 2 Parameters : %5.2f  %8.2f" % (comp2["sersic_n"],
                                                         comp2["reff"])
            print "                     %5.2f  %8.2f" % (comp2["b_a"],
                                                         comp2["theta"])

            doubleArray = galSimFakeDoubleSersic(comp1, comp2,
                                                 psfImage=psfImage,
                                                 trunc=12, returnObj=False,
                                                 devExp=True, plotFake=True,
                                                 drawMethod='no_pixel')

            print " Output Flux : ", np.sum(doubleArray)
            print " Shape of the Output Array : ", doubleArray.shape
            print '---------------------------------'

    # Test RealGalaxy
    if real:
        # Make a special PSF for real galaxy
        psfReal = galsim.Gaussian(fwhm=0.2)
        psfRealImage = psfReal.drawImage().array
        # TODO : Scale seems to be a problem, should check again !!

        if asciiTab:
            raise Exception("For now, only FITS input is allowed !!")
        else:
            galData = fits.open(galList)[1].data

        for igal, gal in enumerate(galData):

            (real_galaxy_catalog, index) = parseRealGalaxy(gal)
            if index >= 0:
                index = index
                random = False
            else:
                index = None
                random = True

            flux = 10.0 ** ((27.0 - gal['mag']) / 2.5)

            realArray = galSimRealGalaxy(flux, real_galaxy_catalog,
                                         index=index,
                                         psfImage=psfRealImage,
                                         random=random,
                                         plotFake=True,
                                         returnObj=False,
                                         drawMethod='no_pixel')

            print '\n---------------------------------'
            print " Input Flux : ", flux

            print " Output Flux : ", np.sum(realArray)
            print " Shape of the Output Array : ", realArray.shape
            print '---------------------------------'
