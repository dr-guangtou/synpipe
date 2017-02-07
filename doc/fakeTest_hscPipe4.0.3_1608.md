# Fake Object Pipeline Test usng S15B and hscPipe 4.0.3 

---- 
* Song Huang 2016/08


## Find all the Visits for Tract=8766 

### HSC-I: 

* Command: 
    ```
    tractFindVisits.py s15b_wide 8766 --filter='HSC-I' --dataDir='/lustre2/HSC_DR/dr1/s15b/data/'
    ```

* Output: 
    ```
    # Input visits for Tract=8766 Filter=HSC-I
        # Input CCDs includes 37 Visits
7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484
    ```

### HSC-G: 

* Command: 
    ```
    tractFindVisits.py s15b_wide 8766 --filter='HSC-G' --dataDir='/lustre2/HSC_DR/dr1/s15b/data/'
    ```

* Output: 
    ```
    # Input visits for Tract=8766 Filter=HSC-G
        # Input CCDs includes 37 Visits
9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536 
    ```

### HSC-R: 

* Command: 
    ```
    tractFindVisits.py s15b_wide 8766 --filter='HSC-R' --dataDir='/lustre2/HSC_DR/dr1/s15b/data/'
    ```

* Output: 
    ```
    # Input visits for Tract=8766 Filter=HSC-R
        # Input CCDs includes 25 Visits
11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144 
    ```

### HSC-Z: 

* Command: 
    ```
    tractFindVisits.py s15b_wide 8766 --filter='HSC-Z' --dataDir='/lustre2/HSC_DR/dr1/s15b/data/'
    ```

* Output: 
    ```
    # Input visits for Tract=8766 Filter=HSC-Z
        # Input CCDs includes 37 Visits
9696^9700^9708^9712^9718^9724^9726^9730^9732^9736^9738^9742^9744^9748^9750^9752^9760^9762^9772^9774^9780^9782^9784^13288^15098^17672^17676^17680^17692^17694^17722^17724^17736^17738^17740^17750^17752
    ```

### HSC-Y: 

* Command: 
    ```
    tractFindVisits.py s15b_wide 8766 --filter='HSC-Y' --dataDir='/lustre2/HSC_DR/dr1/s15b/data/'
    ```

* Output: 
    ```
    # Input visits for Tract=8766 Filter=HSC-Y
        # Input CCDs includes 25 Visits
6462^6466^6470^6478^6482^6488^6490^6496^6498^6512^6522^6524^6528^6530^6536^6538^6542^6544^6546^6564^6566^13152^13154^13198^13254 
    ```

### Show Visits: 

* Commands: 
    ```
    showTractVisit.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8766 7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484 -p 

    showTractVisit.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8766 9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536 -p

    showTractVisit.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8766 11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144 -p

    showTractVisit.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8766 9696^9700^9708^9712^9718^9724^9726^9730^9732^9736^9738^9742^9744^9748^9750^9752^9760^9762^9772^9774^9780^9782^9784^13288^15098^17672^17676^17680^17692^17694^17722^17724^17736^17738^17740^17750^17752 -p

    showTractVisit.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide 8766 6462^6466^6470^6478^6482^6488^6490^6496^6498^6512^6522^6524^6528^6530^6536^6538^6542^6544^6546^6564^6566^13152^13154^13198^13254 -p 
    ```

* Outputs: 
    
    ```
    dr1_8766_patches_HSC-I.png
    dr1_8766_patches_HSC-G.png
    dr1_8766_patches_HSC-R.png
    dr1_8766_patches_HSC-Z.png
    dr1_8766_patches_HSC-Y.png
    ```

--- 

## Make Catalogs of Random Fake Galaxies:

* The parent samples are drawn from `cosmos_mag25.2_shuang.fits`, and only include the 
    ones with magnitude brighter than 23.0 magnitude. 

### High-Sersic Index Sample:

* `sersic_n >= 2.5 && sersic_n <= 5.5 && b_a >= 0.25`
    - Saved as `cosmos_mag23.0_shuang_highn.fits`
* Create the multiband version of the catalog
    - Saved as `cosmos_mag23.0_shuang_highn_multi.fits`

* Command:
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=8766 filter='HSC-I' patch='4,4' \
        -c inputCat='cosmos_mag23.0_shuang_highn_multi.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=500 \
        rejMask='dr1_wide_8766_HSC-I_nodata_all.wkb' \
        acpMask='dr1_wide_HSC-I_tract_8766.wkb'
    ```

* Outputs: 

    ```
    src_8766_radec_G/R/I/Z/Y_highn.fits 
    ```

### Low-Sersic Index Sample:

* `sersic_n >= 0.5 && sersic_n <= 2.5`
    - Saved as `cosmos_mag23.0_shuang_lown.fits`
* Create the multiband version of the catalog
    - Saved as `cosmos_mag23.0_shuang_lown_multi.fits`

* Command:
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=8766 filter='HSC-I' patch='4,4' \
        -c inputCat='cosmos_mag23.0_shuang_lown_multi.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=500 \
        rejMask='dr1_wide_8766_HSC-I_nodata_all.wkb' \
        acpMask='dr1_wide_HSC-I_tract_8766.wkb'
    ```

* Outputs:
    ```
    src_8766_radec_G/R/I/Z/Y_lown.fits 
    ```

--- 

## Add Fake Galaxies to Single Visits

### High-Sersic 

#### HSC-I

* Config file: `dr1_8766_HSC-I_highn.config`
    ```
    from fakes import positionGalSimFakes
    root.fakes.retarget(positionGalSimFakes.PositionGalSimFakesTask)
    root.fakes.galList = 'src_8766_radec_I_highn.fits'
    root.fakes.galType = 'sersic'
    root.fakes.maxMargin = 200
    root.fakes.addShear = False
    ```

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_highn/ \
        --id visit="7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484" \
        --clobber-config -C dr1_8766_HSC-I_highn.config \
        --queue small --job add_i_high --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_highn 7300 40
    ```
        - See: `8766_highn-7300-40.png`

#### HSC-G

* Config file: `dr1_8766_HSC-G_highn.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_highn/ \
        --id visit="9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536" \
        --clobber-config -C dr1_8766_HSC-G_highn.config \
        --queue small --job add_g_high --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_highn 9852 50
    ```
        - See: `8766_highn-9852-50.png`

#### HSC-R

* Config file: `dr1_8766_HSC-R_highn.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_highn/ \
        --id visit="11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144" \
        --clobber-config -C dr1_8766_HSC-R_highn.config \
        --queue small --job add_r_high --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_highn 11442 50
    ```
        - See: `8766_highn-11442-50.png`

#### HSC-Z

* Config file: `dr1_8766_HSC-Z_highn.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_highn/ \
        --id visit="9696^9700^9708^9712^9718^9724^9726^9730^9732^9736^9738^9742^9744^9748^9750^9752^9760^9762^9772^9774^9780^9782^9784^13288^15098^17672^17676^17680^17692^17694^17722^17724^17736^17738^17740^17750^17752" \
        --clobber-config -C dr1_8766_HSC-Z_highn.config \
        --queue small --job add_z_high --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_highn 9708 40
    ```
        - See: `8766_highn-9708-40.png`

#### HSC-Y

* Config file: `dr1_8766_HSC-Y_highn.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_highn/ \
        --id visit="6462^6466^6470^6478^6482^6488^6490^6496^6498^6512^6522^6524^6528^6530^6536^6538^6542^6544^6546^6564^6566^13152^13154^13198^13254" \
        --clobber-config -C dr1_8766_HSC-Y_highn.config \
        --queue small --job add_y_high --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_highn 6478 40
    ```
        - See: `8766_highn-6478-40.png`


### Low-Sersic 

#### HSC-I

* Config file: `dr1_8766_HSC-I_lown.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_lown/ \
        --id visit="7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484" \
        --clobber-config -C dr1_8766_HSC-I_lown.config \
        --queue small --job add_i_low --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_lown 7300 41
    ```
        - See: `8766_lown-7300-40.png`
    
#### HSC-G

* Config file: `dr1_8766_HSC-G_lown.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_lown/ \
        --id visit="9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536" \
        --clobber-config -C dr1_8766_HSC-G_lown.config \
        --queue small --job add_g_low --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_lown 9852 49
    ```
        - See: `8766_highn-9852-49.png`

#### HSC-R

* Config file: `dr1_8766_HSC-R_lown.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_lown/ \
        --id visit="11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144" \
        --clobber-config -C dr1_8766_HSC-R_lown.config \
        --queue small --job add_r_low --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_lown 11442 49
    ```
        - See: `8766_lown-11442-49.png`


#### HSC-Z

* Config file: `dr1_8766_HSC-Z_lown.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_lown/ \
        --id visit="9696^9700^9708^9712^9718^9724^9726^9730^9732^9736^9738^9742^9744^9748^9750^9752^9760^9762^9772^9774^9780^9782^9784^13288^15098^17672^17676^17680^17692^17694^17722^17724^17736^17738^17740^17750^17752" \
        --clobber-config -C dr1_8766_HSC-Z_lown.config \
        --queue small --job add_z_low --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_lown 9708 41
    ```
        - See: `8766_lown-9708-41.png`


#### HSC-Y

* Config file: `dr1_8766_HSC-Y_lown.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_lown/ \
        --id visit="6462^6466^6470^6478^6482^6488^6490^6496^6498^6512^6522^6524^6528^6530^6536^6538^6542^6544^6546^6564^6566^13152^13154^13198^13254" \
        --clobber-config -C dr1_8766_HSC-Y_lown.config \
        --queue small --job add_y_low --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_lown 6478 41
    ```
        - See: `8766_lown-6478-41.png

---- 

## Stacking the Single Visits into deepCoadd Images

### High Sersic Index 

#### HSC-I

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_highn \
        --job stack_i_highn --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-I \
        --selectId visit='7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484'
    ```

* Check 
    ```
    python showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 4,4 --filter HSC-I
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 4,4 HSC-I
    ```
        - See: `8766_highn-8766-4,4-HSC-I.png`

#### HSC-G

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_highn \
        --job stack_g_highn --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-G \
        --selectId visit='9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 4,4 HSC-G
    ```
        - See: `8766_highn-8766-4,4-HSC-G.png`

#### HSC-R

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_highn \
        --job stack_r_highn --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-R \
        --selectId visit='11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 4,4 HSC-R
    ```
        - See: `8766_highn-8766-4,4-HSC-R.png`

#### HSC-Z

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_highn \
        --job stack_z_highn --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-Z \
        --selectId visit='9696^9700^9708^9712^9718^9724^9726^9730^9732^9736^9738^9742^9744^9748^9750^9752^9760^9762^9772^9774^9780^9782^9784^13288^15098^17672^17676^17680^17692^17694^17722^17724^17736^17738^17740^17750^17752'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 4,4 HSC-Z
    ```
        - See: `8766_highn-8766-4,4-HSC-Z.png`


#### HSC-Y

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_highn \
        --job stack_y_highn --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-Y \
        --selectId visit='6462^6466^6470^6478^6482^6488^6490^6496^6498^6512^6522^6524^6528^6530^6536^6538^6542^6544^6546^6564^6566^13152^13154^13198^13254'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 4,4 HSC-Y
    ```
        - See: `8766_highn-8766-4,4-HSC-Y.png`


### Low Sersic Index 

#### HSC-I

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_lown \
        --job stack_i_lown --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-I \
        --selectId visit='7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484'
    ```

* Check 
    ```
    python showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 4,4 --filter HSC-I
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 4,4 HSC-I
    ```
        - See: `8766_lown-8766-4,4-HSC-I.png`

#### HSC-G

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_lown \
        --job stack_g_lown --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-G \
        --selectId visit='9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 4,4 HSC-G
    ```
        - See: `8766_lown-8766-4,4-HSC-G.png`

#### HSC-R

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_lown \
        --job stack_r_lown --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-R \
        --selectId visit='11422^11426^11430^11442^11446^11466^11468^11474^11476^11478^11496^11498^11504^11506^11508^11530^11532^11534^41064^41068^41072^41120^41122^41142^41144'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 4,4 HSC-R
    ```
        - See: `8766_lown-8766-4,4-HSC-R.png`

#### HSC-Z

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_lown \
        --job stack_z_lown --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-Z \
        --selectId visit='9696^9700^9708^9712^9718^9724^9726^9730^9732^9736^9738^9742^9744^9748^9750^9752^9760^9762^9772^9774^9780^9782^9784^13288^15098^17672^17676^17680^17692^17694^17722^17724^17736^17738^17740^17750^17752'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 4,4 HSC-Z
    ```
        - See: `8766_lown-8766-4,4-HSC-Z.png`

#### HSC-Y

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_lown \
        --job stack_y_lown --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-Y \
        --selectId visit='6462^6466^6470^6478^6482^6488^6490^6496^6498^6512^6522^6524^6528^6530^6536^6538^6542^6544^6546^6564^6566^13152^13154^13198^13254'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 4,4 HSC-Y
    ```
        - See: `8766_lown-8766-4,4-HSC-Y.png`

----- 

## Multiband Analysis 

### High Sersic Index 

* `usePixelWeights == False` Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_highn \
        --id tract=8766 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=multi_8766_highn --clobber-config -C multi.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000
    ```

* `usePixelWeights == True` Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_highn \
        --id tract=8766 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=multi_8766_highnPix --clobber-config -C multi_pix.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000
    ```

### Low Sersic Index 

* `usePixelWeights == False` Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_lown \
        --id tract=8766 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=multi_8766_lown --clobber-config -C multi.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000
    ```

* `usePixelWeights == True` Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_lown \
        --id tract=8766 filter=HSC-I^HSC-R^HSC-Z^HSC-G^HSC-Y \
        --job=multi_8766_lownPix --clobber-config -C multi_pix.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000
    ```

----- 

## Match the Output Catalogs 

### High Sersic Index - Multi 

#### HSC-I

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-I -c src_8766_radec_I_highn.fits \
        -o dr1_8766_highn_HSC-I_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-I_multi.fits`

#### HSC-G

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-G -c src_8766_radec_G_highn.fits \
        -o dr1_8766_highn_HSC-G_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-G_multi.fits`

#### HSC-R

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-R -c src_8766_radec_R_highn.fits \
        -o dr1_8766_highn_HSC-R_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-R_multi.fits`

#### HSC-Z

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-Z -c src_8766_radec_Z_highn.fits \
        -o dr1_8766_highn_HSC-Z_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-Z_multi.fits`

#### HSC-Y

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-Y -c src_8766_radec_Y_highn.fits \
        -o dr1_8766_highn_HSC-Y_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-Y_multi.fits`



### High Sersic Index - Multi_Pix 

#### HSC-I

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-I -c src_8766_radec_I_highn.fits \
        -o dr1_8766_highn_HSC-I_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-I_multi_pix.fits`

#### HSC-G

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-G -c src_8766_radec_G_highn.fits \
        -o dr1_8766_highn_HSC-G_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-G_multi_pix.fits`

#### HSC-R

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-R -c src_8766_radec_R_highn.fits \
        -o dr1_8766_highn_HSC-R_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-R_multi_pix.fits`

#### HSC-Z

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-Z -c src_8766_radec_Z_highn.fits \
        -o dr1_8766_highn_HSC-Z_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-Z_multi_pix.fits`

#### HSC-Y

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_highn 8766 \
        -f HSC-Y -c src_8766_radec_Y_highn.fits \
        -o dr1_8766_highn_HSC-Y_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_highn_HSC-Y_multi_pix.fits`



### Low Sersic Index - Multi_Pix 

#### HSC-I

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-I -c src_8766_radec_I_lown.fits \
        -o dr1_8766_lown_HSC-I_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-I_multi_pix.fits`

#### HSC-G

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-G -c src_8766_radec_G_lown.fits \
        -o dr1_8766_lown_HSC-G_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-G_multi_pix.fits`

#### HSC-R

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-R -c src_8766_radec_R_lown.fits \
        -o dr1_8766_lown_HSC-R_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-R_multi_pix.fits`

#### HSC-Z

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-Z -c src_8766_radec_Z_lown.fits \
        -o dr1_8766_lown_HSC-Z_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-Z_multi_pix.fits`

#### HSC-Y

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-Y -c src_8766_radec_Y_lown.fits \
        -o dr1_8766_lown_HSC-Y_multi_pix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-Y_multi_pix.fits`


### Low Sersic Index - Multi 

#### HSC-I

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-I -c src_8766_radec_I_lown.fits \
        -o dr1_8766_lown_HSC-I_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-I_multi.fits`

#### HSC-G

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-G -c src_8766_radec_G_lown.fits \
        -o dr1_8766_lown_HSC-G_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-G_multi.fits`

#### HSC-R

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-R -c src_8766_radec_R_lown.fits \
        -o dr1_8766_lown_HSC-R_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-R_multi.fits`

#### HSC-Z

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-Z -c src_8766_radec_Z_lown.fits \
        -o dr1_8766_lown_HSC-Z_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-Z_multi.fits`

#### HSC-Y

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_lown 8766 \
        -f HSC-Y -c src_8766_radec_Y_lown.fits \
        -o dr1_8766_lown_HSC-Y_multi \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_lown_HSC-Y_multi.fits`

---- 

## Test Afterburner 

## High Sersic Index -- Multi 

* Command: 
    ```
    afterburner.py /lustre/Subaru/SSP --rerun song/fake/8766_highn \
        --id tract=8766 filter=HSC-G^HSC-R^HSC-I^HSC-Z^HSC-Y \
        --doraise -j 12 --logdest dr1_8766_highn_afterburner.log -t 999999999999
    ```

## Low Sersic Index -- Multi 

* Command: 
    ```
    afterburner.py /lustre/Subaru/SSP --rerun song/fake/8766_lown \
        --id tract=8766 filter=HSC-G^HSC-R^HSC-I^HSC-Z^HSC-Y \
        --doraise -j 12 --logdest dr1_8766_lown_afterburner.log -t 999999999999
    ```


----

## Test for UDG (2016-08-16)

### makeSourceList.py 

* Command:
    ```
    makeSourceList.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=8766 filter='HSC-I' patch='4,4' \
        -c inputCat='fakeUDG_test1.fits' \
        innerTract=True uniqueID=True \
        rhoFakes=250 \
        rejMask='region/dr1_wide_8766_HSC-I_nodata_all.wkb' \
        acpMask='region/dr1_wide_HSC-I_tract_8766.wkb'
    ```

* Outputs: 
    ```
    src_8766_UDG_G/I.fits
    ```

### runAddFakes.py

#### HSC-I

* Config file: `dr1_8766_HSC-I_UDG.config`
    ```
    from fakes import positionGalSimFakes
    root.fakes.retarget(positionGalSimFakes.PositionGalSimFakesTask)
    root.fakes.galList = 'src_8766_UDG_I.fits'
    root.fakes.galType = 'sersic'
    root.fakes.maxMargin = 200
    root.fakes.addShear = False
    ```

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_udg/ \
        --id visit="7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484" \
        --clobber-config -C dr1_8766_HSC-I_UDG.config \
        --queue small --job add_i_udg --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_udg 7300 40
    ```
        - See: `8766_UDG-7300-40.png`

#### HSC-G

* Config file: `dr1_8766_HSC-G_UDG.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_udg/ \
        --id visit="9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536" \
        --clobber-config -C dr1_8766_HSC-G_UDG.config \
        --queue small --job add_g_udg --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_udg 9852 50
    ```
        - See: `8766_udg-9852-50.png`

### Stack.py

#### HSC-I

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_udg \
        --job stack_i_udg --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-I \
        --selectId visit='7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484'
    ```

* Check 
    ```
    python showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/8766_udg 8766 4,4 --filter HSC-I
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_udg 8766 4,4 HSC-I
    ```
        - See: `8766_udg-8766-4,4-HSC-I.png`

#### HSC-G

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_udg \
        --job stack_g_udg --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-G \
        --selectId visit='9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_udg 8766 4,4 HSC-G
    ```
        - See: `8766_udg-8766-4,4-HSC-G.png`

### multiband.py 

* `usePixelWeights == True` Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_udg \
        --id tract=8766 filter=HSC-I^HSC-G \
        --job=multi_8766_udgPix --clobber-config -C multi_pix.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000
    ```

### runMatchFakes.py 

#### HSC-I

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_udg 8766 \
        -f HSC-I -c src_8766_UDG_I.fits \
        -o dr1_8766_UDG_HSC-I_multiPix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_UDG_HSC-I_multiPix.fits`

#### HSC-G

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_udg 8766 \
        -f HSC-G -c src_8766_UDG_G.fits \
        -o dr1_8766_UDG_HSC-G_multiPix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_udg_HSC-G_multiPix.fits`


----

## Test for UDG on a sparse grid (2016-08-17)

### makeSourceList.py 

* Command:
    ```
    makeSourceListGrid.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --rerun /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --id tract=8766 filter='HSC-I' patch='4,4' \
        -c inputCat='sample/fakeUDG_test1.fits' \
        innerTract=True uniqueID=True \
        theta_grid=45 \
        rejMask='region/dr1_wide_8766_HSC-I_nodata_all.wkb' \
        acpMask='region/dr1_wide_HSC-I_tract_8766.wkb'
    ```

* Outputs: 
    ```
    src_8766_UDG_grid_45.0asec_G/I.fits
    ```

### runAddFakes.py

#### HSC-I

* Config file: `dr1_8766_HSC-I_UDG_grid.config`
    ```
    from fakes import positionGalSimFakes
    root.fakes.retarget(positionGalSimFakes.PositionGalSimFakesTask)
    root.fakes.galList = 'src_8766_UDG_grid_45.0asec_I.fits'
    root.fakes.galType = 'sersic'
    root.fakes.maxMargin = 200
    root.fakes.addShear = False
    ```

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid/ \
        --id visit="7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484" \
        --clobber-config -C dr1_8766_HSC-I_UDG_grid.config \
        --queue small --job add_i_udg_grid --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid 7300 40
    ```
        - See: `8766_udg_grid-7300-40.png`

#### HSC-G

* Config file: `dr1_8766_HSC-G_UDG_grid.config`

* Command: 
    ```
    runAddFakes.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid/ \
        --id visit="9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536" \
        --clobber-config -C dr1_8766_HSC-G_UDG_grid.config \
        --queue small --job add_g_udg_grid --nodes 9 --procs 12
    ```

* Check:
    ```
    compFakeGalaxy.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid 9852 50
    ```
        - See: `8766_udg_grid-9852-50.png`

### Stack.py

#### HSC-I

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_udg_grid \
        --job stack_i_udg_grid --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-I \
        --selectId visit='7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484'
    ```

* Check 
    ```
    python showInDs9.py /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid 8766 4,4 --filter HSC-I
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid 8766 4,4 HSC-I
    ```
        - See: `8766_udg_grid-8766-4,4-HSC-I.png`

#### HSC-G

* Command:
    ```
    stack.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_udg_grid \
        --job stack_g_udg_grid --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec='-bind-to socket' \
        --clobber-config \
        --config makeCoaddTempExp.doOverwrite=True doOverwriteCoadd=True \
        --id tract=8766 filter=HSC-G \
        --selectId visit='9840^9844^9852^9856^9862^9868^9870^9880^9882^9886^9888^9898^9900^9904^9912^9916^9918^11568^11572^11578^11582^11586^11588^11590^11596^11598^11620^11638^11640^11674^42456^42460^42464^42512^42514^42534^42536'
    ```

* Check 
    ```
    python compFakeCoadd.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide \
        /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid 8766 4,4 HSC-G
    ```
        - See: `8766_udg_grid-8766-4,4-HSC-G.png`

### multiband.py 

* `usePixelWeights == True` Command: 
    ```
    multiBand.py /lustre/Subaru/SSP/ --rerun=song/fake/8766_udg_grid \
        --id tract=8766 filter=HSC-I^HSC-G \
        --job=multi_8766_udgGrid --clobber-config -C multi_pix.config \
        --queue small --nodes 9 --procs 12 \
        --batch-type=pbs --mpiexec="-bind-to socket" --time=1000000
    ```

### runMatchFakes.py 

#### HSC-I

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid 8766 \
        -f HSC-I -c src_8766_UDG_grid_45.0asec_I.fits \
        -o dr1_8766_UDG_grid_HSC-I_multiPix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_UDG_grid_HSC-I_multiPix.fits`

#### HSC-G

* Command:
    ```
    runMatchFakes.py /lustre/Subaru/SSP/rerun/song/fake/8766_udg_grid 8766 \
        -f HSC-G -c src_8766_UDG_grid_45.0asec_G.fits \
        -o dr1_8766_UDG_grid_HSC-G_multiPix \
        -w -t 2.0 \
        -j 6
    ```
    - Output: `dr1_8766_UDG_grid_HSC-G_multiPix.fits`






----

## Test Mosaic.py 

    ```
    mosaic.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_highn/ \
        --diagnostics --diagDir=mosaicDiag \
        --id tract=8766 visit="7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484" \
        ccd=0..103 filter=HSC-I expTime=270.0^300.0
    ```

    ```
    mosaic.py /lustre2/HSC_DR/dr1/s15b/data/s15b_wide/ \
        --output /lustre/Subaru/SSP/rerun/song/fake/8766_lown/ \
        --diagnostics --diagDir=mosaicDiag \
        --id tract=8766 visit="7288^7292^7300^7304^7310^7318^7322^7338^7340^7344^7346^7350^7352^7356^7358^7360^7370^7372^7384^7386^7392^7394^7396^7408^7416^19396^19400^19404^19414^19416^19454^19456^19466^19468^19470^19482^19484" \
        ccd=0..103 filter=HSC-I expTime=270.0^300.0
    ```

* Reference: 
    ```
    mosaic.py /tigress/HSC/HSC --rerun hsc-1375/20151126/cosmos --diagnostics --diagDir=20151126/cosmos/g --id tract=0 ccd=0..103 field=SSP_UDEEP_COSMOS filter=HSC-G expTime=300.0
    mosaic.py /tigress/HSC/HSC --rerun hsc-1375/20151126/cosmos --diagnostics --diagDir=20151126/cosmos/r --id tract=0 ccd=0..103 field=SSP_UDEEP_COSMOS filter=HSC-R expTime=360.0^300.0
    mosaic.py /tigress/HSC/HSC --rerun hsc-1375/20151126/cosmos --diagnostics --diagDir=20151126/cosmos/i --id tract=0 ccd=0..103 field=SSP_UDEEP_COSMOS filter=HSC-I expTime=270.0^300.0
    mosaic.py /tigress/HSC/HSC --rerun hsc-1375/20151126/cosmos --diagnostics --diagDir=20151126/cosmos/z --id tract=0 ccd=0..103 field=SSP_UDEEP_COSMOS filter=HSC-Z expTime=270.0^300.0
    mosaic.py /tigress/HSC/HSC --rerun hsc-1375/20151126/cosmos --diagnostics --diagDir=20151126/cosmos/y --id tract=0 ccd=0..103 field=SSP_UDEEP_COSMOS filter=HSC-Y expTime=240.0^300.0^360.0
    ```
