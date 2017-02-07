# Summary of On-going SynPipe Tests 

* Last update: 2016/10/31

----- 

## Basic Photometric Tests for the SynPipe Paper: 

* by Song Huang @Kavli-IPMU (song.huang@ipmu.jp)

* The purpose of the tests is to provide basic photometric benchmarks of the current HSC 
  pipeline using synthetic stars and galaxies, to evaluate the accuracy of PSF, Kron, and 
  cModel photometry under ideal conditions.  

* All the catalogs are kept on `Master@IPMU`; Please contact Song Huang in case you are
  interested in them; The results will be used for the technical paper for SynPipe 

* The tests rightn now have three components: 

### Photometric Tests for Synthetic Stars

* **Inputs**: 5-band photometry of real stars at $$$i < 26.5$$$ mag in the VVDs region.
    (Basic quality cuts applied)
* **Tracts**: 9699 / 8764 
* **Basic Information**: 5-band tests at single-visit level; 
    random locations within the Tract; 
    ~150000 stars per tract 
* **Progress**: Finished 

### Photometric Tests for Synthetic Galaxies 

- **Inputs**: Single Sersic model of COSMOS galaxies with $$i<25.2$$ mag from 
    Claire Lackner's catalog; Colors are based on multiband catalog for COSMOS
- **Tracts**: 9699 / 8764 
- **Basic Information**: 5-band tests at single-visit level; 
    random locations within the Tract; 
    ~60000-100000 galaxies per tract; 
    Will separate the galaxies into bright/faint subsamples at $$i\sim 23.0$$ mag.
- **Progress**: In preparation

### Photometric Tests for Synthetic QSOs (On behalf of Ji-Jia)

- **Inputs**: 5-band photometry of synthetic QSOs from Ji-Jia down to $$i > 28.0$$;
    QSOs are modeled as point sources. 
- **Tracts**: 9693
- **Basic Information**: 5-band tests at single-visit level; 
    random locations designed by Ji-Jia; 
    ~500000 QSOs per tract 
- **Progress**: Finished 

----- 

## Photometric Tests for Synthetic LAEs at z=5.7 and 6.6

* by Akira Konno @ICRR

* **Inputs**: 6-band (NB0816 or NB0921; and grizy) photometry of synthetic z=5.7 (or 6.6) LAEs at NB<27.0
* **Tracts**: 9813 / 9464
* **Basic Information**: 6-band tests in stacked images; random locations within the tract; ~150000 LAEs per tract
* **Progress**: On going

----- 

## Test the Selection Completness for the Paper of High-z Dropout Galaxies

* by Yoshiaki Ono@ICRR (ono@icrr.u-tokyo.ac.jp)

* The purpose of the tests is to estimate the completeness of high-z galaxies by using our selection criteria for the HSC SSP catalogs. 

* All the catalogs are kept on the ICRR computer. Please contact Yoshiaki Ono if you are interested in the catalogs. The results will be used in high-z dropout galaxy papers. 

### Tests for z=4 g-dropout, z=5 r-dropout, z=6 i-dropout and z=7 z-dropout galaxies 
    - **Inputs**: 5-band photometry (grizy) of z=4-7 galaxies with $m_UV$=22-27 mag.    
    - **Tracts**: 9813 (Ultradeep) / 9464 (Deep) / 8766 (Wide)
    - **Basic Information**: added at single-visit level; grid locations 
    - **Progress**: Finished

### Tests for z=3 u-dropout galaxies and z=2 BX/BM galaxies
    - **Inputs**: 6-band photometry (ugrizy) of z=2-3 galaxies with $m_UV$=22-27 mag. 
    - **Progress**: in preparation; we need to work around the source inserting process for the CLAUDS u-band data.  

----- 

## Detection and Selection Tests in Small Scale Separations 

* by Yuichi Harikane @ICRR  (hari@icrr.u-tokyo.ac.jp)

* The catalogs are in the ICRR computer to save the resources in IPMU. Please contact Yuichi Harikane if you are interested in them.

- **Inputs**: 5-band photometry of model Lyman break galaxies with `23.25<i<26.75 mag`.
- **Tracts**: 9813 (UD-COSMOS)
- **Basic Information**: Grid locations within the tract; ~200000 galaxies per tract. The separations of pairs are changed from 1" to 15" in order to test the detection/selection completeness depending on the separation.
- **Progress**: Finished. 

----- 

## Detection and photometry tests in (CAMIRA) cluster fields 

* by I-Non Chiu@ASIAA  (inchiu@asiaa.sinica.edu.tw)

- **Inputs**: Coordinates (RA/Dec) and grizY band photometry of selected background galaxies (modelled from BC03 templates).
- **Tracts**: TBD (we are going to select several typical clusters where we want to run Synpipe on).
- **Basic Information**: Grid locations around cluster centers. We are going to study the `relative` difference (or a function of clustercentric radius) in detection and photometry.
- **Progress**: The catalogs are done. The projection onto the tracts is being prepared.
