
# fakePipe Test Using `hscPipe 4.0.1`

---- Song Huang 2016.01.05 ----

## Basic Information: 

    * Using `hscPipe 4.0.1`
    * Use data from: `/lustre/Subaru/SSP/rerun/DR_S16A`
    
    * Input catalog is based on Claire Lackner's Sersic model fit to HSC/ACS images of 
      galaxies in the COSMOS field.  
    * For now, only test using HSC-G, HSC-R and HSC-I bands.

--------

## Input Catalog of Fake Galaxies: 

### Galaxies as faint as 25.2 magnitudes

    * From Claire's fit to COSMOS galaxies, down to `F814W=25.2 mag`:
        - `ser_25.2_listarcsec.fits`
        - There are **86440** galaxies

    * Select the ones with reasonable properties, and suitable for fakePipe tests: 
      ```
      mag <= 25.2 && reff >= 0.05 && reff <= 5.0 && sersic_n >= 0.4 && sersic_n <= 6.0 
          && b_a >= 0.05 && b_a <= 0.99
      ```
      - This results in **59651** galaxies. 

    * There is a population of faint galaxies with very large `reff` 
        (when plotting `mag` againt `reff`).  Exclude them from the sample using: 
      ```
      mag <= 23.0 || reff <= (-0.25 * mag + 7.2)
      ```
      - This results in **58697** galaxies.
      - **Fig.1**: See `cosmos_mag_reff_cut.png`

    * Make a multiband catalog: 
        - `g-i` = 0.5 

    * Save the catalog: `cosmos_25.2_multiband.fits`

### Bright Galaxies (`mag <= 21.5`)

    * Other cuts are the same with the above catalog 
        - There are **3221** galaxies in the sample.

    * Save the catalog: `cosmos_21.5_multiband.fits`

### Basic Properties of the Sample

    1. Magnitude: **Fig.2**, see `cosmos_fake_mag.png` 
    2. Effective radius: **Fig.3**, see `cosmos_fake_reff.png` 
    3. Sersic index: **Fig.4**, see `cosmos_fake_sersicn.png` 
    3. Axis ratio: **Fig.5**, see `cosmos_fake_ba.png` 

----

## HSC Data

* Using the data from rerun: `DR_S16A`.
* 2 WIDE Tracts in the `XMM_LSS` field.

### Wide: Tract:8766 

#### Find Visits: 

    * Command:
    ``` bash
    tractFindVisits.py DR_S16A 8766 --filter='HSC-I'
    tractFindVisits.py DR_S16A 8766 --filter='HSC-R'
    tractFindVisits.py DR_S16A 8766 --filter='HSC-Z'
    tractFindVisits.py DR_S16A 8766 --filter='HSC-G'
    tractFindVisits.py DR_S16A 8766 --filter='HSC-Y'
    ```

    * Results: 

    ```
    # Input visits for Tract=8766 Filter=HSC-I
        # Input CCDs includes 37 Visits:
7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484 

    # Input visits for Tract=8766 Filter=HSC-G
        # Input CCDs includes 37 Visits:
9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536

    # Input visits for Tract=8766 Filter=HSC-R
        # Input CCDs includes 25 Visits:
11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144
    ```

### Show Visits

    * Command: 

    - HSC-I band
    ``` bash 
    showTractVisit.py /lustre/Subaru/SSP/rerun/DR_S16A 8766  7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484 -p 
    ```
        - See: `dr16a_8766_patches_HSC-I.png`

    - HSC-G band
    ``` bash 
    showTractVisit.py /lustre/Subaru/SSP/rerun/DR_S16A 8766  9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536 -p 
    ```
        - See: `dr16a_8766_patches_HSC-G.png`

    - HSC-R band
    ``` bash 
    showTractVisit.py /lustre/Subaru/SSP/rerun/DR_S16A 8766  11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144 -p 
    ```
        - See: `dr16a_8766_patches_HSC-R.png`

    * Also do `showTractVisit.py` again with the `-s` option;
        - And save the figure for each visit under the `visits` folder


### Wide: Tract:8767 

#### Find Visits: 

    * Command:
    
    ``` bash
    tractFindVisits.py DR_S16A 8767 --filter='HSC-I'
    tractFindVisits.py DR_S16A 8767 --filter='HSC-R'
    tractFindVisits.py DR_S16A 8767 --filter='HSC-Z'
    tractFindVisits.py DR_S16A 8767 --filter='HSC-G'
    tractFindVisits.py DR_S16A 8767 --filter='HSC-Y'
    ```

    * Results: 

    ```
    # Input visits for Tract=8767 Filter=HSC-I
        # Input CCDs includes 32 Visits
7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486

    # Input visits for Tract=8767 Filter=HSC-G
        # Input CCDs includes 38 Visits
9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540

    # Input visits for Tract=8767 Filter=HSC-R
        # Input CCDs includes 25 Visits
11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148
    ```

### Show Visits

    * Command: 

    - HSC-I band
    ``` bash 
    showTractVisit.py /lustre/Subaru/SSP/rerun/DR_S16A 8767 7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486 -p 
    ```
        - See: `dr16a_8767_patches_HSC-I.png`

    - HSC-G band
    ``` bash 
    showTractVisit.py /lustre/Subaru/SSP/rerun/DR_S16A 8767 9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540 -p 
    ```
        - See: `dr16a_8767_patches_HSC-G.png`

    - HSC-R band
    ``` bash 
    showTractVisit.py /lustre/Subaru/SSP/rerun/DR_S16A 8767 11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148 -p 
    ```
        - See: `dr16a_8767_patches_HSC-R.png`

    * Also do `showTractVisit.py` again with the `-s` option;
        - And save the figure for each visit under the `visits` folder

-----

### Generate the "Accept" masks for these two Tracts: 

    * **This is an optional step, and involves using code outside the fakePipe.**
      Please contact Song Huang if you want to generate these for your data.

    * Under `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a`
        - Using `HSC-I` band as reference
        - `batchShapeComb.sh` and `dr16a_wide_fakeTest.lis`
        - Command: 
            ``` bash 
            ./batchShapeComb.sh dr16a_wide_fakeTest.lis
            ```
        - Results saved in `8766/shape` and `8767/shape`
        - The two accept masks are:
            1. `dr16a_wide_8766_HSC-I_shape_all.wkb`
            2. `dr16a_wide_8767_HSC-I_shape_all.wkb`

    * For these two Tracts, no Patch is missing, so the TractShape is very simple: 
        1. `dr16a_wide_8766_HSC-I_shape_all.png`
        2. `dr16a_wide_8767_HSC-I_shape_all.png`

### Generate the "Accept" masks for these two Tracts: 

    * **This is an optional step, and involves using code outside the fakePipe.**
      Please contact Song Huang if you want to generate these for your data.

    * Right now, the `BRIGHT_OBJECT` mask can be also combined; 
      But it is better to use the flag in the output catalog to exclude objects 
      contaminated by the bright stars. 

    * Under `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a`
        - Using `HSC-I` band as reference
        - `batchNoData.sh` and `dr16a_wide_fakeTest.lis`
        - Command: 
            ``` bash 
            ./batchNoData.sh dr16a_wide_fakeTest.lis
            ```
        - Results saved in `8766/nodata` and `8767/nodata`
        - The mask files are: 
            1. `dr16a_wide_8766_HSC-I_nodata_big.wkb`
            2. `dr16a_wide_8766_HSC-I_shape_all.wkb`
            3. `dr16a_wide_8767_HSC-I_nodata_big.wkb`
            4. `dr16a_wide_8767_HSC-I_shape_all.wkb`

    * The visualizations of these masks are available here: 
        1. `dr16a_wide_8766_HSC-I_nodata_big.png`
        2. `dr16a_wide_8766_HSC-I_shape_all.png`
        3. `dr16a_wide_8767_HSC-I_nodata_big.png`
        4. `dr16a_wide_8767_HSC-I_shape_all.png`
    * **There is an extremely bright star that affect many Patches in Tract 8766**

---- 

## Generate Input Catalogs:

### For full catalog

#### Tract: 8766

    * Configuration:
        - Input: `cosmos_25.2_multiband.fits`
        - acpMask: `dr16a_wide_8766_HSC-I_shape_all.wkb`
        - rejMask: `dr16a_wide_8766_HSC-I_nodata_all.wkb`
        - Only add to innerTract, and rename the ID column 
        - Outputs: rename to `full_8766_radec_G/R/I/Z/Y.fits`

    * Command:
    ``` bash
    makeSourceList.py /lustre/Subaru/SSP \
         --rerun=DR_S16A \
         --id tract=8766 filter='HSC-I' patch='4,4' \
         -c inputCat='../cosmos_25.2_multiband.fits' \
         acpMask='dr16a_wide_8766_HSC-I_shape_all.wkb' \
         rejMask='dr16a_wide_8766_HSC-I_nodata_all.wkb' \
         rhoFakes=450 innerTract=True uniqueID=True
    ``` 

    * Results: 
        - **36119** galaxies are left in the catalog.
        - The RA,Dec distribution of the fake sources is: `full_8766_radec_I.png` 

#### Tract: 8767

    * Configuration:
        - Input: `cosmos_25.2_multiband.fits`
        - acpMask: `dr16a_wide_8767_HSC-I_shape_all.wkb`
        - rejMask: `dr16a_wide_8767_HSC-I_nodata_all.wkb`
        - Only add to innerTract, and rename the ID column 
        - Outputs: rename to `full_8767_radec_G/R/I/Z/Y.fits`

    * Command:
    ``` bash
    makeSourceList.py /lustre/Subaru/SSP \
         --rerun=DR_S16A \
         --id tract=8767 filter='HSC-I' patch='4,4' \
         -c inputCat='../cosmos_25.2_multiband.fits' \
         acpMask='dr16a_wide_8767_HSC-I_shape_all.wkb' \
         rejMask='dr16a_wide_8767_HSC-I_nodata_all.wkb' \
         rhoFakes=450 innerTract=True uniqueID=True
    ``` 

    * Results: 
        - **36237** galaxies are left in the catalog.
        - The RA,Dec distribution of the fake sources is: `full_8767_radec_I.png` 

### For bright galaxies: 

#### Tract: 8766

    * Configuration:
        - Input: `cosmos_21.5_multiband.fits`
        - acpMask: `dr16a_wide_8766_HSC-I_shape_all.wkb`
        - rejMask: `dr16a_wide_8766_HSC-I_nodata_big.wkb`
        - Only add to innerTract, and rename the ID column 
        - Outputs: rename to `bright_8766_radec_G/R/I/Z/Y.fits`

    * Command:
    ``` bash
    makeSourceList.py /lustre/Subaru/SSP \
         --rerun=DR_S16A \
         --id tract=8766 filter='HSC-I' patch='4,4' \
         -c inputCat='../cosmos_21.5_multiband.fits' \
         acpMask='dr16a_wide_8766_HSC-I_shape_all.wkb' \
         rejMask='dr16a_wide_8766_HSC-I_nodata_big.wkb' \
         rhoFakes=300 innerTract=True uniqueID=True
    ``` 

    * Results: 
        - **24081** galaxies are left in the catalog.
        - The RA,Dec distribution of the fake sources is: `bright_8766_radec_I.png`

#### Tract: 8767

    * Configuration:
        - Input: `cosmos_21.5_multiband.fits`
        - acpMask: `dr16a_wide_8767_HSC-I_shape_all.wkb`
        - rejMask: `dr16a_wide_8767_HSC-I_nodata_big.wkb`
        - Only add to innerTract, and rename the ID column 
        - Outputs: rename to `bright_8766_radec_G/R/I/Z/Y.fits`

    * Command:
    ``` bash
    makeSourceList.py /lustre/Subaru/SSP \
         --rerun=DR_S16A \
         --id tract=8767 filter='HSC-I' patch='4,4' \
         -c inputCat='../cosmos_21.5_multiband.fits' \
         acpMask='dr16a_wide_8767_HSC-I_shape_all.wkb' \
         rejMask='dr16a_wide_8767_HSC-I_nodata_big.wkb' \
         rhoFakes=300 innerTract=True uniqueID=True
    ``` 

    * Results: 
        - **24177** galaxies are left in the catalog.
        - The RA,Dec distribution of the fake sources is: `bright_8767_radec_I.png`


### For highly blended objects: 

    * Replace the RA, DEC of available fake object catalog with RA, DEC of 
      real galaxies in the same Tract, and then add small shifts in both 
      RA and DEC direction.  Uisng `makeBlendedCat.py`
        - The shift is randomly drawn from a normal distribution.

    * Do this test only to Tract=8767 
        - The real galaxy catalog is from Hiranao's shape catalog: `8767.fits`
        - Only include galaxies with `cmodel_mag <= 23.9` -> `8767_cmodel_24.0.fits`
        - The mean Re of fake galaxies is around 0.3 arcsec, so let mu=0.6, sigma=0.6

    * Command: 
        ``` bash 
        python makeBlendedCat.py full_8767_radec_I.fits 8767_cmodel_24.0.fits
        ```
        - Output: `full_8767_radec_I_highb.fits` -- **36237** objects
        - Copy to `full_8767_radec_R_highb.fits`
        - Manually adjust the magnitude for `full_8767_radec_G_highb.fits`


----

## fakePipe Test: 

### Setup the environment: 

    * Commands: 
        - One should adjust the directory according to their installation.

    ``` bash 
    # Setup HSC environment on Master:
    . /data1a/ana/products2014/eups/default/bin/setups.sh 
    
    # Setup hscPipe:
    setup -v hscPipe 4.0.1 

    # Setup the Astrometry catalog:
    setup -v -j astrometry_net_data ps1_pv1.2c

    # Setup the TMV library (Used by Galsim)
    setup -v -j -r /home/clackner/src/tmv0.72/ 

    # Setup the Galsim library (Used by fakePipe)
    setup -v -j -r /home/song/code/GalSim-1.3.0/ 

    # Setup the fakePipe
    setup -v -r /home/song/work/fakes 
    ```

----- 

### 1. Tract=8766; Full catalog: `full_8766`

##########################################################################################

#### runAddFake.py

    * Add fake galaxies to single visits.
    * Under: `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a/`

##### HSC-I: `add_i` 

    * Config file: `addfake_8766_i_full.config` 

    * Command: `42862.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/full_8766 \
        --id visit="7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484" \
        --clobber-config -C addfake_8766_i_full.config \
        --queue small --job add_i_8766_full --nodes 9 --procs 12
    ```
        - Running ...

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/full_8766 7300 40
    ```
        - `full_8766-7300-40.png`


##### HSC-G: `add_g` 

    * Config file: `addfake_8766_g_full.config` 

    * Command: `42863.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/full_8766 \
        --id visit="9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536" \
        --clobber-config -C addfake_8766_g_full.config \
        --queue small --job add_g_8766_full --nodes 9 --procs 12
    ```
        - Running ...

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/full_8766 9852 50
    ```
        - `full_8766-9852-50.png`


##### HSC-R: `add_r` 

    * Config file: `addfake_8766_r_full.config` 

    * Command: `42864.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/full_8766 \
        --id visit="11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144" \
        --clobber-config -C addfake_8766_r_full.config \
        --queue small --job add_r_8766_full --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/full_8766 11442 50
    ```
        - `full_8766-11442-50.png`

##########################################################################################

#### stack.py

    * Generate coadd images.
    * Under: `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a/`

##### HSC-I band: 

    * Command: `42889.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/full_8766 \
        --job=stack_i_8766_full --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08766 filter=HSC-I --selectId ccd=0..8^10..103 visit=7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484
    ```
        - Running ...

    * Warnings: 
    ``` bash 
    2016-01-06T04:07:23:  WARNING: No data found for dataId=OrderedDict([('ccd', 24), ('visit', 19396)])
    2016-01-06T04:07:25:  WARNING: No data found for dataId=OrderedDict([('ccd', 58), ('visit', 19482)])
    2016-01-06T04:07:25:  WARNING: No data found for dataId=OrderedDict([('ccd', 63), ('visit', 19466)])
    2016-01-06T04:07:25:  WARNING: No data found for dataId=OrderedDict([('ccd', 67), ('visit', 7344)])
    2016-01-06T04:07:25:  WARNING: No data found for dataId=OrderedDict([('ccd', 69), ('visit', 19468)])
    2016-01-06T04:07:26:  WARNING: No data found for dataId=OrderedDict([('ccd', 84), ('visit', 7408)])
    2016-01-06T04:07:27:  WARNING: No data found for dataId=OrderedDict([('ccd', 96), ('visit', 7356)])
    ```

    * Visually check the results: 
        - Show in DS9, check the Cyan box for FAKE mask plane:
        ``` bash
        python showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/full_8766 8766 6,6 --filter HSC-I
        ```
        - See: `fake_on_coadd_example.png`

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/full_8766 8766 6,6 HSC-I
        ```
            - See: `full_8766-8766-6,6-HSC-I.png`

##### HSC-G band: 

    * Command: `42886.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/full_8766 \
        --job=stack_g_8766_full --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08766 filter=HSC-G --selectId ccd=0..8^10..103 visit=9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536
    ```
        - Finished

    * Warnings: 
    ``` bash 
    2016-01-06T04:02:27:  WARNING: No data found for dataId=OrderedDict([('ccd', 103), ('visit', 11582)])
    ```

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/full_8766 8766 6,4 HSC-G
        ```
            - See: `full_8766-8766-6,4-HSC-G.png`

##### HSC-R band: 

    * Command: `42887.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/full_8766 \
        --job=stack_r_8766_full --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08766 filter=HSC-R --selectId ccd=0..8^10..103 visit=11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144
    ```
        - Finished

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/full_8766 8766 4,5 HSC-R
        ```
            - See: `full_8766-8766-4,5-HSC-R.png`

##########################################################################################

#### multiband.py 

    * Config file: `multi.config` under `multiband`
    ``` Python
    root.measureCoaddSources.propagateFlags.flags={}
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.clobberMergedDetections = True
    root.clobberMeasurements = True
    root.clobberMergedMeasurements = True
    root.clobberForcedPhotometry = True
    ```
        - Right now, the `detectFakeOnly` option is still not available,
          so the process will try to measure everything, including the real galaxies. 

    * Command: `44492.master`
    ``` bash
    multiBand.py /lustre/Subaru/SSP --rerun=song/fake/full_8766 \
        --job=multi_8766_full --queue small --nodes 9 --procs 12 \
        --time=1000000 --batch-type=pbs --mpiexec="-bind-to socket" \
        --id tract=8766 filter=HSC-I^HSC-R^HSC-G --clobber-config -C multi.config
    ```
        - Running ...

##########################################################################################

#### runMatchFakes.py

    * Results are under: `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a/match`

##### HSC-I band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/full_8766 8766 \
        -f HSC-I -c full_8766_radec_I.fits -o full_8766_I_multiband -w -t 1.5 -m
    ```
        - `full_8766_I_multiband.fits`

##### HSC-G band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/full_8766 8766 \
        -f HSC-G -c full_8766_radec_G.fits -o full_8766_G_multiband -w -t 1.5 -m
    ```
        - `full_8766_G_multiband.fits`

##### HSC-R band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/full_8766 8766 \
        -f HSC-R -c full_8766_radec_R.fits -o full_8766_R_multiband -w -t 1.5 -m
    ```
        - `full_8766_R_multiband.fits`

##########################################################################################



-----

### 2. Tract-8767; Bright galaxies: `bright_8767`

##########################################################################################

#### runAddFakes.py

##### HSC-I: `add_i` 

    * Config file: `addfake_8767_i_bright.config` 

    * Command: `42893.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/bright_8767 \
        --id visit="7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486" \
        --clobber-config -C addfake_8767_i_bright.config \
        --queue small --job add_i_8767_bright --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/bright_8767 7304 40
    ```
        - `bright_8767-7304-40.png`

##### HSC-G: `add_g` 

    * Config file: `addfake_8767_g_bright.config` 

    * Command: `42894.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/bright_8767 \
        --id visit="9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540" \
        --clobber-config -C addfake_8767_g_bright.config \
        --queue small --job add_g_8767_bright --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/bright_8767 9872 50
    ```
        - `bright_8767-9872-50.png`

##### HSC-R: `add_r` 

    * Config file: `addfake_8767_r_bright.config` 

    * Command: `42895.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/bright_8767 \
        --id visit="11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148" \
        --clobber-config -C addfake_8767_r_bright.config \
        --queue small --job add_r_8767_bright --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/bright_8767 11470 50
    ```
        - `bright_8767-11470-50.png`

##########################################################################################

#### stack.py 

##### HSC-I band: 

    * Command: `42902.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/bright_8767 \
        --job=stack_i_8767_bright --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-I --selectId ccd=0..8^10..103 visit=7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486
    ```
        - Finished 

    * Visually check the results: 
        - Show in DS9, check the Cyan box for FAKE mask plane:
        ``` bash
        python showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/bright_8767 8767 6,6 --filter HSC-I
        ```

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/bright_8767 8767 6,6 HSC-I
        ```
            - See: `bright_8767-8767-6,6-HSC-I.png`

##### HSC-G band: 

    * Command: `42901.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/bright_8767 \
        --job=stack_g_8767_bright --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-G --selectId ccd=0..8^10..103 visit=9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540
    ```
        - Finished

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/bright_8767 8767 6,6 HSC-G
        ```
            - See: `bright_8767-8767-6,6-HSC-G.png`

##### HSC-R band: 

    * Command: `42903.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/bright_8767 \
        --job=stack_r_8767_bright --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-R --selectId ccd=0..8^10..103 visit=11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148
    ```
        - Finished

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/bright_8767 8767 6,6 HSC-R
        ```
            - See: `bright_8767-8767-6,6-HSC-R.png`

##########################################################################################

#### multiband.py 

    * Config file: `multi.config` under `multiband`
    ``` Python
    root.measureCoaddSources.propagateFlags.flags={}
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.clobberMergedDetections = True
    root.clobberMeasurements = True
    root.clobberMergedMeasurements = True
    root.clobberForcedPhotometry = True    ```
        - Right now, the `detectFakeOnly` option is still not available,
          so the process will try to measure everything, including the real galaxies. 

    * Command: `44493.master`
    ``` bash
    multiBand.py /lustre/Subaru/SSP --rerun=song/fake/bright_8767 \
        --job=multi_8767_bright --queue small --nodes 9 --procs 12 \
        --time=1000000 --batch-type=pbs --mpiexec="-bind-to socket" \
        --id tract=8767 filter=HSC-I^HSC-R^HSC-G --clobber-config -C multi.config
    ```
        - Running ...

##########################################################################################

#### runMatchFakes.py

    * Results are under: `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a/match`

##### HSC-I band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/bright_8767 8767 \
        -f HSC-I -c bright_8767_radec_I.fits -o bright_8767_I_multiband -w -t 1.5 -m
    ```
        - `bright_8767_I_multiband.fits`

##### HSC-G band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/bright_8767 8767 \
        -f HSC-G -c bright_8767_radec_G.fits -o bright_8767_G_multiband -w -t 1.5 -m
    ```
        - `bright_8767_G_multiband.fits`

##### HSC-R band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/bright_8767 8767 \
        -f HSC-R -c bright_8767_radec_R.fits -o bright_8767_R_multiband -w -t 1.5 -m
    ```
        - `bright_8767_R_multiband.fits`

##########################################################################################





-----

### 3. Tract-8767; Blended objects: `blend_8767`

##########################################################################################

#### runAddFakes.py

##### HSC-I: `add_i` 

    * Config file: `addfake_8767_i_blend.config` 

    * Command: `42888.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/blend_8767 \
        --id visit="7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486" \
        --clobber-config -C addfake_8767_i_blend.config \
        --queue small --job add_i_8767_blend --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/blend_8767 7304 41
    ```
        - `blend_8767-7304-41.png`

##### HSC-G: `add_g` 

    * Config file: `addfake_8767_g_blend.config` 

    * Command: `42890.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/blend_8767 \
        --id visit="9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540" \
        --clobber-config -C addfake_8767_g_blend.config \
        --queue small --job add_g_8767_blend --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/blend_8767 9872 50
    ```
        - `blend_8767-9872-50.png`

##### HSC-R: `add_r` 

    * Config file: `addfake_8767_r_blend.config` 

    * Command: `42891.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/blend_8767 \
        --id visit="11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148" \
        --clobber-config -C addfake_8767_r_blend.config \
        --queue small --job add_r_8767_blend --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/blend_8767 11508 50
    ```
        - `blend_8767-11470-50.png`

##########################################################################################

#### stack.py 

##### HSC-I band: 

    * Command: `42898.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/blend_8767 \
        --job=stack_i_8767_blend --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-I --selectId ccd=0..8^10..103 visit=7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486
    ```
        - Finished 

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/blend_8767 8767 5,5 HSC-I
        ```
            - See: `blend_8767-8767-5,5-HSC-I.png`

##### HSC-G band: 

    * Command: `42897.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/blend_8767 \
        --job=stack_g_8767_blend --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-G --selectId ccd=0..8^10..103 visit=9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540
    ```
        - Finished

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/blend_8767 8767 6,6 HSC-G
        ```
            - See: `blend_8767-8767-6,6-HSC-G.png`

##### HSC-R band: 

    * Command: `42896.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/blend_8767 \
        --job=stack_r_8767_blend --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-R --selectId ccd=0..8^10..103 visit=11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148
    ```
        - Finished

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/blend_8767 8767 6,7 HSC-R
        ```
            - See: `blend_8767-8767-6,7-HSC-R.png`

##########################################################################################

#### multiband.py 

    * Config file: `multi.config` under `multiband`
    ``` Python
    root.measureCoaddSources.propagateFlags.flags={}
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.clobberMergedDetections = True
    root.clobberMeasurements = True
    root.clobberMergedMeasurements = True
    root.clobberForcedPhotometry = True
    ```
        - Right now, the `detectFakeOnly` option is still not available,
          so the process will try to measure everything, including the real galaxies. 

    * Command: `44497.master`
    ``` bash
    multiBand.py /lustre/Subaru/SSP --rerun=song/fake/blend_8767 \
        --job=multi_8767_blend --queue small --nodes 9 --procs 12 \
        --time=1000000 --batch-type=pbs --mpiexec="-bind-to socket" \
        --id tract=8767 filter=HSC-I^HSC-R^HSC-G --clobber-config -C multi.config
    ```
        - Finished

##########################################################################################

#### runMatchFakes.py

    * Results are under: `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a/match`

##### HSC-I band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/blend_8767 8767 \
        -f HSC-I -c full_8767_radec_I_highb.fits -o blend_8767_I_multiband -w -t 1.5 -m
    ```
        - `blend_8767_I_multiband.fits`

##### HSC-G band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/blend_8767 8767 \
        -f HSC-G -c full_8767_radec_G_highb.fits -o blend_8767_G_multiband -w -t 1.5 -m
    ```
        - `blend_8767_G_multiband.fits`

##### HSC-R band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/blend_8767 8767 \
        -f HSC-R -c full_8767_radec_R_highb.fits -o blend_8767_R_multiband -w -t 1.5 -m
    ```
        - `blend_8767_R_multiband.fits`

##########################################################################################



-----

### 4. Tract-8767; Full catalog: `full_8767`

##########################################################################################

#### runAddFakes.py

##### HSC-I: `add_i` 

    * Config file: `addfake_8767_i_full.config` 

    * Command: `43118.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/full_8767 \
        --id visit="7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486" \
        --clobber-config -C addfake_8767_i_full.config \
        --queue small --job add_i_8767_full --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/full_8767 7304 40
    ```
        - `full_8767-7304-40.png`

##### HSC-G: `add_g` 

    * Config file: `addfake_8767_g_full.config` 

    * Command: `43119.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/full_8767 \
        --id visit="9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540" \
        --clobber-config -C addfake_8767_g_full.config \
        --queue small --job add_g_8767_full --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/full_8767 9872 50
    ```
        - `full_8767-9872-50.png`

##### HSC-R: `add_r` 

    * Config file: `addfake_8767_r_full.config` 

    * Command: `43197.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/full_8767 \
        --id visit="11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148" \
        --clobber-config -C addfake_8767_r_full.config \
        --queue small --job add_r_8767_full --nodes 8 --procs 10
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/full_8767 11508 50
    ```
        - `full_8767-11470-50.png`

##########################################################################################

#### stack.py 

##### HSC-I band: 

    * Command: `43145.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/full_8767 \
        --job=stack_i_8767_full --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-I --selectId ccd=0..8^10..103 visit=7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486
    ```
        - Finished 

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/full_8767 8767 5,5 HSC-I
        ```
            - See: `full_8767-8767-5,5-HSC-I.png`

##### HSC-G band: 

    * Command: `43183.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/full_8767 \
        --job=stack_g_8767_full --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-G --selectId ccd=0..8^10..103 visit=9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540
    ```
        - Finished 

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/full_8767 8767 6,6 HSC-G
        ```
            - See: `full_8767-8767-6,6-HSC-G.png`

##### HSC-R band: 

    * Command: `43290.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/full_8767 \
        --job=stack_r_8767_full --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-R --selectId ccd=0..8^10..103 visit=11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148
    ```
        - Finished

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/full_8767 8767 6,7 HSC-R
        ```
            - See: `full_8767-8767-6,7-HSC-R.png`

##########################################################################################

#### multiband.py 

    * Config file: `multi.config` under `multiband`
    ``` Python
    root.measureCoaddSources.propagateFlags.flags={}
    root.clobberMergedDetections = True
    root.clobberMeasurements = True
    root.clobberMergedMeasurements = True
    root.clobberForcedPhotometry = True 
    ```
        - Right now, the `detectFakeOnly` option is still not available,
          so the process will try to measure everything, including the real galaxies. 

    * Command: `43292.master`
    ``` bash
    multiBand.py /lustre/Subaru/SSP --rerun=song/fake/full_8767 \
        --job=multi_8767_full --queue small --nodes 9 --procs 12 \
        --time=1000000 --batch-type=pbs --mpiexec="-bind-to socket" \
        --id tract=8767 filter=HSC-I^HSC-R^HSC-G --clobber-config -C multi.config
    ```
        - Finished


#### multiband.py with fix of cMoldel by Jim Bosch:

    * Config file: `multi.config` under `multiband`
    ``` Python
    root.measureCoaddSources.propagateFlags.flags={}
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.clobberMergedDetections = True
    root.clobberMeasurements = True
    root.clobberMergedMeasurements = True
    root.clobberForcedPhotometry = True 

    * Command: `44243.master`
    ``` bash
    multiBand.py /lustre/Subaru/SSP --rerun=song/fake/full_8767 \
        --job=multi_8767_full --queue small --nodes 9 --procs 12 \
        --time=1000000 --batch-type=pbs --mpiexec="-bind-to socket" \
        --id tract=8767 filter=HSC-I^HSC-R^HSC-G --clobber-config -C multi.config
    ```
        - Finished


##########################################################################################

#### runMatchFakes.py

    * Results are under: `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a/match`

##### HSC-I band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/full_8767 8767 \
        -f HSC-I -c full_8767_radec_I.fits -o full_8767_I_multiband -w -t 1.5 -m
    ```
        - `full_8767_I_multiband.fits`

##### HSC-G band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/full_8767 8767 \
        -f HSC-G -c full_8767_radec_G.fits -o full_8767_G_multiband -w -t 1.5 -m
    ```
        - `full_8767_G_multiband.fits`

##### HSC-R band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/full_8767 8767 \
        -f HSC-R -c full_8767_radec_R.fits -o full_8767_R_multiband -w -t 1.5 -m
    ```
        - `full_8767_R_multiband.fits`

##########################################################################################





-----

### 5. Tract-8767; Highly blended objects: `tight_8767`

##########################################################################################

#### runAddFakes.py

##### HSC-I: `add_i` 

    * Config file: `addfake_8767_i_tight.config` 

    * Command: `43184.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/tight_8767 \
        --id visit="7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486" \
        --clobber-config -C addfake_8767_i_tight.config \
        --queue small --job add_i_8767_tight --nodes 9 --procs 12
    ```
        - Finished 

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/tight_8767 7304 41
    ```
        - `tight_8767-7304-41.png`


##### HSC-G: `add_g` 

    * Config file: `addfake_8767_g_tight.config` 

    * Command: `43185.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/tight_8767 \
        --id visit="9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540" \
        --clobber-config -C addfake_8767_g_tight.config \
        --queue small --job add_g_8767_tight --nodes 9 --procs 12
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/tight_8767 9872 50
    ```
        - `tight_8767-9872-50.png`

##### HSC-R: `add_r` 

    * Config file: `addfake_8767_r_tight.config` 

    * Command: `43196.master` 
    ``` bash
    runAddFakes.py /lustre/Subaru/SSP/ \
        --rerun DR_S16A:song/fake/tight_8767 \
        --id visit="11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148" \
        --clobber-config -C addfake_8767_r_tight.config \
        --queue small --job add_r_8767_tight --nodes 8 --procs 10
    ```
        - Finished

    * Visually check the results: 
    ``` bash 
    python compFakeGalaxy.py DR_S16A song/fake/tight_8767 11508 52
    ```
        - `tight_8767-11470-52.png`

##########################################################################################

#### stack.py 

##### HSC-I band: 

    * Command: ``
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/tight_8767 \
        --job=stack_i_8767_tight --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-I --selectId ccd=0..8^10..103 visit=7288^7292^7296^7304^7308^7310^7312^7318^7320^7322^7338^7340^7342^7346^7348^7352^7354^7358^7360^7372^7374^7384^7386^7388^19400^19404^19416^19418^19456^19470^19484^19486
    ```
        - Finished 

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/tight_8767 8767 5,5 HSC-I
        ```
            - See: `tight_8767-8767-5,5-HSC-I.png`

##### HSC-G band: 

    * Command: `43193.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/tight_8767 \
        --job=stack_g_8767_tight --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-G --selectId ccd=0..8^10..103 visit=9840^9844^9848^9856^9860^9862^9866^9870^9872^9882^9884^9888^9900^9902^9904^9906^9912^9914^9918^11564^11572^11576^11578^11580^11584^11588^11590^11598^11600^42460^42464^42468^42500^42514^42516^42536^42538^42540
    ```
        - Finished

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/tight_8767 8767 6,6 HSC-G
        ```
            - See: `tight_8767-8767-6,6-HSC-G.png`

##### HSC-R band: 

    * Command: `42942.master`
    ``` bash 
    stack.py /lustre/Subaru/SSP --rerun=song/fake/tight_8767 \
        --job=stack_r_8767_tight --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=08767 filter=HSC-R --selectId ccd=0..8^10..103 visit=11426^11430^11434^11446^11450^11468^11470^11472^11478^11480^11498^11500^11506^11508^11534^11536^41068^41072^41076^41108^41122^41124^41144^41146^41148
    ```
        - Finished

    * Generate a before-after comparison plot: 
        ``` bash
        python compFakeCoadd.py DR_S16A song/fake/tight_8767 8767 6,7 HSC-R
        ```
            - See: `tight_8767-8767-6,7-HSC-R.png`

##########################################################################################

#### multiband.py 

    * Config file: `multi.config` under `multiband`
    ``` Python
    root.measureCoaddSources.propagateFlags.flags={}
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.clobberMergedDetections = True
    root.clobberMeasurements = True
    root.clobberMergedMeasurements = True
    root.clobberForcedPhotometry = True    
    ```
        - Right now, the `detectFakeOnly` option is still not available,
          so the process will try to measure everything, including the real galaxies. 

    * Command: `44503.master`
    ``` bash
    multiBand.py /lustre/Subaru/SSP --rerun=song/fake/tight_8767 \
        --job=multi_8767_tight --queue small --nodes 9 --procs 12 \
        --time=1000000 --batch-type=pbs --mpiexec="-bind-to socket" \
        --id tract=8767 filter=HSC-I^HSC-R^HSC-G --clobber-config -C multi.config
    ```
        - Finished

##########################################################################################

#### runMatchFakes.py

    * Results are under: `/lustre/Subaru/SSP/rerun/song/fake/dr_s16a/match`

##### HSC-I band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/tight_8767 8767 \
        -f HSC-I -c full_8767_radec_I_tight.fits -o tight_8767_I_multiband -w -t 1.5 -m
    ```
        - `tight_8767_I_multiband.fits`

##### HSC-G band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/tight_8767 8767 \
        -f HSC-G -c full_8767_radec_G_tight.fits -o tight_8767_G_multiband -w -t 1.5 -m
    ```
        - `tight_8767_G_multiband.fits`

##### HSC-R band 

    * Command: 
    ``` bash 
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/tight_8767 8767 \
        -f HSC-R -c full_8767_radec_R_tight.fits -o tight_8767_R_multiband -w -t 1.5 -m
    ```
        - `tight_8767_R_multiband.fits`

##########################################################################################
