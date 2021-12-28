import requests
import pandas as pd
import urllib
import os.path
import time

# Location of the "W10" JSON API
# W10: https://pds-imaging.jpl.nasa.gov/tools/w10n/#webified_data
baseUrl = 'https://pds-imaging.jpl.nasa.gov/w10n/cassini/cassini_orbiter'
# Location for HTTP file downlaods
fileUrl = 'https://pds-imaging.jpl.nasa.gov/data/cassini/cassini_orbiter'

# ISS file directories
# As this is an old mission these shouldn't change so I hard
# coded these rather than write code to generat this list
issDirList = ['coiss_0001', 'coiss_0002', 'coiss_0003', 'coiss_0004', 'coiss_0005',
 'coiss_0006', 'coiss_0007', 'coiss_0008', 'coiss_0009', 'coiss_0010',
 'coiss_0011_v4.3', 'coiss_1001', 'coiss_1002', 'coiss_1003', 'coiss_1004',
 'coiss_1005', 'coiss_1006', 'coiss_1007', 'coiss_1008', 'coiss_1009',
 'coiss_2001', 'coiss_2002', 'coiss_2003', 'coiss_2004', 'coiss_2005',
 'coiss_2006', 'coiss_2007', 'coiss_2008', 'coiss_2009', 'coiss_2010',
 'coiss_2011', 'coiss_2012', 'coiss_2013', 'coiss_2014', 'coiss_2015',
 'coiss_2016', 'coiss_2017', 'coiss_2018', 'coiss_2019', 'coiss_2020',
 'coiss_2021', 'coiss_2022', 'coiss_2023', 'coiss_2024', 'coiss_2025',
 'coiss_2026', 'coiss_2027', 'coiss_2028', 'coiss_2029', 'coiss_2030',
 'coiss_2031', 'coiss_2032', 'coiss_2033', 'coiss_2034', 'coiss_2035',
 'coiss_2036', 'coiss_2037', 'coiss_2038', 'coiss_2039', 'coiss_2040',
 'coiss_2041', 'coiss_2042', 'coiss_2043', 'coiss_2044', 'coiss_2045',
 'coiss_2046', 'coiss_2047', 'coiss_2048', 'coiss_2049', 'coiss_2050',
 'coiss_2051', 'coiss_2052', 'coiss_2053', 'coiss_2054', 'coiss_2055',
 'coiss_2056', 'coiss_2057', 'coiss_2058', 'coiss_2059', 'coiss_2060',
 'coiss_2061', 'coiss_2062', 'coiss_2063', 'coiss_2064', 'coiss_2065',
 'coiss_2066', 'coiss_2067', 'coiss_2068', 'coiss_2069', 'coiss_2070',
 'coiss_2071', 'coiss_2072', 'coiss_2073', 'coiss_2074', 'coiss_2075',
 'coiss_2076', 'coiss_2077', 'coiss_2078', 'coiss_2079', 'coiss_2080',
 'coiss_2081', 'coiss_2082', 'coiss_2083', 'coiss_2084', 'coiss_2085',
 'coiss_2086', 'coiss_2087', 'coiss_2088', 'coiss_2089', 'coiss_2090',
 'coiss_2091', 'coiss_2092', 'coiss_2093', 'coiss_2094', 'coiss_2095',
 'coiss_2096', 'coiss_2097', 'coiss_2098', 'coiss_2099', 'coiss_2100',
 'coiss_2101', 'coiss_2102', 'coiss_2103', 'coiss_2104', 'coiss_2105',
 'coiss_2106', 'coiss_2107', 'coiss_2108', 'coiss_2109', 'coiss_2110',
 'coiss_2111', 'coiss_2112', 'coiss_2113', 'coiss_2114', 'coiss_2115',
 'coiss_2116', 'coiss_3001', 'coiss_3002_v3', 'coiss_3003_v1', 'coiss_3004',
 'coiss_3005_v1', 'coiss_3006_v4', 'coiss_3007']

for mainDir in issDirList:
    # Go through each main directory and if not there, create it
    dirName = 'local_data/image_cache/{}'.format(mainDir)
    if not os.path.isdir(dirName):
        os.makedirs(dirName)
    # Pull the contents of this directory
    r = requests.get(url='{}/{}/data'.format(baseUrl, mainDir),params={'output':'json'})
    data = r.json()
    
    # Create a list of the sub directories
    nameList = []
    for d in data['nodes']:
        nameList.append(d['name'])
    
    for directory in nameList:
        # Go through each subdirectory and create and then pull
        dirName = 'local_data/image_cache/{}/{}'.format(mainDir, directory)
        if not os.path.isdir(dirName):
            os.makedirs(dirName)
        r = requests.get(url='{}/{}/data/{}'.format(baseUrl, mainDir, directory),params={'output':'json'})
        data = r.json()
        
        fileList = []
        for d in data['leaves']:
            fileList.append(d['name'])
        
        for f in fileList:
            # Look for each LBL file
            if f.endswith('.LBL'):
                # We want to have a local copy of the remote file, set up pointers
                localFile = '{}/{}'.format(dirName, f)
                fullUrl = '{}/{}/data/{}/{}'.format(fileUrl, mainDir, directory, f)
                if not os.path.exists(localFile):
                    # If this file doesn't already have a local copy then download it
                    # Have a few goes at downloading the file, note we're usingt eh file
                    # interface here rather than the JSON API
                    remaining_download_tries = 15
                    while remaining_download_tries > 0 :
                        try:
                            urllib.request.urlretrieve(fullUrl, localFile)
                            time.sleep(0.1)
                        except:
                            print("error downloading " + f +" on trial no: " + str(16 - remaining_download_tries))
                            remaining_download_tries = remaining_download_tries - 1
                            continue
                        else:
                            break                    
