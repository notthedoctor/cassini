# Kernels
# LSK (leap seconds) : naif0012.tls.pc
# SCLK (spacecraft clock) : cas00172.tsc 
# PCK (planetary constants) : cpck15Dec2017.tpc
# FK (reference frames) : cas_v39.tf 
# IK (instrument geometry) : cas_iss_v10.ti [Imaging Sub System only]
# SPK (Object trajectories)

import spiceypy as spice
import datetime as dt
import pandas as pd
import urllib.request
from os.path import exists
import common
import numpy as np
import time

times = pd.read_csv('../out/label_summary.csv')
furnishedList = []
def furnish(name):
    if name not in furnishedList:
        furnishedList.append(name)
        spice.furnsh(name)
    
baseKernelsUrl = "https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/"

furnish('../local_data/naif0012.tls.pc')
furnish('../local_data/cas00172.tsc')
furnish('../local_data/cas_v39.tf')
furnish('../local_data/cpck15Dec2017.tpc')

summaryClass = common.kernels('../out/kernel_summary.csv')
J2000 = pd.Timestamp(year=2000, month=1, day=1, hour=12)

cassiniId = spice.bodn2c('Cassini')
newCols = ['x','y','z','Closest','Distance','t_loc']

for timesIndex in times.index:
    t0 = time.time()
    spacecraftClock = str(times.loc[timesIndex, 'Start clk'])
    et = spice.scs2e(cassiniId, spacecraftClock)
    spacecraftTime = J2000 + dt.timedelta(seconds=et)

    kernelList = summaryClass.requiredKernels(spacecraftTime)
    
    for l in kernelList:
        if not exists('../local_data/kernel_cache/spk/'+l):
            urllib.request.urlretrieve(baseKernelsUrl+'spk/'+l, '../local_data/kernel_cache/spk/'+l)
    
        furnish('../local_data/kernel_cache/spk/'+l)

    posSaturn = spice.spkpos('Cassini', et, 'J2000', 'NONE', 'SATURN')[0]
    posEarth = spice.spkpos('Cassini', et, 'J2000', 'NONE', 'EARTH')[0]
    posVenus = spice.spkpos('Cassini', et, 'J2000', 'NONE', 'VENUS')[0]
    posJupiter = spice.spkpos('Cassini', et, 'J2000', 'NONE', 'JUPITER')[0]
    posSun = spice.spkpos('Cassini', et, 'J2000', 'NONE', 'SUN')[0]
    distSaturn = np.sqrt(np.sum(np.power(posSaturn,2)))
    distEarth = np.sqrt(np.sum(np.power(posEarth,2)))
    distVenus = np.sqrt(np.sum(np.power(posVenus,2)))
    distJupiter = np.sqrt(np.sum(np.power(posJupiter,2)))
    if (distEarth < 1e7):
        closest = 'Earth'
        dist = distEarth
        pos = posEarth
    elif (distVenus < 1e7):
        closest = 'Venus'
        dist = distVenus
        pos = posVenus
    elif (distJupiter < 1e7):
        closest = 'Jupiter'
        dist = distJupiter
        pos = posJupiter
    elif (distSaturn < 1e7):
        closest = 'Saturn'
        dist = distSaturn
        pos = posSaturn
    else:
        closest = 'None'
        pos = posSun
        dist = 0
    times.loc[timesIndex, newCols] = [pos[0], pos[1], pos[2], closest, dist, time.time() - t0]

spice.kclear()

times.to_csv('../out/position_summary.csv')
