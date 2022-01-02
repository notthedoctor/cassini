import common
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Get file list from server
baseUrl = "https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/"

# I don't think the kernels are webified so we have to scrape them out
# by pulling all the links
r = requests.get(url=baseUrl+'spk')
soup = BeautifulSoup(r.text, 'html.parser')
fileList = []
for x in soup.pre.find_all('a')[4:]:
    fileList.append(x.contents[0])

# Get just the links for .lbl files, this also ignores all the external
# links which were scattered round the page
labelList = []
for f in fileList:
    if f.endswith('.lbl'):
        labelList.append(f)
     
        
def fileNameDate(dateStr):
    if len(dateStr) == 6:
        return pd.Timestamp(year=int('20'+dateStr[0:2]), month=int(dateStr[2:4]), day=int(dateStr[4:6]))
    else:
        return pd.Timestamp(year=int('20'+dateStr[0:2]),month=1,day=1) + pd.Timedelta(days=int(dateStr[2:5]))

# The data frame we wish to populate for interesting times for each kernel
summary = pd.DataFrame(columns=['Spacecraft','Start','Stop','Created'])
for l in labelList:
    # Want to go through all the kernal labels. Not buffering as there
    # aren't that many of them so just pull contents directly from web
    r = requests.get(url=baseUrl+'spk/'+l)
    try:
        labelDict = common.labelToDict(r.text)

        summary.loc[l[:-4]] = [  labelDict['SPACECRAFT_NAME'],
                                  common.dateConv(labelDict['START_TIME']),
                                  common.dateConv(labelDict['STOP_TIME']),
                                  common.dateConv(labelDict['PRODUCT_CREATION_TIME'])  ]
    except:
        numbers = l.split('.')[0].split('_')
        for x in range(0,len(numbers)):
            search = re.findall('\d+',numbers[x])
            if len(search) == 1:
                numbers[x] = search[0]
        if len(numbers) != 4:
            print('Failed in: '+l)
        else:
            try:
                summary.loc[l[:-4]] = [ 'CASSINI-SUPER',
                    fileNameDate(numbers[2]), fileNameDate(numbers[3]), fileNameDate(numbers[0]) ] 
            except:
                print('Failed in: '+l)

summary.to_csv('../out/kernel_summary.csv')