####Instructions for running test tasks
We've implemented three test cases for the the tasks below. You can run these to test that everything works and use them as templates for larger, more complicated tasks. 

###Adding stars at random positions
The task randomStarFakeSourcesTask adds fake stars of a given magnitude to an individual CCD at random positions. The sample configuration file is in `test/stars/config_star_test`. The available configuration parameters are:

name | description
---------| -------------
retarget | name of fake sources task to use
magnitude | magnitude of stars to add
nStars | number of stars to add ,default is 1
margin | size of margin around chip edge in which no sources should be added 
seed | seed for random generator 

The test case adds 100 stars of 22nd magnitude to visit 1236 and ccd 50 (COSMOS i-band data). To run the test, simply run `$ test_star_run.sh /path/to/data/ /path/to/rerun`. The example task then outputs a file `test_star_matchFakes.fits`, which is a list of the measurements of the fake stars. From here, you can check the PSF magnitudes of the stars against the input catalog. Note that because of the fixed random seed, galaxies will be added to the same pixel positions in all CCDs if you run this over multiple CCDs (i.e. using reduceFrames.py).

###Adding galaxies at random positions
The task randomGalFimFakes adds fake galaxies to random positions of a given CCD. The galaxies can be either Sersic or double Serisc profiles and a catalog of the galaxy properties are needed in a fits file. This is given to the config parameter `fakes.galList`. The input catalog for single Sersic galaxies (of which exponential and de Vaucouleurs are special cases) needs to contain at least:
  1. ID (otherwise the index in the list is used)
  2. mag: desired total magnitude
  3. reff: half-light radius in arcseconds
  4. sersic_n: sersic index
  5. b_a: axis ratio
  6. theta: rotation angle, in degrees counter-clockwise from the x-axis

The galaxy profiles are computed by GalSim. Right now, the profile are truncated at 10x reff, but that's subject to change. 

The configuration for the test case of this task is in `test/galaxies/config_gal_test`. The available configuration parameters are:

name | description
---------| -------------
retarget | name of fake sources task to use
galList | file for galaxy catalog
galType | type of galaxy profile to make, used by makeFakes code, options are sersic, dsersic, and real
nGal | number of galaxies to add, chosen at random from the galList catalog, if unset, the whole catalog is used
margin | size of margin around chip edge in which no sources should be added 
seed | seed for random generator 

The extra, non-fake-related parameters in the config are used to turn on cmodel magnitudes for single frame sources, and turn off the last re-estimation of the background during detection. In this way, no background subtraction is done after fake sources are added, so we aren't testing the background subtraction at all.

The test task adds 50 exponential galaxies to chip 50 in visit 1236 (COSMOS i-band). To run it, use the command `$ test_gal_run.sh /path/to/data /path/to/rerun`. As with the stars, the test task outputs a catalog (`test_exp_matchFakes.fits`) of measured parameters of the fake sources (measurements that match the added fakes in pixel position.

####Adding fake galaxies at fixed RA/DEC
The task positionGalSimFakes.py similar to the randomGalSimFakes.py, except the input catalog includes an ra/dec position where the source is added. This means that this task can be used in adding fake sources for coadd processing. In this case, the input catalog position angle, theta, refers to degrees counter-clockwise from North, the standard definition. The available configuration parameters are:

name | description
---------| -------------
galList | file for galaxy catalog, including columns ra and dec
galType | type of galaxy profile to make, used by makeFakes code, options are sersic, dsersic, and real
maxMargin | size of buffer around CCD (in pixels) in which to look for sources that partially overlap with the current CCD
seed | seed for random generator for the Poisson noise added to the galaxy images

An example configuration file is given in `test/galaxies/config_pos`. This takes as input a list of 3 galaxies which are in the ccd 50 of visit 1236. The galaxy input parameters are galaxy_test_pos.fits. Random galaxy positions in an ra/dec range or for a visit/ccd or tract/patch can be generated with makeRaDecCat.py.

###Adding sources to Coadds
When dealing with coadds, you'll want to use the tasks that take a catalog of sources along with positions and add them to all the visits going into the stack. If you want to add fake galaxies, use positionGalSimFakes.py. To make things a bit easier, use the `reduceFrames.py` command, which batch processes all the CCDs in a visit. *Note that since `reduceFrames.py` calls `processCcd`, you'll need to change the configuration file. All the entries need to be prepended with `root.processCcd.` instead of simply `root.`.*

Once the single frame processing is finished, follow the [instructions](http://hsca.ipmu.jp/hscsphinx/pipeline/coadd_proc.html) for making a sky map or discrete sky map and running `mosaic.py` and `stack.py`. The fake sources don't get any special treatment in the coadd processing. *TODO: ensure this isn't a problem*

####Looking at the processed fake sources

