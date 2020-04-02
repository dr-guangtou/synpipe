# More SynPipe Photometric Tests 

---- 

* by Song  Huang (UCSC)

----

## Tests 

* New tests of stellar objects using more complete catalog from COSMOS 

* Tests of fake galaxies around clusters for I-Non

----

## Preparation

### Data Storage

* The metadata and results are kept on Master@IPMU, under Song Huang's working directory:
    ```
    /lustre/Subaru/SSP/rerun/song/fake/synpipe
    ```

### Tract Selection: 

* New Tract=`9799` for I-Non's cluster test

* Useful files, under `/lustre/Subaru/SSP/rerun/song/fake/synpipe/mask/`:
    ```
    dr1_s16a_9799_HSC-I_shape_all.wkb 
    ```

### Regions with Problematic Data: 

* Useful files, under `/lustre/Subaru/SSP/rerun/song/fake/synpipe/mask/`
    ```
    dr1_s16a_9799_nodata_all.wkb 
    ``` 

--- 

### List of Visits that belong to each Tract: 

* Find all the Visits that are used to generate the coadd images in the Tract.  

* Using script within SynPipe. Example command: 
    ```
    tractFindVisits.py s15b_wide 9799 --filter='HSC-G' --dataDir='/lustre2/HSC_DR/dr1/s15b/data/'
    ```

---- 

# New commands : 17/04/30


#### Generate Input Catalogs for Tract=9699

* Command: 
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=9699 filter='HSC-I' patch='4,4' \
        -c inputCat='cosmos_star_xd_2.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=1500 \
        rejMask='dr1_s16a_9699_nodata_all.wkb' \
        acpMask='dr1_s16a_9699_HSC-I_shape_all.wkb'
    ```

#### Generate Input Catalogs for Tract=8764

* Command: 
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=8764 filter='HSC-I' patch='4,4' \
        -c inputCat='cosmos_star_xd_2.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=1500 \
        rejMask='dr1_s16a_8764_nodata_all.wkb' \
        acpMask='dr1_s16a_8764_HSC-I_shape_all.wkb'
    ```

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

    - `HSC-R`:
        ``
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$R9699 \
            --clobber-config -C star_9699_HSC-R.config \
            --queue small --job star_add_R --nodes 9 --procs 12
        ```

    - `HSC-I`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$I9699 \
            --clobber-config -C star_9699_HSC-I.config \
            --queue small --job star_add_I --nodes 9 --procs 12
        ```

    - `HSC-Z`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$Z9699 \
            --clobber-config -C star_9699_HSC-Z.config \
            --queue small --job star_add_Z --nodes 9 --procs 12
        ```

    - `HSC-Y`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 \
            --id visit=$Y9699 \
            --clobber-config -C star_9699_HSC-Y.config \
            --queue small --job star_add_Y --nodes 9 --procs 12
        ```


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

    - `HSC-R`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$R8764 \
            --clobber-config -C star_8764_HSC-R.config \
            --queue small --job star2_add_R --nodes 9 --procs 12
        ```
    
    - `HSC-I`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$I8764 \
            --clobber-config -C star_8764_HSC-I.config \
            --queue small --job star2_add_I --nodes 9 --procs 12
        ```

    - `HSC-Z`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$Z8764 \
            --clobber-config -C star_8764_HSC-Z.config \
            --queue small --job star2_add_Z --nodes 9 --procs 12
        ```

    - `HSC-Y`:
        ```
        runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
            --output /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 \
            --id visit=$Y8764 \
            --clobber-config -C star_8764_HSC-Y.config \
            --queue small --job star2_add_Y --nodes 9 --procs 12
        ```


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

-----

## Match the Output Catalogs

### Point Sources in Tract=9699 

#### Rerun with Fake Objects 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-G -c star_9699_HSC-G.fits \
            -o star1_HSC-G_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-G_syn.fits`
        - Visual check: Ok

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-R -c star_9699_HSC-R.fits \
            -o star1_HSC-R_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-R_syn.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-I -c star_9699_HSC-I.fits \
            -o star1_HSC-I_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-I_syn.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-Z -c star_9699_HSC-Z.fits \
            -o star1_HSC-Z_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-Z_syn.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star1 9699 \
            -f HSC-Y -c star_9699_HSC-Y.fits \
            -o star1_HSC-Y_syn -w -t 2.0 -j 8 --ra RA --dec Dec
        ```
        - File: `star1_HSC-Y_syn.fits`

#### Match with original rerun 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-G -c star_9699_HSC-G.fits \
            -o star1_HSC-G_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-G_ori.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-R -c star_9699_HSC-R.fits \
            -o star1_HSC-R_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-R_ori.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-I -c star_9699_HSC-I.fits \
            -o star1_HSC-I_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-I_ori.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-Z -c star_9699_HSC-Z.fits \
            -o star1_HSC-Z_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-Z_ori.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 9699 \
            -f HSC-Y -c star_9699_HSC-Y.fits \
            -o star1_HSC-Y_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star1_HSC-Y_ori.fits`


### Point Sources in Tract=8764 

#### Rerun with Fake Objects 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-G -c star_8764_HSC-G.fits \
            -o star2_HSC-G_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-G_syn.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-R -c star_8764_HSC-R.fits \
            -o star2_HSC-R_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-R_syn.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-I -c star_8764_HSC-I.fits \
            -o star2_HSC-I_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-I_syn.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-Z -c star_8764_HSC-Z.fits \
            -o star2_HSC-Z_syn -w -t 2.0 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-Z_syn.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/synpipe/star2 8764 \
            -f HSC-Y -c star_8764_HSC-Y.fits \
            -o star2_HSC-Y_syn -w -t 2.0 -j 8 --ra RA --dec Dec
        ```
        - File: `star2_HSC-Y_syn.fits`

#### Match with original rerun 

* Commands: 
    -`HSC-G`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-G -c star_8764_HSC-G.fits \
            -o star2_HSC-G_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-G_ori.fits`

    -`HSC-R`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-R -c star_8764_HSC-R.fits \
            -o star2_HSC-R_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-R_ori.fits`

    -`HSC-I`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-I -c star_8764_HSC-I.fits \
            -o star2_HSC-I_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-I_ori.fits`

    -`HSC-Z`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-Z -c star_8764_HSC-Z.fits \
            -o star2_HSC-Z_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-Z_ori.fits`

    -`HSC-Y`:
        ``` bash
        runMatchFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8764 \
            -f HSC-Y -c star_8764_HSC-Y.fits \
            -o star2_HSC-Y_ori -w -t 2.5 -j 8 --ra RA --dec Dec 
        ```
        - File: `star2_HSC-Y_ori.fits`



