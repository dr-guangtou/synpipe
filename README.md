# SynPipe: Synthetic Object Pipeline for Hyper Suprime-Cam Data

This project is to add fake stellar and galaxy sources to the HSC data processing. We use [galsim](https://github.com/GalSim-developers/GalSim) to generate fake galaxy sources. Stellar (PSF) sources are simply taken as the measured PSF. In the current incarnation, the pipeline accepts fake sources after the calibration but before measurement when processing single CCDs. This way, the fake sources don't affect things like PSF determination. Once the sources are added, they are deblended and measured just like the rest of the sources, and included in the output catalogs. They are also measured in the coadds, if you continue with the processing beyond single frame processing.

All the fake sources are added with the appropriate amount of Poisson noise. When adding fake sources, we also add a bit plane to the image mask called `FAKE`. This mask plane sets every pixel to which a fake source was added, even those for which the added flux is negligible. When adding sources, the pixel positions are saved in the calibrated exposure image header as `FAKE ID x_pos y_pos`. Because of this, and because of crowding, you probably don't want to add too many (few hundred of so) sources to a single CCD. This information in the header is used by matchFakes.py to extract the measurements of the fake sources from the catalog. For source catalogs where the sky (ra/dec) position of the objects are given, saving the pixel positions isn't necessary, but we've left it for now. In this case, `matchFakes.py` uses the ra/dec positions from the input catalog instead of the pixel position in the header to match input fake sources to the dected sources. This enables matchFakes.py to work on the coadd source tables as well as the visit source tables (the sources aren't directly added to the coadd so the pixel positions aren't saved in the coadd image).

####Setup
This code depends on the HSC pipeline (version 3.3.3 or later), and needs to have galsim built against the pipeline python. For some of the additional scripts (makeRaDec, matchFakes) the astropy package is also necessary. If you just have a list of sources however, you don't need it. This is already setup on master at IPMU, so if you are running there, you just need to setup the following:
```bash
$ export PYTHONPATH=/home/clackner/.local/lib/python2.7/site-packages:${PYTHONPATH}
$ setup -v -r hscPipe 3.3.3 (or whichever later version)
$ setup -v -j astrometry_net_data ps1_pv1.2c
$ setup -v -r path/to/fake-sources/
``` 
The first export is only to get astropy on PYTHONPATH, so adjust according to your local installation.

####Running
To run, you need to override the default configuration in the pipeline to include fake sources. We have 3 different tasks you can implement with the override config. They are:
  1. randomStarFakes: adds stars of a single brightness to random positions in a CCD
  2. randomGalSimFakes: adds galsim galaxies from a catalog to random positions in a CCD
  3. positionGalSimFakes: adds galsim galaxies from a catalog to fixed sky positions, also given in the catalog.
  4. positionStarFakes: adds PSF sources from a catalog to fixed sky positions 

Examples of how to use these tasks and standard configurations are given in the test/stars and test/galaxies. The command to run these for a small set of CCDs would is:
```bash
$ hscProcessCcd.py /to/data/ --rerun=/to/rerun --id visit=XXX ccd=YY -C config_XXX
```
More detailed instructions on how to run these examples is found in the tests folder [here](test/README.md). This also works with reduceFrames.py, if you want to add fake sources to an entire frame at once.

#####Adding fakes for coadds
Once the fake sources have been injected at the visit (individual exposure) level, they will be processed as regular sources while making coadds, as they are in the calibrated images. However, if you want to multiband detection, you need to add the fake sources (with reasonable colors) to all the bands, unless you want to test dropouts. This can be accomplished by having one input source catalog per band, with the same source positions, but different magnitudes. 

If you aren't interested in looking at the source measurement on the individual visits, you should still add the sources to the single visits, and then run the stacking, detection and measurement on the visits with fakes. `runAddFakes.py` is a simple task that takes already processed data and creates a new rerun with fake sources added to the calibrated frames. You'll need to retarget the `fakes` task to make it actually add fake sources. To run it:
```bash
$ runAddFakes.py /path/to/root --rerun rerun/input:rerun/output-fakes --queue queue -id visit=visit1^visit2... -C fakes_config
```
where `fakes_config` needs to at least include a line `root.fakes.retarget(someFakes.someFakesTask)`. Examples of configurations for the various tasks are in the test directory.

####Debugging
If you want to add check that the fake source adding is working without going through all the measurements, use debugFakes, which takes a calibrated exposure from a completed rerun (rerun1) and writes the exposure with fakes added to rerun2.
```bash
$ debugFakes.py /to/data/ --rerun=rerun1:rerun2 --id visit=XXX ccd=YY -C config_debug
```
Note that this will fail if rerun1 doesn't have the visit/ccd you are trying to process already in it. This code doesn't do any measurements, it simply adds the fake sources to the image, which you can then open in DS9.

####Make Random RA, DEC catalog 

* Right now, makeRaDecCat.py accepts either a dataId ({visit,ccd} or
  {tract,patch,filter}) or a range of {RA,Dec} as input. 
* To use it on single frame or coadd images, a rootDir for the data is also
  required 
* The rangeRaDec can be either a list or a numpy array in the format of 
  (raMin, raMax, decMin, decMax)
* The code will return a list of {RA,Dec} pairs; It also accepts an input fits
  catalog, and will add two columns to the catalog (RA, Dec).  Make sure the
  number of galaxies in the input catalog is equal or smaller than the number of
  random RA,Dec pairs (This can be improved later).  The output catalog will
  have a '_radec' suffix.  
* And, an optional 'rad' parameter is available as the minimum allowed
  separation (in unit of arcsec) between any of these random RA, Dec pairs. 

```python 
> rangeRaDec = [123.4, 123.8, 12.0, 13.0]
> inputCat = 'fakeExp.fits'
> randomRaDec = makeRaDecCat(50, rangeRaDec=rangeRaDec, rad=10.0, inputCat=inputCat)
```
or 

```python 
> dataId = {tract:0, patch:'4,5', filter:'HSC-I'}
> rootDir = '/lustre/Subaru/SSP/rerun/song/cosmos-i2' 
> inputCat = 'fakeExp.fits'
> randomRaDec = makeRaDecCat(50, dataId=dataId, rad=10.0, inputCat=inputCat,
>                            rootDir=rootDir)
```
