# Basic SynPipe Photometric Tests 

---- 

* by Song Huang (Kavli-IPMU)

----

## Introduction 

* These are the basic photometric tests using `SynPipe` and `hscPipe` version 4.0.5, and 
  also for the technical paper for SynPipe.  
* We will test using synthetic point sources and galaxies in five bands and selected
  Tracts that represent good and bad seeing.  
* We will also test the half million QSO-like point sources from Ji-Jia. 

----

## Preparation 

### Data Storage: 

* The metadata and results are kept on Master@IPMU, under Song Huang's working directory:
    ```
    /lustre/Subaru/SSP/rerun/song/fake/synpipe
    ```

### Tract Selection: 

* We select Tract=`9699` in VVDS chunk as Tract with very good seeing: <0.449 arcsec>
* We select Tract=`8764` in XMM-LSS chunk as Tract with bad seeing: <0.700 arcsec>
* Ji-Jia selected Tract=`9693` for his test 

### Regions with Useful Data within the Tract:

* These are files that define the regions of useful data within each Tract in each band 
  that are generated using script by Song Huang.  
* File `synpipe_test_tract.lis` contains the IDs of these three Tracts.

* Command: 
    ```
    ./batchShapeComb.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-G dr1_s16a 
    ./batchShapeComb.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-R dr1_s16a 
    ./batchShapeComb.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-I dr1_s16a 
    ./batchShapeComb.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-Z dr1_s16a 
    ./batchShapeComb.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-Y dr1_s16a 
    ```

* All the three Tracts are fully covered, not necessary to combine the region files for
  all five bands.

* Useful files, under `/lustre/Subaru/SSP/rerun/song/fake/synpipe/mask/`:
    ```
    dr1_s16a_9693_HSC-I_shape_all.wkb 
    dr1_s16a_9699_HSC-I_shape_all.wkb
    dr1_s16a_8764_HSC-I_shape_all.wkb
    ```

### Regions with Problematic Data: 

* These are files that define the regions with problematic pixels like the interpolated
  ones, and they are also generated using script by Song Huang. 

* Command:
    ```
    ./batchNoData.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-G dr1_s16a 
    ./batchNoData.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-R dr1_s16a 
    ./batchNoData.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-I dr1_s16a 
    ./batchNoData.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-Z dr1_s16a 
    ./batchNoData.sh synpipe_test_tract.lis /lustre2/HSC_DR/dr1/s15b/data/s15b_wide HSC-Y dr1_s16a 
    ```

* Combine the regions files in five bands together using function `combineWkbFiles()`
  under `coaddPatchNoData.py`; Example commands: 
    ``` python 
    from coaddPatchNoData import combineWkbFiles as cwf
    from coaddPatchNoData import showNoDataMask as show 

    cwb('dr1_s16a_8764_nodata_all.lis', output='dr1_s16a_8764_nodata_all.wkb') 
    show('dr1_s16a_8764_nodata_all.wkb', pngName='dr1_s16a_8764_nodata_all.png')
    ```

* Useful files, under `/lustre/Subaru/SSP/rerun/song/fake/synpipe/mask/`
    ```
    dr1_s16a_8764_nodata_all.wkb 
    dr1_s16a_8764_nodata_big.wkb 
    dr1_s16a_9693_nodata_all.wkb 
    dr1_s16a_9693_nodata_big.wkb 
    dr1_s16a_9699_nodata_all.wkb 
    dr1_s16a_9699_nodata_big.wkb 
    ```

### List of Visits that belong to each Tract: 

* Find all the Visits that are used to generate the coadd images in the Tract.  

* Using script within SynPipe. Example command: 
    ```
    tractFindVisits.py s15b_wide 9693 --filter='HSC-G' --dataDir='/lustre2/HSC_DR/dr1/s15b/data/'
    showTractVisit.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9693 6306^6322^6328^6334^6346^34334^34370^34380^34410^34428^34430^34452^38306^38310^38314^38316^38318^38324^38326^38330^38332^38342^38344^38346 -p -f HSC-I
    ```

* Also define corresponding environmental parameters for later usage

#### Tract=9693: 

* HSC-G: 24 visits
    ```
6306^6322^6328^6334^6346^34334^34370^34380^34410^34428^34430^34452^38306^38310^38314^38316^38318^38324^38326^38330^38332^38342^38344^38346
    ```

* HSC-R: 21 visits 
    ```
7124^7140^7146^7152^7164^11394^34636^34656^34668^34684^34694^34710^40754^40758^40762^40764^40766^40772^40774^40778^40780
    ```

* HSC-I: 33 visits 
    ```
14090^14094^35862^35874^35878^35888^35894^35896^35902^35908^35916^35922^35924^35926^35938^35940^35942^35952^35954^37978^37982^37986^37988^37990^37992^37994^37996^38000^38002^38008^38010^38014^38016
    ```

* HSC-Z: 33 visits 
    ```
9626^9684^9686^33890^33894^33904^33906^33908^33914^33916^33924^33926^33928^33930^33936^33938^33940^33946^33948^38878^38882^38886^38888^38890^38892^38894^38896^38900^38902^38908^38910^38914^38916
    ```

* HSC-Y: 33 visits 
    ```
13136^13138^34886^34888^34890^34892^34894^34896^34906^34908^34930^34932^34934^34936^36742^36764^36796^36814^36832^37522^37526^37530^37532^37534^37536^37538^37540^37544^37546^37552^37554^37558^37560
    ```

#### Tract=9699:

* HSC-G: 25 visits 
    ```
34358^34386^34388^34390^34392^34394^34396^34398^34416^34418^34420^34444^34446^38378^38382^38394^38414^38444^38446^38450^38452^38454^42144^42146^42156
    ```

* HSC-R: 25 visits 
    ```
34718^34722^34726^34730^34738^34740^34742^34744^34746^34752^34754^34756^34762^34768^34770^34774^34808^34812^34814^40788^40800^40806^40808^40812^40816
    ```

* HSC-I: 37 visits 
    ```
36122^36128^36132^36136^36152^36156^36160^36162^36164^36166^36168^36176^36178^36184^36186^36188^36190^36206^36208^36210^36220^36222^36232^36242^36244^36254^36256^36264^36266^38024^38044^38050^38052^38056^38060^38064^38068
    ```

* HSC-Z: 37 visits 
    ```
36430^38920^38924^38928^38930^38932^38934^38936^38938^38942^38946^38952^38956^38958^38962^38966^38970^38972^38974^38976^38978^38980^38984^38986^38988^38992^38994^38998^39000^39008^39016^39018^39020^39024^39028^44462^44466
    ```

* HSC-Y: 27 visits 
    ```
36734^36758^36760^36776^36826^36876^36878^36880^37564^37566^37570^37572^37574^37612^37624^37628^44010^44012^44014^44016^44020^44022^44024^44028^44030^44034^44036
    ```

#### Tract=8764: 

* HSC-G: 25 visits
    ```
11616^11624^11636^11640^11652^11654^11656^11674^15196^15214^15226^42428^42432^42448^42452^42472^42474^42498^42506^42508^42510^42520^42522^42530^42532
    ```

* HSC-R: 25 visits 
    ```
11418^11438^11464^11474^11492^11494^11502^11530^11550^11552^11554^41036^41040^41056^41060^41080^41082^41106^41114^41116^41118^41128^41130^41138^41140
    ```

* HSC-I: 37 visits 
    ```    
7398^7410^7412^7414^7416^7424^14134^14138^14148^14150^14168^14170^14180^14182^19388^19392^19408^19410^19412^19424^19426^19450^19452^19464^19466^19478^19480^45858^45862^45868^45870^45894^45896^45902^45904^45910^45912
    ```

* HSC-Z: 33 visits
    ```
9786^13278^13282^13286^13306^15080^15084^15086^15092^15098^15122^15134^15146^15158^17664^17668^17684^17686^17690^17702^17704^17718^17720^17734^17736^17746^17748^44630^44634^44648^44650^44676^44678
    ```

* HSC-Y: 37 visits 
    ```
6534^13184^13188^13196^13214^13216^13224^13226^13244^13254^16088^16094^16102^16110^39336^39356^39358^39360^39362^39364^39366^44092^44104^44110^44114^44120^44122^44126^44136^44142^44148^44150^44156^44158^44162^44164^44166
    ```

---- 

## Input Catalogs 

### Ji-Jia's QSO catalogs: 

* 500000 objects with magnitudes in all five bands: `jijia_qso_test.fits`

* Catalogs used for inputs: `jijia_qso_test_HSC-G/R/I/Z/Y.fits`

### Stars from S16A WIDE:

* These are stars with $i_{PSF} < 26.5$ in the VVDS chunk.  They have been filtered with
  basic quality cuts, and they have low `blendedness`, not within region affected by
  bright objects.  We have checked their color-color distributions, and they behave as
  expected.

* Input catalog: `dr1_s16a_star_vvds_i26.5_input.fits`

#### Generate Input Catalogs for Tract=9699

* Command: 
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=9699 filter='HSC-I' patch='4,4' \
        -c inputCat='dr1_s16a_star_vvds_i26.5_input.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=1500 \
        rejMask='dr1_s16a_9699_nodata_all.wkb' \
        acpMask='dr1_s16a_9699_HSC-I_shape_all.wkb'
    ```

* **119616** objects are included.  
    - Files: `star_9699_HSC-G/R/I/Z/Y.fits` 

#### Generate Input Catalogs for Tract=8764

* Command: 
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=8764 filter='HSC-I' patch='4,4' \
        -c inputCat='dr1_s16a_star_vvds_i26.5_input.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=1500 \
        rejMask='dr1_s16a_8764_nodata_all.wkb' \
        acpMask='dr1_s16a_8764_HSC-I_shape_all.wkb'
    ```

* **120363** objects are included.  
    - Files: `star_8764_HSC-G/R/I/Z/Y.fits` 


### Galaxies from Claire's COSMOS catalog 

#### Assign realistic optical colors to fake galaxies

* TODO: Fill more details later
* `cosmos_mag25.2_shuang_multiband_phocolor_short.fits`

#### Generate Input Catalogs for Tract=9699; Full magnitude range; Full Sersic index range

* Command: 
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=9699 filter='HSC-I' patch='4,4' \
        -c inputCat='cosmos_mag25.2_shuang_multiband_phocolor_short.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=500 \
        rejMask='dr1_s16a_9699_nodata_all.wkb' \
        acpMask='dr1_s16a_9699_HSC-I_shape_all.wkb'
    ```

* **39869** objects are included.  
    - Files: `galaxy_all_9699_HSC-G/R/I/Z/Y.fits` 

#### Generate Input Catalogs for Tract=8764; Full magnitude range; Full Sersic index range

* Command: 
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=8764 filter='HSC-I' patch='4,4' \
        -c inputCat='cosmos_mag25.2_shuang_multiband_phocolor_short.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=500 \
        rejMask='dr1_s16a_8764_nodata_all.wkb' \
        acpMask='dr1_s16a_8764_HSC-I_shape_all.wkb'
    ```

* **40115** objects are included.  
    - Files: `galaxy_all_8764_HSC-G/R/I/Z/Y.fits` 


----

## Add Fake Galaxies to Single Visits 

### Point Sources in Tract=9699 

#### Prepare Config Files

* Example config file: 
    ```
    from fakes import positionStarFakes
    
    root.fakes.retarget(positionStarFakes.PositionStarFakesTask)
    root.fakes.starList = 'star_9699_HSC-G.fits'
    ```

* Config files: `star_9699_HSC-G/R/I/Z/Y.config`

#### runAddFakes.py

* Commands 
    - `HSC-G`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$G9699 \
            --clobber-config -C star_9699_HSC-G.config \
            --queue small --job star_add_G --nodes 9 --procs 12
        ```
        * Start: 10/24/18:04; Finished: 10/24/19:31 
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 34386 40
            ```
            - Looks Ok: `star1-34386-40.png`

    - `HSC-R`:
        ``
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$R9699 \
            --clobber-config -C star_9699_HSC-R.config \
            --queue small --job star_add_R --nodes 9 --procs 12
        ```
        * Start: 10/25/05:03; Finished: 10/25/06:20  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 34726 40
            ```
            - Looks Ok: `star1-34726-40.png`

    - `HSC-I`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$I9699 \
            --clobber-config -C star_9699_HSC-I.config \
            --queue small --job star_add_I --nodes 9 --procs 12
        ```
        * Start: 10/25/06:20; Finished: 10/25/08:12  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 36132 40
            ```
            - Looks Ok: `star1-36132-40.png`

    - `HSC-Z`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$Z9699 \
            --clobber-config -C star_9699_HSC-Z.config \
            --queue small --job star_add_Z --nodes 9 --procs 12
        ```
        * Start: 10/25/08:12; Finished: 10/25/10:06  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 38932 40
            ```
            - Looks Ok: `star1-38932-40.png`

    - `HSC-Y`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$Y9699 \
            --clobber-config -C star_9699_HSC-Y.config \
            --queue small --job star_add_Y --nodes 9 --procs 12
        ```
        * Start: 10/25/08:43; Finished: 10/25/10:15  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 36760 40
            ```
            - Looks Ok: `star1-36760-40.png`



### Point Sources in Tract=8764 

#### Prepare Config Files

* Example config file: 
    ```
    from fakes import positionStarFakes
    
    root.fakes.retarget(positionStarFakes.PositionStarFakesTask)
    root.fakes.starList = 'star_8764_HSC-G.fits'
    ```

* Config files: `star_8764_HSC-G/R/I/Z/Y.config`

#### runAddFakes.py

* Commands 
    - `HSC-G`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$G8764 \
            --clobber-config -C star_8764_HSC-G.config \
            --queue small --job star2_add_G --nodes 9 --procs 12
        ```
        * Submit: 10/24/21:47; 
        * Start: 10/25/10:15; Finished: 10/25/11:46  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 42432 40
            ```
            - Looks Ok: `star2-42432-40.png`

    - `HSC-R`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$R8764 \
            --clobber-config -C star_8764_HSC-R.config \
            --queue small --job star2_add_R --nodes 9 --procs 12
        ```
        * Submit: 10/24/21:48; 
        * Start: 10/25/10:17; Finished: 10/25/11:35  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 41040 40
            ```
            - Looks Ok: `star2-41040-40.png`
    
    - `HSC-I`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$I8764 \
            --clobber-config -C star_8764_HSC-I.config \
            --queue small --job star2_add_I --nodes 9 --procs 12
        ```
        * Submit: 10/24/21:48; 
        * Start: 10/25/11:35; Finished: 10/25/13:29  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 14168 40
            ```
            - Looks Ok: `star2-14168-40.png`

    - `HSC-Z`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$Z8764 \
            --clobber-config -C star_8764_HSC-Z.config \
            --queue small --job star2_add_Z --nodes 9 --procs 12
        ```
        * Submit: 10/24/21:49; 
        * Start: 10/25/11:46; Finished: 10/25/13:44  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 15146 40
            ```
            - Looks Ok: `star2-15146-40.png`

    - `HSC-Y`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$Y8764 \
            --clobber-config -C star_8764_HSC-Y.config \
            --queue small --job star2_add_Y --nodes 9 --procs 12
        ```
        * Submit: 10/24/21:50; 
        * Start: 10/25/13:29; Finished: 10/25/15:33  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 16102 40
            ```
            - Looks Ok: `star2-16102-40.png`


### Ji-Jia's QSOs in Tract=9693

#### Prepare Config Files

* Example config file: 
    ```
    from fakes import positionStarFakes
    
    root.fakes.retarget(positionStarFakes.PositionStarFakesTask)
    root.fakes.starList = 'jijia_qso_HSC-G.fits'
    ```

* Config files: `jijia_qso_HSC-G/R/I/Z/Y.config`

#### runAddFakes.py

* Commands 
    - `HSC-G`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
            --id visit=$G9693 \
            --clobber-config -C jijia_qso_HSC-G.config \
            --queue small --job qso_add_G --nodes 9 --procs 12
        ```
        * Submit: 10/25/19:45; 
        * Start: 10/25/19:46; Finished: 10/25/23:02  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 38310 40
            ```
            - Looks Ok: `qso-38310-40.png`

    - `HSC-R`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
            --id visit=$R9693 \
            --clobber-config -C jijia_qso_HSC-R.config \
            --queue small --job qso_add_R --nodes 9 --procs 12
        ```
        * Submit: 10/25/20:06; 
        * Start: 10/25/20:07; Finished: 10/25/22:46
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 40758 40
            ```
            - Looks Ok: `qso-40758-40.png`

    - `HSC-I`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
            --id visit=$I9693 \
            --clobber-config -C jijia_qso_HSC-I.config \
            --queue small --job qso_add_I --nodes 9 --procs 12
        ```
        * Submit: 10/25/20:06; 
        * Start: 10/25/22:46; Finished: 10/26/02:54
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 35902 40
            ```
            - Looks Ok: `qso-35902-40.png`

    - `HSC-Z`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
            --id visit=$Z9693 \
            --clobber-config -C jijia_qso_HSC-Z.config \
            --queue small --job qso_add_Z --nodes 9 --procs 12
        ```
        * Submit: 10/26/07:34 
        * Start: 10/26/07:35; Finished: 10/26/12:02
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 33914 40
            ```
            - Looks Ok: `qso-33914-40.png`

    - `HSC-Y`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
            --id visit=$Y9693 \
            --clobber-config -C jijia_qso_HSC-Y.config \
            --queue small --job qso_add_Y --nodes 9 --procs 12
        ```
        * Submit: 10/25/20:06; 
        * Start: 10/26/01:55; Finished: 10/26/06:25
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 34892 40
            ```
            - Looks Ok: `qso-34892-40.png`


### Galaxies in Tract=9699 (Full magnitude and Sersic index range) 

#### Prepare Config Files

* Example config file: 
    ```
    from fakes import positionGalSimFakes
    root.fakes.retarget(positionGalSimFakes.PositionGalSimFakesTask)
    root.fakes.galList = 'galaxy_all_9699_HSC-G.fits'
    root.fakes.galType = 'sersic'
    root.fakes.maxMargin = 150
    root.fakes.addShear = False
    ```

* Config files: `galaxy_all_9699_HSC-G/R/I/Z/Y.config`

#### runAddFakes.py

* Commands 
    - `HSC-G`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 \
            --id visit=$G9699 \
            --clobber-config -C galaxy_all_9699_HSC-G.config \
            --queue small --job galA1_add_G --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:33; 
        * Start: 12/23/06:34; Finished: 10/25/07:29  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 34386 40
            ```
            - Looks Ok: `gal_all1-34386-40.png`

    - `HSC-R`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 \
            --id visit=$R9699 \
            --clobber-config -C galaxy_all_9699_HSC-R.config \
            --queue small --job galA1_add_R --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:36; 
        * Start: 12/23/06:36; Finished: 10/25/07:32  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 34726 40
            ```
            - Looks Ok: `gal_all1-34726-40.png`

    - `HSC-I`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 \
            --id visit=$I9699 \
            --clobber-config -C galaxy_all_9699_HSC-I.config \
            --queue small --job galA1_add_I --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:37; 
        * Start: 12/23/06:37; Finished: 10/25/07:59  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 36132 40
            ```
            - Looks Ok: `gal_all1-36132-40.png`

    - `HSC-Z`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 \
            --id visit=$Z9699 \
            --clobber-config -C galaxy_all_9699_HSC-Z.config \
            --queue small --job galA1_add_Z --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:38; 
        * Start: 12/23/07:29; Finished: 10/25/08:74  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 38932 40
            ```
            - Looks Ok: `gal_all1-38932-40.png`

    - `HSC-Y`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 \
            --id visit=$Y9699 \
            --clobber-config -C galaxy_all_9699_HSC-Y.config \
            --queue small --job galA1_add_Y --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:39; 
        * Start: 12/23/07:32; Finished: 10/25/08:30  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 36760 40
            ```
            - Looks Ok: `gal_all1-36760-40.png`


### Galaxies in Tract=8764 (Full magnitude and Sersic index range) 

#### Prepare Config Files

* Example config file: 
    ```
    from fakes import positionGalSimFakes
    root.fakes.retarget(positionGalSimFakes.PositionGalSimFakesTask)
    root.fakes.galList = 'galaxy_all_8764_HSC-G.fits'
    root.fakes.galType = 'sersic'
    root.fakes.maxMargin = 150
    root.fakes.addShear = False
    ```

* Config files: `galaxy_all_8764_HSC-G/R/I/Z/Y.config`

#### runAddFakes.py

* Commands 
    - `HSC-G`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /data3a/work/song/synpipe/gal_all2 \
            --id visit=$G8764 \
            --clobber-config -C galaxy_all_8764_HSC-G.config \
            --queue small --job galA2_add_G --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:41; 
        * Start: 12/23/07:59; Finished: 10/25/09:05  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /data3a/work/song/synpipe/gal_all2 42432 40
            ```
            - Looks Ok: `gal_all2-42432-40.png`

    - `HSC-R`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /data3a/work/song/synpipe/gal_all2 \
            --id visit=$R8764 \
            --clobber-config -C galaxy_all_8764_HSC-R.config \
            --queue small --job galA2_add_R --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:42; 
        * Start: 12/23/08:30; Finished: 10/25/10:11  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /data3a/work/song/synpipe/gal_all2 41040 40
            ```
            - Looks Ok: `gal_all2-41040-40.png`

    - `HSC-I`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /data3a/work/song/synpipe/gal_all2 \
            --id visit=$I8764 \
            --clobber-config -C galaxy_all_8764_HSC-I.config \
            --queue small --job galA2_add_I --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:42; 
        * Start: 12/23/08:47; Finished: 10/25/11:40  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /data3a/work/song/synpipe/gal_all2 14168 40
            ```
            - Looks Ok: `gal_all2-14168-40.png`

    - `HSC-Z`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /data3a/work/song/synpipe/gal_all2 \
            --id visit=$Z8764 \
            --clobber-config -C galaxy_all_8764_HSC-Z.config \
            --queue small --job galA2_add_Z --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:38; 
        * Start: 12/23/09:05; Finished: 10/25/11:40  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /data3a/work/song/synpipe/gal_all2 15146 40
            ```
            - Looks Ok: `gal_all2-15146-40.png`

    - `HSC-Y`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /data3a/work/song/synpipe/gal_all2 \
            --id visit=$Y8764 \
            --clobber-config -C galaxy_all_8764_HSC-Y.config \
            --queue small --job galA2_add_Y --nodes 9 --procs 12
        ```
        * Submit: 12/23/06:39; 
        * Start: 12/23/10:11; Finished: 10/25/12:16  
        * Visual check: 
            ```
            compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /data3a/work/song/synpipe/gal_all2 16102 40
            ```
            - Looks Ok: `gal_all2-16102-40.png`

----

## Stack the Single Visits into Coadd Images 

### Point Sources in Tract=9699 

#### Stack.py 

* Commands: 
    - `HSC-G`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star1 \
            --job stack_star1_HSC-G --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-G \
            --selectId visit=$G9699
        ```
        * Submit: 10/25/19:58
        * Start: 10/25/19:59; Finished: 10/25/20:07  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
                9699 4,4 --filter HSC-G 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 4,4 HSC-G
            ```
            - File: `star1-9699-4,4-HSC-G.png`

    - `HSC-R`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star1 \
            --job stack_star1_HSC-R --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-R \
            --selectId visit=$R9699
        ```
        * Submit: 10/25/20:07
        * Start: 10/26/02:54; Finished: 10/26/03:02  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
                9699 4,4 --filter HSC-R 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 4,4 HSC-R
            ```
            - File: `star1-9699-4,4-HSC-R.png`

    - `HSC-I`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star1 \
            --job stack_star1_HSC-I --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-I \
            --selectId visit=$I9699
        ```
        * Submit: 10/25/21:33
        * Start: 10/26/04:17; Finished: 10/26/04:28  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
                9699 4,4 --filter HSC-I 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 4,4 HSC-I
            ```
            - File: `star1-9699-4,4-HSC-I.png`

    - `HSC-Z`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star1 \
            --job stack_star1_HSC-Z --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-Z \
            --selectId visit=$Z9699
        ```
        * Submit: 10/25/21:34
        * Start: 10/26/04:28; Finished: 10/26/04:40  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
                9699 4,4 --filter HSC-Z 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 4,4 HSC-Z
            ```
            - File: `star1-9699-4,4-HSC-Z.png`

    - `HSC-Y`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star1 \
            --job stack_star1_HSC-Y --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-Y \
            --selectId visit=$Y9699
        ```
        * Submit: 10/25/21:34
        * Start: 10/26/04:40; Finished: 10/26/04:49  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
                9699 4,4 --filter HSC-Y 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 4,4 HSC-Y
            ```
            - File: `star1-9699-4,4-HSC-Y.png`

### Point Sources in Tract=8764 

#### Stack.py 

* Commands: 
    - `HSC-G`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star2 \
            --job stack_star2_HSC-G --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-G \
            --selectId visit=$G8764
        ```
        * Submit: 10/25/21:43
        * Start: 10/26/04:49; Finished: 10/26/04:57  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
                8764 4,4 --filter HSC-G 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 4,4 HSC-G
            ```
            - File: `star2-8764-4,4-HSC-G.png`

    - `HSC-R`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star2 \
            --job stack_star2_HSC-R --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-R \
            --selectId visit=$R8764
        ```
        * Submit: 10/25/21:46
        * Start: 10/26/04:57; Finished: 10/26/05:04  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
                8764 4,4 --filter HSC-R 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 4,4 HSC-R
            ```
            - File: `star2-8764-4,4-HSC-R.png`

    - `HSC-I`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star2 \
            --job stack_star2_HSC-I --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-I \
            --selectId visit=$I8764
        ```
        * Submit: 10/25/21:47
        * Start: 10/26/05:04; Finished: 10/26/05:16  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
                8764 4,4 --filter HSC-I 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 4,4 HSC-I
            ```
            - File: `star2-8764-4,4-HSC-I.png`

    - `HSC-Z`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star2 \
            --job stack_star2_HSC-Z --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-Z \
            --selectId visit=$Z8764
        ```
        * Submit: 10/25/21:48
        * Start: 10/26/05:16; Finished: 10/26/05:25  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
                8764 4,4 --filter HSC-Z 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 4,4 HSC-Z
            ```
            - File: `star2-8764-4,4-HSC-Z.png`

    - `HSC-Y`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star2 \
            --job stack_star2_HSC-Y --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-Y \
            --selectId visit=$Y8764
        ```
        * Submit: 10/25/21:50
        * Start: 10/26/05:25; Finished: 10/26/05:35  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
                8764 4,4 --filter HSC-Y 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 4,4 HSC-Y
            ```
            - File: `star2-8764-4,4-HSC-Y.png`

### Ji-Jia's QSO Test 

#### Stack.py 

* Commands: 
    - `HSC-G`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/qso \
            --job stack_qso_HSC-G --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9693 filter=HSC-G \
            --selectId visit=$G9693
        ```
        * Submit: 10/26/07:45
        * Start: 10/26/11:45; Finished: 10/26/11:54  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
                9693 4,4 --filter HSC-G 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 4,4 HSC-G
            ```
            - File: `qso-9693-4,4-HSC-G.png`

    - `HSC-R`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/qso \
            --job stack_qso_HSC-R --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9693 filter=HSC-R \
            --selectId visit=$R9693
        ```
        * Submit: 10/26/07:47
        * Start: 10/26/11:54; Finished: 10/26/12:02  
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
                9693 4,4 --filter HSC-R 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 4,4 HSC-R
            ```
            - File: `qso-9693-4,4-HSC-R.png`

    - `HSC-I`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/qso \
            --job stack_qso_HSC-I --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9693 filter=HSC-I \
            --selectId visit=$I9693
        ```
        * Submit: 10/26/07:47
        * Start: 10/26/12:02; Finished: 10/26/12:20 
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
                9693 4,4 --filter HSC-I 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 4,4 HSC-I
            ```
            - File: `qso-9693-4,4-HSC-I.png`

    - `HSC-Z`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/qso \
            --job stack_qso_HSC-Z --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9693 filter=HSC-Z \
            --selectId visit=$Z9693
        ```
        * Submit: 10/26/04:01
        * Start: 10/26/16:24; Finished: 10/26/16:37 
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
                9693 4,4 --filter HSC-Z 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 4,4 HSC-Z
            ```
            - File: `qso-9693-4,4-HSC-Z.png`

    - `HSC-Y`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/qso \
            --job stack_qso_HSC-Y --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9693 filter=HSC-Y \
            --selectId visit=$Y9693
        ```
        * Submit: 10/26/07:48
        * Start: 10/26/12:02; Finished: 10/26/12:18 
        * Visual check:
            ```
            showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso \
                9693 4,4 --filter HSC-Y 
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 4,4 HSC-Y
            ```
            - File: `qso-9693-4,4-HSC-Y.png`


### Galaxies in Tract=9699 (Full magnitude and Sersic index range) 

#### Stack.py 

* Commands: 

    - `HSC-G`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all1 \
            --job galA1_stack-G --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-G \
            --selectId visit=$G9699
        ```
        * Submit: 12/23/16:54
        * Start: 12/23/16:58; Finished: 12/23/17:20  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 4,4 HSC-G
            ```
            - File: `gal_all1-9699-4,4-HSC-G.png`

    - `HSC-R`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all1 \
            --job galA1_stack-R --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-R \
            --selectId visit=$R9699
        ```
        * Submit: 12/23/17:00
        * Start: 12/23/17:00; Finished: 12/23/17:25  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 4,4 HSC-R
            ```
            - File: `gal_all1-9699-4,4-HSC-R.png`

    - `HSC-I`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all1 \
            --job galA1_stack-I --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-I \
            --selectId visit=$I9699
        ```
        * Submit: 12/23/17:01
        * Start: 12/23/17:01; Finished: 12/23/17:40  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 4,4 HSC-I
            ```
            - File: `gal_all1-9699-4,4-HSC-I.png`

    - `HSC-Z`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all1 \
            --job galA1_stack-Z --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-Z \
            --selectId visit=$Z9699
        ```
        * Submit: 12/23/17:02
        * Start: 12/23/17:20; Finished: 12/23/17:46  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 4,4 HSC-Z
            ```
            - File: `gal_all1-9699-4,4-HSC-Z.png`

    - `HSC-Y`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all1 \
            --job galA1_stack-Y --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=9699 filter=HSC-Y \
            --selectId visit=$Y9699
        ```
        * Submit: 12/23/17:03
        * Start: 12/23/17:25; Finished: 12/23/17:45  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 4,4 HSC-Y
            ```
            - File: `gal_all1-9699-4,4-HSC-Y.png`


### Galaxies in Tract=8764 (Full magnitude and Sersic index range) 

#### Stack.py 

* Commands: 

    - `HSC-G`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all2 \
            --job galA2_stack-G --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-G \
            --selectId visit=$G8764
        ```
        * Submit: 12/23/17:14
        * Start: 12/24/11:06; Finished: 12/24/01:17  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 4,4 HSC-G
            ```
            - File: `gal_all2-8764-4,4-HSC-G.png`

    - `HSC-R`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all2 \
            --job galA2_stack-R --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-R \
            --selectId visit=$R8764
        ```
        * Submit: 12/23/17:14
        * Start: 12/24/01:13; Finished: 12/24/01:41  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 4,4 HSC-R
            ```
            - File: `gal_all2-8764-4,4-HSC-R.png`

    - `HSC-I`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all2 \
            --job galA2_stack-I --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-I \
            --selectId visit=$I8764
        ```
        * Submit: 12/23/17:15
        * Start: 12/24/01:14; Finished: 12/24/01:56  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 4,4 HSC-I
            ```
            - File: `gal_all2-8764-4,4-HSC-I.png`

    - `HSC-Z`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all2 \
            --job galA2_stack-Z --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-Z \
            --selectId visit=$Z8764
        ```
        * Submit: 12/23/17:15
        * Start: 12/24/01:17; Finished: 12/24/01:57  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 4,4 HSC-Z
            ```
            - File: `gal_all2-8764-4,4-HSC-Z.png`

    - `HSC-Y`: 
        ```
        stack.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all2 \
            --job galA2_stack-Y --queue small --nodes 9 --procs 12 \
            --batch-type=pbs --mpiexec='-bind-to socket' \
            --clobber-config \
            --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
            --id tract=8764 filter=HSC-Y \
            --selectId visit=$Y8764
        ```
        * Submit: 12/23/17:15
        * Start: 12/24/01:41; Finished: 12/24/02:02  
        * Visual check:
            ```
            compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
                /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 4,4 HSC-Y
            ```
            - File: `gal_all2-8764-4,4-HSC-Y.png`

-----

## Photometric Measurement using Multiband.py

### Configuration Files:

* `multi.config`: Without using pixel weights
    ``` python 
    root.measureCoaddSources.propagateFlags.flags={}
    root.clobberMergedDetections = True
    root.clobberMeasurements = True
    root.clobberMergedMeasurements = True
    root.clobberForcedPhotometry = True
    ```

* `multi_pix.config`: 
    ```
    root.measureCoaddSources.propagateFlags.flags={}
    root.clobberMergedDetections = True
    root.clobberMeasurements = True
    root.clobberMergedMeasurements = True
    root.clobberForcedPhotometry = True
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.forcedPhotCoadd.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].exp.usePixelWeights = True
    root.measureCoaddSources.measurement.algorithms["cmodel"].dev.usePixelWeights = True
    ```

### Point Sources in Tract=9699 

#### Multiband.py 

* Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star1 \
        --id tract=9699 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=star1_multi --clobber-config -C multi.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000 
    ```
    * Submit: 10/26:13:34
    * Start: 10/26/13:34; Finished: 10/26/16:24 


### Point Sources in Tract=8764 

#### Multiband.py 

* Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/star2 \
        --id tract=8764 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=star2_multi --clobber-config -C multi.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000 
    ```
    * Submit: 10/26:13:34
    * Start: 10/26/13:34; Finished: 10/26/18:20 


### Ji-Jia's QSO Tests Tract=9693

#### Multiband.py 

* Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/qso \
        --id tract=9693 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=qso_multi --clobber-config -C multi.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000 
    ```
    * Submit: 10/26/20:58
    * Start: 10/27/05:02; Finished: 10/27/10:13 


### Galaxies in Tract=9699 (Full magnitude and Sersic index range) 

#### Multiband.py using `multi.config` 

* Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all1 \
        --id tract=9699 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=galA1_multi --clobber-config -C multi.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000 
    ```
    * Submit: 12/23:17:53
    * Start: 10/26/20:31; Finished: 10/26/00:54 

#### Afterburner.py

* Need to copy the original schema files to the reruns for fakes

* Command: 
    ```
    afterburner.py /lustre/Subaru/SSP --rerun song/fake/synpipe/gal_all1 \
        --id tract=9699 filter=HSC-G^HSC-R^HSC-I^HSC-Z^HSC-Y \
        --doraise -j 12 --logdest galA1_afterburner.log -t 999999999999
    ```
    * Submit: 01/23:16:36
    * Start: 01/23/16:36; Finished: 10/26/16:24 


#### Multiband.py using `multi_pix.config` 

* Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all1 \
        --id tract=9699 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=galA1_multipix --clobber-config -C multi_pix.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000 
    ```
    * Submit: 12/24:02:32
    * Start: 12/24/02:36; Finished: 10/26/07:42 


### Galaxies in Tract=8764 (Full magnitude and Sersic index range) 

#### Multiband.py using `multi.config` 

* Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all2 \
        --id tract=8764 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=galA2_multi --clobber-config -C multi.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000 
    ```
    * Submit: 12/24:02:10
    * Start: 12/24/02:10; Finished: 10/26/05:33 

#### Multiband.py using `multi_pix.config` 

* Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/synpipe/gal_all2 \
        --id tract=8764 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=galA2_multipix --clobber-config -C multi_pix.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000 
    ```
    * Submit: 12/24:09:42
    * Start: 12/24/02:10; Finished: 10/26/05:33 

#### Afterburner.py

* Need to copy the original schema files to the reruns for fakes

* Command: 
    ```
    afterburner.py /lustre/Subaru/SSP --rerun song/fake/synpipe/gal_all2 \
        --id tract=8764 filter=HSC-G^HSC-R^HSC-I^HSC-Z^HSC-Y \
        --doraise -j 12 --logdest galA2_afterburner.log -t 999999999999
    ```
    * Submit: 01/23:16:36
    * Start: 01/23/16:36; Finished: 10/26/16:24 


-----

## Match the Output Catalogs

### Point Sources in Tract=9699 

#### Rerun with Fake Objects 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-G -c star_9699_HSC-G.fits \
            -o star1_HSC-G_syn -w -t 2.0 -j 6 --ra RA --dec DEC 
        ```
        - File: `star1_HSC-G_syn.fits`
        - Visual check: Ok

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-R -c star_9699_HSC-R.fits \
            -o star1_HSC-R_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-R_syn.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-I -c star_9699_HSC-I.fits \
            -o star1_HSC-I_syn -w -t 2.0 -j 6 --ra RA --dec DEC 
        ```
        - File: `star1_HSC-I_syn.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-Z -c star_9699_HSC-Z.fits \
            -o star1_HSC-Z_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-Z_syn.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-Y -c star_9699_HSC-Y.fits \
            -o star1_HSC-Y_syn -w -t 2.0 -j 6 --ra RA --dec Dec
        ```
        - File: `star1_HSC-Y_syn.fits`

#### Match with original rerun 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-G -c star_9699_HSC-G.fits \
            -o star1_HSC-G_ori -w -t 2.5 -j 6 --ra RA --dec DEC 
        ```
        - File: `star1_HSC-G_ori.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-R -c star_9699_HSC-R.fits \
            -o star1_HSC-R_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-R_ori.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-I -c star_9699_HSC-I.fits \
            -o star1_HSC-I_ori -w -t 2.5 -j 6 --ra RA --dec DEC 
        ```
        - File: `star1_HSC-I_ori.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-Z -c star_9699_HSC-Z.fits \
            -o star1_HSC-Z_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-Z_ori.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-Y -c star_9699_HSC-Y.fits \
            -o star1_HSC-Y_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-Y_ori.fits`


### Point Sources in Tract=8764 

#### Rerun with Fake Objects 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-G -c star_8764_HSC-G.fits \
            -o star2_HSC-G_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-G_syn.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-R -c star_8764_HSC-R.fits \
            -o star2_HSC-R_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-R_syn.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-I -c star_8764_HSC-I.fits \
            -o star2_HSC-I_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-I_syn.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-Z -c star_8764_HSC-Z.fits \
            -o star2_HSC-Z_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-Z_syn.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-Y -c star_8764_HSC-Y.fits \
            -o star2_HSC-Y_syn -w -t 2.0 -j 6 --ra RA --dec Dec
        ```
        - File: `star2_HSC-Y_syn.fits`

#### Match with original rerun 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-G -c star_8764_HSC-G.fits \
            -o star2_HSC-G_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-G_ori.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-R -c star_8764_HSC-R.fits \
            -o star2_HSC-R_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-R_ori.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-I -c star_8764_HSC-I.fits \
            -o star2_HSC-I_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-I_ori.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-Z -c star_8764_HSC-Z.fits \
            -o star2_HSC-Z_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-Z_ori.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-Y -c star_8764_HSC-Y.fits \
            -o star2_HSC-Y_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-Y_ori.fits`


### Ji-Jia's QSOs in Tract=9693 

#### Rerun with Fake Objects 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 \
            -f HSC-G -c jijia_qso_HSC-G.fits \
            -o qso_HSC-G_syn -w -t 2.0 -j 6 --ra RA --dec DEC 
        ```
        - File: `qso_HSC-G_syn.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 \
            -f HSC-R -c jijia_qso_HSC-R.fits \
            -o qso_HSC-R_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `qso_HSC-R_syn.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 \
            -f HSC-I -c jijia_qso_HSC-I.fits \
            -o qso_HSC-I_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `qso_HSC-I_syn.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 \
            -f HSC-Z -c jijia_qso_HSC-Z.fits \
            -o qso_HSC-Z_syn -w -t 2.0 -j 10 --ra RA --dec Dec 
        ```
        - File: `qso_HSC-Z_syn.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/qso 9693 \
            -f HSC-Y -c jijia_qso_HSC-Y.fits \
            -o qso_HSC-Y_syn -w -t 2.0 -j 10 --ra RA --dec Dec 
        ```
        - File: `qso_HSC-Y_syn.fits`

#### Match with original rerun 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9693 \
            -f HSC-G -c jijia_qso_HSC-G.fits \
            -o qso_HSC-G_ori -w -t 2.5 -j 10 --ra RA --dec DEC 
        ```
        - File: `qso_HSC-G_ori.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9693 \
            -f HSC-R -c jijia_qso_HSC-R.fits \
            -o qso_HSC-R_ori -w -t 2.5 -j 10 --ra RA --dec Dec 
        ```
        - File: `qso_HSC-R_ori.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9693 \
            -f HSC-I -c jijia_qso_HSC-I.fits \
            -o qso_HSC-I_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `qso_HSC-I_ori.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9693 \
            -f HSC-Z -c jijia_qso_HSC-Z.fits \
            -o qso_HSC-Z_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `qso_HSC-Z_ori.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9693 \
            -f HSC-Y -c jijia_qso_HSC-Y.fits \
            -o qso_HSC-Y_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `qso_HSC-Y_ori.fits`

### Fake Galaxies Tract=9699 (Full magnitude and Sersic index range)

#### Rerun with Fake Objects 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-G -c galaxy_all_9699_HSC-G.fits \
            -o gal_all1_HSC-G_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-G_syn.fits`
        - Visual check: Ok

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-R -c galaxy_all_9699_HSC-R.fits \
            -o gal_all1_HSC-R_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-R_syn.fits`
        - Visual check: Ok

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-I -c galaxy_all_9699_HSC-I.fits \
            -o gal_all1_HSC-I_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-I_syn.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-Z -c galaxy_all_9699_HSC-Z.fits \
            -o gal_all1_HSC-Z_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-Z_syn.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-Y -c galaxy_all_9699_HSC-Y.fits \
            -o gal_all1_HSC-Y_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-Y_syn.fits`

#### Rerun with Fake Objects (multipix run) 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-G -c galaxy_all_9699_HSC-G.fits \
            -o gal_all1_HSC-G_syn_multipix -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-G_syn_multipix.fits`
        - Visual check: Ok

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-R -c galaxy_all_9699_HSC-R.fits \
            -o gal_all1_HSC-R_syn_multipix -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-R_syn_multipix.fits`
        - Visual check: Ok

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-I -c galaxy_all_9699_HSC-I.fits \
            -o gal_all1_HSC-I_syn_multipix -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-I_syn_multipix.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-Z -c galaxy_all_9699_HSC-Z.fits \
            -o gal_all1_HSC-Z_syn_multipix -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-Z_syn_multipix.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all1 9699 \
            -f HSC-Y -c galaxy_all_9699_HSC-Y.fits \
            -o gal_all1_HSC-Y_syn_multipix -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-Y_syn_multipix.fits`

#### Match with original rerun 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-G -c galaxy_all_9699_HSC-G.fits \
            -o gal_all1_HSC-G_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-G_ori.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-R -c galaxy_all_9699_HSC-R.fits \
            -o gal_all1_HSC-R_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-R_ori.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-I -c galaxy_all_9699_HSC-I.fits \
            -o gal_all1_HSC-I_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-I_ori.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-Z -c galaxy_all_9699_HSC-Z.fits \
            -o gal_all1_HSC-Z_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-Z_ori.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-Y -c galaxy_all_9699_HSC-Y.fits \
            -o gal_all1_HSC-Y_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all1_HSC-Y_ori.fits`

### Fake Galaxies Tract=8764 (Full magnitude and Sersic index range)

#### Rerun with Fake Objects 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 \
            -f HSC-G -c galaxy_all_8764_HSC-G.fits \
            -o gal_all2_HSC-G_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-G_syn.fits`
        - Visual check: Ok

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 \
            -f HSC-R -c galaxy_all_8764_HSC-R.fits \
            -o gal_all2_HSC-R_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-R_syn.fits`
        - Visual check: Ok

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 \
            -f HSC-I -c galaxy_all_8764_HSC-I.fits \
            -o gal_all2_HSC-I_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-I_syn.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 \
            -f HSC-Z -c galaxy_all_8764_HSC-Z.fits \
            -o gal_all2_HSC-Z_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-Z_syn.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/gal_all2 8764 \
            -f HSC-Y -c galaxy_all_8764_HSC-Y.fits \
            -o gal_all2_HSC-Y_syn -w -t 2.0 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-Y_syn.fits`

#### Match with original rerun 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-G -c galaxy_all_8764_HSC-G.fits \
            -o gal_all2_HSC-G_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-G_ori.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-R -c galaxy_all_8764_HSC-R.fits \
            -o gal_all2_HSC-R_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-R_ori.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-I -c galaxy_all_8764_HSC-I.fits \
            -o gal_all2_HSC-I_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-I_ori.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-Z -c galaxy_all_8764_HSC-Z.fits \
            -o gal_all2_HSC-Z_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-Z_ori.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-Y -c galaxy_all_8764_HSC-Y.fits \
            -o gal_all2_HSC-Y_ori -w -t 2.5 -j 6 --ra RA --dec Dec 
        ```
        - File: `gal_all2_HSC-Y_ori.fits`



-----
