import os,sys,gc,glob
import cdms2 as cdm
import cdutil as cdu
import MV2 as mv
import numpy as npy
from string import replace
from genutil import statistics
from libToE import findToE
import time as timc



def defModels():
#
# List available models and properties
#
#  name, props=[Nb of hist members, nb of HistNat members, idx of common interval [1861-2005]]
#      picontrol=[length of run]
#

    models = [
#        {'name':'ACCESS1-0'     ,'props':[2,0,11,156], 'picontrol':[500]}, # 0
#        {'name':'ACCESS1-3'     ,'props':[3,0,11,156], 'picontrol':[500]}, # 1
#        {'name':'bcc-csm1-1-m'  ,'props':[3,0,11,156], 'picontrol':[0]}, # 2
         {'name':'bcc-csm1-1'    ,'props':[3,1,11,156], 'picontrol':[0]}, # 3
#        {'name':'bcc-csm1-1'    ,'props':[3,1,11,21], 'picontrol':[0]}, # 3
#        {'name':'BNU-ESM'       ,'props':[1,0,11,156], 'picontrol':[559]}, # 4
         {'name':'CanESM2'       ,'props':[5,5,11,156], 'picontrol':[996]}, # 5
         {'name':'CCSM4'         ,'props':[6,4,11,156], 'picontrol':[1051]}, # 6
#        {'name':'CESM1-BGC'     ,'props':[1,0,11,156], 'picontrol':[500]}, # 7
         {'name':'CESM1-CAM5'    ,'props':[3,2,11,156], 'picontrol':[319]}, # 8
#        {'name':'CESM1-FASTCHEM','props':[3,0,11,156], 'picontrol':[175]}, # 9
#        {'name':'CESM1-WACCM'   ,'props':[1,0,11,156], 'picontrol':[200]}, # 10
#        {'name':'CMCC-CESM'     ,'props':[1,0,11,156], 'picontrol':[277]}, # 11
#        {'name':'CMCC-CM'       ,'props':[1,0,11,156], 'picontrol':[330]}, # 12
#        {'name':'CMCC-CMS'      ,'props':[1,0,11,156], 'picontrol':[500]}, # 13
#        {'name':'CNRM-CM5-2'    ,'props':[1,0,11,156], 'picontrol':[410]}, # 14
         {'name':'CNRM-CM5'      ,'props':[9,6,11,156], 'picontrol':[850]}, # 15
         {'name':'CSIRO-Mk3-6-0' ,'props':[9,5,11,156], 'picontrol':[500]}, # 16
#        {'name':'CSIRO-Mk3L-1-2','props':[2,0,10,155], 'picontrol':[0]}, # 17
#        {'name':'EC-EARTH'      ,'props':[6,0,11,156], 'picontrol':[452]}, # 18
         {'name':'FGOALS-g2'     ,'props':[4,3,11,156], 'picontrol':[700]}, # 19
#        {'name':'FGOALS-s2'     ,'props':[3,0,11,156], 'picontrol':[501]}, # 20
#        {'name':'GFDL-CM2p1'    ,'props':[9,0,11,156], 'picontrol':[0]}, # 21
         {'name':'GFDL-CM3'      ,'props':[4,3, 1,146], 'picontrol':[0]}, # 22
#        {'name':'GFDL-ESM2G'    ,'props':[1,0, 1,146], 'picontrol':[500]}, # 23
         {'name':'GFDL-ESM2M'    ,'props':[1,1, 0,145], 'picontrol':[500]}, # 24
         {'name':'GISS-E2-H'     ,'props':[14,11,11,156],'picontrol':[780]},# 25
#        {'name':'GISS-E2-H-CC'  ,'props':[1,0,11,156], 'picontrol':[251]}, # 26
         {'name':'GISS-E2-R'     ,'props':[16,11,11,156],'picontrol':[846]},# 27
#        {'name':'GISS-E2-R-CC'  ,'props':[1,0,11,156], 'picontrol':[251]}, # 28
#        {'name':'HadCM3'        ,'props':[9,0, 1,146], 'picontrol':[0]}, # 29
#        {'name':'HadGEM2-CC'    ,'props':[1,0, 1,146], 'picontrol':[240]}, # 30
         {'name':'HadGEM2-ES'    ,'props':[3,3, 1,146], 'picontrol':[576]}, # 31
         {'name':'IPSL-CM5A-LR'  ,'props':[6,3,11,156], 'picontrol':[1000]}, # 32
         {'name':'IPSL-CM5A-MR'  ,'props':[3,3,11,156], 'picontrol':[300]}, # 33
#        {'name':'IPSL-CM5B-LR'  ,'props':[1,0,11,156], 'picontrol':[300]}, # 34
         {'name':'MIROC-ESM-CHEM','props':[1,1,11,156], 'picontrol':[255]}, # 35
         {'name':'MIROC-ESM'     ,'props':[3,3,11,156], 'picontrol':[100]}, # 36
#        {'name':'MPI-ESM-LR'    ,'props':[3,0,11,156], 'picontrol':[0]}, # 37
#        {'name':'MPI-ESM-MR'    ,'props':[3,0,11,156], 'picontrol':[0]}, # 38
#        {'name':'MPI-ESM-P'     ,'props':[2,0,11,156], 'picontrol':[0]}, # 39
#        {'name':'NorESM1-ME'    ,'props':[1,0,11,156], 'picontrol':[0]}, # 40
#        {'name':'NorESM1-M'     ,'props':[2,0,11,156], 'picontrol':[0]}, # 41
        ]

    return models

# models to check
"""
    models = [
        ]
"""

def maskVal(field,valmask):
    '''
    The maskVal() function applies a mask to an array provided
    
    Author:    Eric Guilyardi : Eric.Guilyardi@locean-ipsl.upmc.fr
    Co-author: Paul J. Durack : pauldurack@llnl.gov : @durack1.
    
    Created on Sun Sep 14 21:13:30 2014

    Inputs:
    ------
    - field     - 1D/2D/3D array
    - valmask    - 1D scalar of mask value
    
    Output:
    - field     - 1D/2D/3D masked array
    
    Usage:
    ------
    >>> from binDensity import maskVal
    >>> maskedVariable = maskVal(unMaskedVariable,valmask)

    Notes:
    -----
    - PJD 15 Sep 2014 - 
    '''
    field [npy.isnan(field.data)] = valmask
    field._FillValue = valmask
    field = mv.masked_where(field > valmask/10, field)
    return field

def mmeAveMsk2D(listFiles, sw2d, years, inDir, outDir, outFile, timeInt, mme, ToeType, debug=True):
    '''
    The mmeAveMsk2D() function averages rhon/lat density bined files with differing masks
    It ouputs
     - the MME
     - a percentage of non-masked bins
     - the sign agreement of period2-period1 differences
     - ToE per run and for MME

    Author:    Eric Guilyardi : Eric.Guilyardi@locean-ipsl.upmc.fr

    Created on Tue Nov 25 13:56:20 CET 2014

    Inputs:
    -------
    - listFiles(str)         - the list of files to be averaged
    - sw2d                   - dimension of input fields to consider (1 = lat/rho or 2 = lon/lat/rho)
    - years(t1,t2)           - years for slice read
    - inDir[](str)           - input directory where files are stored (add histnat as inDir[1] for ToE)
    - outDir(str)            - output directory
    - outFile(str)           - output file
    - timeInt(2xindices)     - indices of init period to compare with (e.g. [1,20])
    - mme(bool)              - multi-model mean (will read in single model ensemble stats)
    - ToeType(str)           - ToE type ('F': none, 'histnat')
                               -> requires running first mm+mme without ToE to compute Stddev
    - debug <optional>       - boolean value

    Notes:
    -----
    - EG 25 Nov 2014   - Initial function write
    - EG 27 Nov 2014   - Rewrite with loop on variables
    - EG 06 Dec 2014   - Added agreement on difference with init period - save as <var>Agree
    - EG 07 Dec 2014   - Read bowl to remove points above bowl - save as <var>Bowl
    - EG 19 Apr 2016   - ToE computation (just for 2D files)
    - EG 07 Oct 2016   - add 3D file support

    - TODO :
                 - remove loops
                 - add computation of ToE per model (toe 1 and toe 2) see ticket #50
                 - add isonhtc (see ticket #48)
    '''

    # CDMS initialisation - netCDF compression
    comp = 1 # 0 for no compression
    cdm.setNetcdfShuffleFlag(comp)
    cdm.setNetcdfDeflateFlag(comp)
    cdm.setNetcdfDeflateLevelFlag(comp)
    cdm.setAutoBounds('on')
    # Numpy initialisation
    npy.set_printoptions(precision=2)

    if debug:
        debug = True
    else:
        debug = False
    # File dim and grid inits
    t1 = years[0]
    t2 = years[1]
    # Bound of period average to remove
    peri1 = timeInt[0]
    peri2 = timeInt[1]
    fi      = cdm.open(inDir[0]+'/'+listFiles[0])
    if sw2d == 1:
        isond0  = fi['isondepth'] ; # Create variable handle
        # Get grid objects
        axesList = isond0.getAxisList()
        sigmaGrd = isond0.getLevel()
        latN = isond0.shape[3]
        levN = isond0.shape[2]
        basN = isond0.shape[1]
        varsig='ptopsigma'
    elif sw2d == 2:
        isond0  = fi['isondepthg'] ; # Create variable handle
        # Get grid objects
        axesList = isond0.getAxisList()
        sigmaGrd = isond0.getLevel()
        lonN = isond0.shape[3]
        latN = isond0.shape[2]
        levN = isond0.shape[1]
        varsig='ptopsigmaxy'

    # Declare and open files for writing
    if os.path.isfile(outDir+'/'+outFile):
        os.remove(outDir+'/'+outFile)
    outFile_f = cdm.open(outDir+'/'+outFile,'w')

    #timN = isond0.shape[0]
    timN = t2-t1
    runN = len(listFiles)

    print ' Number of members:',len(listFiles)

    valmask = isond0.missing_value
    if sw2d == 1:
        varList = ['isondepth','isonpers','isonso','isonthetao','isonthick','isonvol']
        varFill = [0.,0.,valmask,valmask,0.,0.]
        # init arrays (2D rho/lat)
        percent  = npy.ma.ones([runN,timN,basN,levN,latN], dtype='float32')*0.
        #minbowl  = npy.ma.ones([basN,latN], dtype='float32')*1000.
        varbowl  = npy.ma.ones([runN,timN,basN,latN], dtype='float32')*1.
    #varList = ['isondepth']
    #print ' !!! ### Testing one variable ###'
    #varList = ['isonthetao']
    elif sw2d == 2:
        varList = ['isondepthg','persistmxy','sog','thetaog','isonthickg']
        varFill = [valmask,valmask,valmask,valmask,valmask]
        percent  = npy.ma.ones([runN,timN,levN,latN,lonN], dtype='float32')*0.
        varbowl  = npy.ma.ones([runN,timN,latN,lonN], dtype='float32')*1.
        varList = ['isondepthg']
        print ' !!! ### Testing one variable ###'

    # init time axis
    time       = cdm.createAxis(npy.float32(range(timN)))
    time.id    = 'time'
    time.units = 'years since 1861'
    time.designateTime()
    # init ensemble axis
    ensembleAxis       = cdm.createAxis(npy.float32(range(runN)))
    ensembleAxis.id    = 'members'
    ensembleAxis.units = 'N'
    # loop on variables
    for iv,var in enumerate(varList):

        # Array inits (2D rho/lat 3D rho/lat/lon)
        if sw2d == 1:
            shapeR = [basN,levN,latN]
            isonvar  = npy.ma.ones([runN,timN,basN,levN,latN], dtype='float32')*valmask
            vardiff,varbowl2D = [npy.ma.ones(npy.ma.shape(isonvar)) for _ in range(2)]
            varstd,varToE1,varToE2 =  [npy.ma.ones([runN,basN,levN,latN], dtype='float32')*valmask for _ in range(3)]
            varones  = npy.ma.ones([runN,timN,basN,levN,latN], dtype='float32')*1.
        elif sw2d == 2:
            shapeR = [levN,latN,lonN]
            isonvar  = npy.ma.ones([runN,timN,levN,latN,lonN], dtype='float32')*valmask
            vardiff,varbowl2D = [npy.ma.ones(npy.ma.shape(isonvar)) for _ in range(2)]
            varstd,varToE1,varToE2 =  [npy.ma.ones([runN,levN,latN,lonN], dtype='float32')*valmask for _ in range(3)]
            varones  = npy.ma.ones([runN,timN,levN,latN,lonN], dtype='float32')*1.

        print ' Variable ',iv, var
        # loop over files to fill up array
        for i,file in enumerate(listFiles):
            ft      = cdm.open(inDir[0]+'/'+file)
            model = file.split('.')[1]
            timeax  = ft.getAxis('time')
            if sw2d == 1:
                file1d = replace(inDir[0]+'/'+file,'2D','1D')
                if os.path.isfile(file1d):
                    f1d = cdm.open(file1d)
                else:
                    print 'ERROR:',file1d,'missing (if mme, run 1D first)'
                sys.exit(1)
            elif sw2d ==2:
                f1d = ft
            if i == 0:
                tmax0 = timeax.shape[0]
            tmax = timeax.shape[0]
            if tmax != tmax0:
                print 'wrong time axis: exiting...'
                return
            # read array
            # loop over time for memory management
            for it in range(timN):
                t1r = t1 + it
                t2r = t1r + 1
                isonRead = ft(var,time = slice(t1r,t2r))
                if varFill[iv] != valmask:
                    isonvar[i,it,...] = isonRead.filled(varFill[iv])
                else:
                    isonvar[i,it,...] = isonRead
            # compute percentage of non-masked points accros MME
            if iv == 0:
                maskvar = mv.masked_values(isonRead.data,valmask).mask
                percent[i,...] = npy.float32(npy.equal(maskvar,0))
            if mme:
                # if mme then just accumulate Bowl, Agree and Std fields
                varst = var+'Agree'
                vardiff[i,...] = ft(varst,time = slice(t1r,t2r))
                varb = var+'Bowl'
                varbowl2D[i,...] = ft(varb,time = slice(t1r,t2r))
            else:
                # Compute difference with average of first initN years
                varinit = cdu.averager(isonvar[i,peri1:peri2,...],axis=0)
                for t in range(timN):
                    vardiff[i,t,...] = isonvar[i,t,...] - varinit
                vardiff[i,...].mask = isonvar[i,...].mask
                # Read bowl and truncate 2D field above bowl
                if iv == 0:
                    bowlRead = f1d(varsig,time = slice(t1,t2))
                    varbowl[i,...] = bowlRead
                # Compute Stddev
                varstd[i,...] = npy.ma.std(isonvar[i,...], axis=0)
                # Compute ToE
                if ToeType == 'histnat':
                    # Read mean and Std dev from histnat
                    if sw2d ==1:
                        if i == 0:
                            filehn  = glob.glob(inDir[1]+'/cmip5.'+model+'.*zon2D*')[0]
                            #filehn = replace(outFile,'historical','historicalNat')
                            fthn = cdm.open(filehn)
                            varmeanhn = fthn(var)
                            varst = var+'Std'
                            varmaxstd = fthn(varst)
                        toemult = 1.
                        signal = npy.reshape(isonvar[i,...]-varmeanhn,(timN,basN*levN*latN))
                        noise = npy.reshape(varmaxstd,(basN*levN*latN))
                        varToE1[i,...] = npy.reshape(findToE(signal, noise, toemult),(basN,levN,latN))
                        toemult = 2.
                        varToE2[i,...] = npy.reshape(findToE(signal, noise, toemult),(basN,levN,latN))
                    elif sw2d == 2:
                        sys.exit('ToE not yet implemented for 3D fields')
                        #TODO
            ft.close()
            f1d.close()
        # <-- end of loop on files

        # Compute percentage of bin presence
        # Only keep points where percent > 50%
        if iv == 0:
            percenta = (cdu.averager(percent,axis=0))*100.
            percenta = mv.masked_less(percenta, 50)
            percentw = cdm.createVariable(percenta, axes = [time,axesList[1],axesList[2],axesList[3]], id = 'isonpercent')
            percentw._FillValue = valmask
            percentw.long_name = 'percentage of MME bin'
            percentw.units     = '%'
            outFile_f.write(percentw.astype('float32'))

        # Sign of difference
        if mme:
            vardiffsgSum = cdu.averager(vardiff, axis=0)
            vardiffsgSum = cdm.createVariable(vardiffsgSum , axes =[time,axesList[1],axesList[2],axesList[3]] , id = 'foo')
            vardiffsgSum = maskVal(vardiffsgSum, valmask)
            vardiffsgSum.mask = percentw.mask
        else:
            vardiffsg = npy.copysign(varones,vardiff)
            # average signs
            vardiffsgSum = cdu.averager(vardiffsg, axis=0)
            vardiffsgSum = mv.masked_greater(vardiffsgSum, 10000.)
            vardiffsgSum.mask = percentw.mask
            vardiffsgSum._FillValue = valmask

        # average variable accross members
        isonVarAve = cdu.averager(isonvar, axis=0)
        isonVarAve = cdm.createVariable(isonVarAve , axes =[time,axesList[1],axesList[2],axesList[3]] , id = 'foo')
        # mask
        if varFill[iv] == valmask:
            isonVarAve = maskVal(isonVarAve, valmask)

        isonVarAve.mask = percentw.mask

        # Only keep points with rhon >  bowl-delta_rho
        delta_rho = 0.
        if mme: # start from average of <var>Agree
            isonVarBowl = cdu.averager(varbowl2D, axis=0)
            isonVarBowl = cdm.createVariable(isonVarBowl , axes =[time,axesList[1],axesList[2],axesList[3]] , id = 'foo')
            isonVarBowl = maskVal(isonVarBowl, valmask)
            isonVarBowl.mask = percentw.mask
            # Compute intermodel stddev
            isonVarStd = statistics.std(varbowl2D, axis=0)
            isonVarStd = cdm.createVariable(isonVarStd , axes =[time,axesList[1],axesList[2],axesList[3]] , id = 'foo')
            isonVarStd = maskVal(isonVarStd, valmask)
            isonVarStd.mask = percentw.mask
            if iv == 0:
                # Read mulitmodel sigma on bowl and average in time
                file1d  =  replace(outDir+'/'+outFile,'2D','1D')
                if os.path.isfile(file1d):
                    f1d = cdm.open(file1d)
                else:
                    print 'ERROR:',file1d,'missing (if mme, run 1D first)'
                    sys.exit(1)
                bowlRead = f1d(varsig,time = slice(t1,t2))
                f1d.close()
                siglimit = cdu.averager(bowlRead, axis=0)  - delta_rho
            # TODO: remove loop by building global array with 1/0
            if sw2d == 1:
                for il in range(latN):
                    for ib in range(basN):
                        #if ib == 2:
                        #    print il, siglimit[ib,il]
                        if siglimit[ib,il] < valmask/1000.:
                             # if mme bowl density defined, mask above bowl
                            index = (npy.argwhere(sigmaGrd[:] >= siglimit[ib,il]))
                            isonVarBowl [:,ib,0:index[0],il].mask = True
                            isonVarStd  [:,ib,0:index[0],il].mask = True
                            vardiffsgSum[:,ib,0:index[0],il].mask = True
                        else:
                            # mask all points
                            isonVarBowl [:,ib,:,il].mask = True
                            isonVarStd  [:,ib,:,il].mask = True
                            vardiffsgSum[:,ib,:,il].mask = True
            elif sw2d == 2:
                sys.exit('ToE not yet implemented for 3D fields')
                #TODO

        else:
            isonVarBowl = isonVarAve*1. # start from variable
            isonVarStd  = isonVarAve*1. # start from variable
            if iv == 0:
                siglimit = cdu.averager(varbowl, axis=0)
                siglimit = cdu.averager(siglimit, axis=0) - delta_rho
            # TODO: remove loop by building global array with 1/0
            if sw2d == 1:
                for il in range(latN):
                    for ib in range(basN):
                        if siglimit[ib,il] < valmask/1000.:
                            # if bowl density defined, mask above bowl
                            index = (npy.argwhere(sigmaGrd[:] >= siglimit[ib,il]))
                            isonVarBowl[:,ib,0:index[0],il].mask = True
                            vardiffsgSum[:,ib,0:index[0],il].mask = True
                        else:
                            # mask all points
                            vardiffsgSum[:,ib,:,il].mask = True
            elif sw2d == 2:
                siglimit = npy.reshape(siglimit,[latN*lonN])
                isonVarBowl = npy.reshape(isonVarBowl,[runN,timN,levN,latN*lonN])
                vardiffsgSum = npy.reshape(vardiffsgSum,[runN,timN,levN,latN*lonN])
                for il in range(latN*lonN):
                    if siglimit(il)  < valmask/1000.:
                        # if bowl density defined, mask above bowl
                        index = (npy.argwhere(sigmaGrd[:] >= siglimit[il]))
                        isonVarBowl[:,0:index[0],il].mask = True
                        vardiffsgSum[:,0:index[0],il].mask = True
                    else:
                        # mask all points
                        vardiffsgSum[:,:,il].mask = True
                isonVarBowl = npy.reshape(isonVarBowl,[runN,timN,levN,latN,lonN])
                vardiffsgSum = npy.reshape(vardiffsgSum,[runN,timN,levN,latN,lonN])

            isonVarBowl = maskVal(isonVarBowl, valmask)
            # Find max of Std dev of all members
            isonVarStd = npy.ma.max(varstd, axis=0)
            # mask
            if varFill[iv] == valmask:
                isonVarStd = maskVal(isonVarStd, valmask)

        # Write
        isonave = cdm.createVariable(isonVarAve, axes = [time,axesList[1],axesList[2],axesList[3]], id = isonRead.id)
        isonave.long_name = isonRead.long_name
        isonave.units     = isonRead.units
        isonavediff = cdm.createVariable(vardiffsgSum, axes = [time,axesList[1],axesList[2],axesList[3]], id = isonRead.id+'Agree')
        isonavediff.long_name = isonRead.long_name
        isonavediff.units     = isonRead.units
        isonavebowl = cdm.createVariable(isonVarBowl, axes = [time,axesList[1],axesList[2],axesList[3]], id = isonRead.id+'Bowl')
        isonavebowl.long_name = isonRead.long_name
        isonavebowl.units     = isonRead.units
        isonmaxstd = cdm.createVariable(isonVarStd, axes = [axesList[1],axesList[2],axesList[3]], id = isonRead.id+'Std')
        isonmaxstd.long_name = isonRead.long_name
        isonmaxstd.units     = isonRead.units

        outFile_f.write(    isonave.astype('float32'))
        outFile_f.write(isonavediff.astype('float32'))
        outFile_f.write(isonavebowl.astype('float32'))
        outFile_f.write(isonmaxstd.astype('float32'))

        if ToeType == 'histnat':
            isontoe1 = cdm.createVariable(varToE1, axes = [ensembleAxis,axesList[1],axesList[2],axesList[3]], id = isonRead.id+'ToE1')
            isontoe1.long_name = 'ToE 1 for '+isonRead.long_name
            isontoe1.units     = 'Year'
            isontoe2 = cdm.createVariable(varToE2, axes = [ensembleAxis,axesList[1],axesList[2],axesList[3]], id = isonRead.id+'ToE2')
            isontoe2.long_name = 'ToE 2 for '+isonRead.long_name
            isontoe2.units     = 'Year'
            outFile_f.write(isontoe1.astype('float32'))
            outFile_f.write(isontoe2.astype('float32'))


        if mme:
            isonvarstd = cdm.createVariable(isonVarStd , axes =[time,axesList[1],axesList[2],axesList[3]] , id = isonRead.id+'ModStd')
            isonvarstd.long_name = isonRead.long_name+' intermodel std'
            isonvarstd.units     = isonRead.units
            outFile_f.write(isonvarstd.astype('float32'))

    # <--- end of loop on variables 

    outFile_f.close()
    fi.close()

def mmeAveMsk1D(listFiles, sw2d, years, inDir, outDir, outFile, timeInt, mme, ToeType, fullTS, debug=True):
    '''
    The mmeAveMsk1D() function averages rhon or scalar density bined files with differing masks
    It ouputs the MME and a percentage of non-masked bins
    
    Created on Tue Nov 25 13:56:20 CET 2014

    Inputs:
    -------
    - listFiles(str)         - the list of files to be averaged
    - sw2d                   - dimension of fields to consider (1 or 2)
    - years(t1,t2)           - years for slice read
    - inDir(str)             - input directory where files are stored
    - outDir(str)            - output directory
    - outFile(str)           - output file
    - timeInt(2xindices)     - indices of init period to compare with (e.g. [1,20])
    - mme(bool)              - multi-model mean (will read in single model ensemble stats)
    - FfllTS                 - 0/1: if 1, uses full time serie (ignores years(t1,t2))
    - debug <optional>       - boolean value

    Notes:
    -----
    - EG 25 Nov 2014   - Initial function write
    - EG  9 Dec 2014   - Add agreement on difference with init period - save as <var>Agree
    - EG 04 Oct 2016   - Add 3D files support

    TODO:
    ------

    '''

    # CDMS initialisation - netCDF compression
    comp = 1 ; # 0 for no compression
    cdm.setNetcdfShuffleFlag(comp)
    cdm.setNetcdfDeflateFlag(comp)
    cdm.setNetcdfDeflateLevelFlag(comp)
    cdm.setAutoBounds('on')
    # Numpy initialisation
    npy.set_printoptions(precision=2)

    if debug:
        debug = True
    else:
        debug = False
    # File dim and grid inits
    t1 = years[0]
    t2 = years[1]
    # Bound of period average to remove
    peri1 = timeInt[0]
    peri2 = timeInt[1]
    # Find dimension
    runN = len(listFiles)
    try:
        fi = cdm.open(inDir[0]+'/'+listFiles[0])
    except:
        print ' *** file not found ',inDir[0]+'/'+listFiles[0]
        sys.exit(' Abort')
    if sw2d == 1:
        ptopd0  = fi['ptopdepth'] ; # Create variable handle
        latN = ptopd0.shape[2]
        basN = ptopd0.shape[1]
    elif sw2d == 2:
        ptopd0  = fi['ptopdepthxy'] ; # Create variable handle
        lonN = ptopd0.shape[2]
        latN = ptopd0.shape[1]

    #timN = ptopd0.shape[0]
    timN = t2-t1
    if fullTS:
        print '  !!! Working on full Time Serie (fullTS = True)'
        timN = ptopd0.shape[0]
        t1=0
        t2=timN
    # Get grid objects
    axesList = ptopd0.getAxisList()
    # Declare and open files for writing
    if os.path.isfile(outDir+'/'+outFile):
        os.remove(outDir+'/'+outFile)
    outFile_f = cdm.open(outDir+'/'+outFile,'w')

    print ' Number of members:',len(listFiles)

    valmask = ptopd0.missing_value

    # init time axis
    time       = cdm.createAxis(npy.float32(range(timN)))
    time.id    = 'time'
    time.units = 'years since 1861'
    time.designateTime()

    # loop on variables
    # init percent array

    if sw2d == 1:
        varList = ['ptopdepth','ptopsigma','ptopso','ptopthetao','volpers','salpers','tempers']
        #varList = ['ptopdepth']
        varDim  = [1,1,1,1,0,0,0]
        percent  = npy.ma.ones([runN,timN,basN,latN], dtype='float32')*0.
    elif sw2d == 2:
        varList = ['ptopdepthxy','ptopsigmaxy','ptopsoxy','ptopthetaoxy']
        #varList = ['ptopdepthxy']
        varDim  = [2,2,2,2]
        percent  = npy.ma.ones([runN,timN,latN,lonN], dtype='float32')*0.

    varFill = [valmask,valmask,valmask,valmask,valmask,valmask,valmask,valmask,valmask]

    axis1D = [time,axesList[1],axesList[2]]
    axis0D = [time,axesList[1]]
    print ' timN = ',timN

    # loop on 1D variables
    for iv,var in enumerate(varList):
        ti0 = timc.clock()

        # Array inits
        if varDim[iv] == 2:
            isonvar = npy.ma.ones([runN,timN,latN,lonN], dtype='float32')*valmask
            vardiff = npy.ma.ones([runN,timN,latN,lonN], dtype='float32')*valmask
            varones = npy.ma.ones([runN,timN,latN,lonN], dtype='float32')*1.
            axisVar = axis1D
        elif varDim[iv] == 1:
            isonvar = npy.ma.ones([runN,timN,basN,latN], dtype='float32')*valmask
            vardiff = npy.ma.ones([runN,timN,basN,latN], dtype='float32')*valmask
            varones = npy.ma.ones([runN,timN,basN,latN], dtype='float32')*1.
            axisVar = axis1D
        else:
            isonvar = npy.ma.ones([runN,timN,basN], dtype='float32')*valmask
            vardiff = npy.ma.ones([runN,timN,basN], dtype='float32')*valmask
            varones = npy.ma.ones([runN,timN,basN], dtype='float32')*1.
            axisVar = axis0D
        print ' Variable ',iv, var, varDim[iv]
        # loop over files to fill up array
        for ic,file in enumerate(listFiles):
            ft      = cdm.open(inDir[0]+'/'+file)
            timeax  = ft.getAxis('time')
            if ic == 0:
                tmax0 = timeax.shape[0]
            tmax = timeax.shape[0]
            if tmax != tmax0:
                print "wrong time axis: exiting..."
                print ' -> file:',ic, inDir[0]+'/'+file
                return
            # read array
            computeVar = False
            #try:
            #    varPresent = ft[var][0]
            #except NameError:
            #computeVar = True
            if (var == 'ptopsigmaxy') & computeVar:
                print '  ic = ',ic
                # reconstruct from isondepthg and ptopdepthxy

                isond = ft('isondepthg',time = slice(t1,t2))
                #print isond.data.shape, timN*latN*lonN
                itest = 94*360+150
                axesList = isond.getAxisList()
                levs = axesList[1][:]
                levN = len(levs)
                #ti02 = timc.clock()
                #levs3d  = mv.reshape(npy.tile(levs,timN*latN*lonN),(timN*latN*lonN,levN))
                levs3d0  = mv.reshape(npy.tile(levs,latN*lonN),(latN*lonN,levN))
                #ti05 = timc.clock()
                isonRead = npy.ma.ones([timN,latN,lonN], dtype='float32')*valmask
                for it in range(timN): # loop on time to limit memory usage
                    levs3d = levs3d0*1.
                    depthlo = mv.reshape(vardepth[ic,it,...],latN*lonN)
                    depth3d = npy.reshape(npy.repeat(depthlo,levN),(latN*lonN,levN))
                    isond3d = mv.reshape(npy.transpose(isond.data[it,...],(1,2,0)),(latN*lonN,levN))
                    #print isond3d[itest,:]
                    isond3d[isond3d > valmask/10] = 0.
                    #print isond3d[itest,:]
                    isond3dp1 = npy.roll(isond3d,-1,axis=1)
                    isond3dp1[:,-1] = isond3d[:,-1]
                    #print isond3dp1[itest,:]
                    #levs3d[levs3d > 30. ] = 0. # to distinguish bottom masked points from surface masked points
                    #print levs3d[itest,:]
                    levs3d[(depth3d <= isond3d)] = 0.
                    #print levs3d[itest,:]
                    levs3d[(depth3d > isond3dp1)] = 0.
                    #print levs3d[itest,:]
                    #isonwrk = npy.sum(levs3d,axis=1)
                    isonwrk = npy.max(levs3d,axis=1)
                    if it < 0:
                        print ic,it
                        print depthlo[itest]
                        print isond3d[itest,:]
                        print isonwrk[itest]
                        print
                    isonRead[it,...] = mv.reshape(isonwrk,(latN,lonN))
                # <-- end of loop on time
                del (isond3d,isond3dp1); gc.collect()
                # mask with depthxy and where sigmaxy = 0
                isonRead.mask = vardepth.mask[ic,...]
                isonRead = mv.masked_where(isonRead == 0, isonRead)
                isonRead.long_name = var
                isonRead.units = 'sigma_n'
                isonRead.id = var
                del (isond,depth3d,levs3d,levs3d0,isonwrk); gc.collect()
                #ti3 = timc.clock()
                #print ti02-ti0,ti05-ti02, ti1-ti05,ti12-ti1,ti15-ti12,ti2-ti15,ti3-ti2
                #print ti3-ti0
                # write ptopsigmaxy
                if os.path.isfile(inDir[0]+'/work/'+file):
                    os.remove(inDir[0]+'/work/'+file)
                fiout = cdm.open(inDir[0]+'/work/'+file,'w')
                isonsigxy = cdm.createVariable(isonRead, axes = axis1D, id = 'ptopsigmaxy')
                isonsigxy.long_name = 'Density of shallowest persistent ocean on ison'
                isonsigxy.units     = 'sigma_n'
                fiout.write(isonsigxy.astype('float32'))
                fiout.close()
            else:
                # Direct read of variable
                isonRead = ft(var,time = slice(t1,t2))
            #print isonRead.shape, timN
            if varFill[iv] != valmask:
                isonvar[ic,...] = isonRead.filled(varFill[iv])
            else:
                isonvar[ic,...] = isonRead
            #print isonvar[ic,:,40,100]
            # compute percentage of non-masked points accros MME
            if iv == 0:
                maskvar = mv.masked_values(isonRead.data,valmask).mask
                percent[ic,...] = npy.float32(npy.equal(maskvar,0))
            if mme:
                # if mme then just average Bowl and Agree fields
                varst = var+'Agree'
                vardiff[ic,...] = ft(varst,time = slice(t1,t2))
            else:
                # Compute difference with average of first initN years, use mask of last month
                varinit = cdu.averager(isonvar[ic,peri1:peri2,...],axis=0)
                for tr in range(timN):
                    vardiff[ic,tr,...] = isonvar[ic,tr,...] - varinit
                vardiff[ic,...].mask = isonvar[ic,...].mask

            ft.close()
        # <-- end of loop on files
        # if ptopdepthxy, keep for ptopsigmaxy computation (reconstruct from isondepthg and ptopdepthxy)
        if var =='ptopdepthxy':
            vardepth = isonvar
        # Compute percentage of bin presence
        # Only keep points where percent > 50%
        if iv == 0:
            percenta = (cdu.averager(percent,axis=0))*100.
            percenta = mv.masked_less(percenta, 50)
            percentw = cdm.createVariable(percenta, axes = axis1D, id = 'ptoppercent')
            percentw._FillValue = valmask
            percentw.long_name = 'percentage of MME bin'
            percentw.units     = '%'
            outFile_f.write(percentw.astype('float32'))
        # Sign of difference
        if mme:
            vardiffsgSum = cdu.averager(vardiff, axis=0)
            vardiffsgSum = cdm.createVariable(vardiffsgSum , axes = axisVar , id = 'foo')
            vardiffsgSum = maskVal(vardiffsgSum, valmask)
            vardiffsgSum.mask = percentw.mask
        else:
            vardiffsg = npy.copysign(varones,vardiff)
            # average signs
            vardiffsgSum = cdu.averager(vardiffsg, axis=0)
            vardiffsgSum = mv.masked_greater(vardiffsgSum, 10000.)
            vardiffsgSum.mask = percentw.mask
            vardiffsgSum._FillValue = valmask

        # average accross members
        isonVarAve = cdu.averager(isonvar, axis=0)
        isonVarAve = cdm.createVariable(isonVarAve , axes = axisVar , id = 'foo')
        # mask
        if varFill[iv] == valmask:
            isonVarAve = maskVal(isonVarAve, valmask)

        isonVarAve.mask = percentw.mask

        # Write
        isonave = cdm.createVariable(isonVarAve, axes = axisVar, id = isonRead.id)
        isonave.long_name = isonRead.long_name
        isonave.units     = isonRead.units
        isonavediff = cdm.createVariable(vardiffsgSum, axes = axisVar, id = isonRead.id+'Agree')
        isonavediff.long_name = isonRead.long_name
        isonavediff.units     = isonRead.units

        outFile_f.write(isonave.astype('float32'))
        outFile_f.write(isonavediff.astype('float32'))
        tf = timc.clock()
        print '   time var',tf-ti0
    # <--- end of loop on variables 

    outFile_f.close()
    fi.close()
