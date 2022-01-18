import pandas as pd
import re
import numpy as np
import bitstring
import shlex
import matplotlib.pyplot as plt
import datetime


def makeDict(inList):
    i = 0
    objectSearch = False
    objectName = ''
    objectStart = 0
    retDict = {}
    while i < len(inList) and inList[i] != 'END':
        d = inList[i]
        if d != '' and d[0] != '/':
            l = d.split('=')
            l = [x.strip() for x in l]
            if not objectSearch:
                if l[0] != 'OBJECT':
                    if len(l) == 2:
                        retDict[l[0]] = l[1].strip('\"')
                else:
                    objectSearch = True
                    objectName = l[1]
                    objectStart = i + 1
            else:
                if l[0] == 'END_OBJECT' and l[1] == objectName:
                    retDict[objectName] = (makeDict(inList[objectStart:i]))
                    objectSearch = False
        i = i + 1
    return retDict

def labelToDict(label):
    data = label.splitlines()
    mergedList = []
    for d in data:
        if '=' in d:
            mergedList.append(d)
        else:
            mergedList[-1] = mergedList[-1]+d.strip()
      
    return makeDict(mergedList)

class kernels:
    def __init__(self, fileName):
        self.spkSummary = pd.read_csv(fileName, parse_dates=[2,3], index_col=0)
        
    def kernalDateString(self, stringIn):
        # If last letter is U then skip that
        if stringIn[-1] == 'U':
            version = 'U'
            end = -2
        else:
            version = stringIn[-2]
            end = -1
        if stringIn[end] == 'R':
            reconPred = 1
        else:
            reconPred = 0
        dateStr = stringIn[:end]
        date = pd.Timestamp(year=int('20'+dateStr[0:2]), month=int(dateStr[2:4]), day=int(dateStr[4:6]))
        return [date, reconPred, version]
        
    def requiredKernels(self, spacecraftTime):
        fullList = []
        for l in self.spkSummary.index:
            if self.spkSummary.loc[l,'Start'] < spacecraftTime and self.spkSummary.loc[l,'Stop'] > spacecraftTime:
                splitFileName = l.split('.')[0].split('_')
                #print(l)
                if (splitFileName[1] in ['SCPSE','SK','PE']):
                    dateInfo = self.kernalDateString(splitFileName[0])
                    fullList.append(dateInfo.__add__([splitFileName[1],l]))
    
        shortList = []
        #for i in range(0,len(fullList)):
        #    splitPoint = fullList[i].find('_')
        #    if (splitPoint == -1):
        #        # No underscore, call this now
        #        shortList.append(fullList[i])
        #    else:
        #        if ((fullList[i][-1] == 'P') or (fullList[i][-1] == 'R')):
        #            # Predicted or reconstructed tag, ignore
        #            splitPoint = splitPoint - 1
        #        best = True
        #        for j in range(i+1,len(fullList)):
        #            if (fullList[i][splitPoint:] == fullList[j][splitPoint:]):
        #                # Identical tails so compare starts
        #                stri = fullList[i][:splitPoint]
        #                strj = fullList[j][:splitPoint]
        #                if ( str.isalpha(stri[-1]) and str.isalpha(strj[-1]) ):
        #                    # End of both strings are letters so can comare versions
        #                    if (stri[-1] < strj[-1]):
        #                        # Lower version so drop
        #                        best = False
        #                if (stri[0:6].isdigit() and strj[0:6].isdigit()):
        #                    datei = pd.Timestamp(year=int('20'+stri[0:2]), month=int(stri[2:4]), day=int(stri[4:6]))
        #                    datej = pd.Timestamp(year=int('20'+strj[0:2]), month=int(strj[2:4]), day=int(strj[4:6]))
        #                    if (datei < datej):
        #                        best = False
        #        if best:
        #            shortList.append(fullList[i])
        for i in range(0,len(fullList)):
            #print(fullList[i])
            best = True
            for j in range(0,len(fullList)):
                if (i != j) and (fullList[i][3] == fullList[j][3]):
                    if fullList[i][1] >= fullList[j][1]:
                        # Reconstructed beats predicted
                        if fullList[i][2] >= fullList[j][2]:
                            # Higher version letter beats lower
                            if fullList[i][0] < fullList[j][0]:
                                # If here the date is lower 
                                best = False
                        else:
                            best = False
                    else:
                        best = False
            if best:
                #print('Best')
                shortList.append(fullList[i][4])
                
        return shortList
    
def processImg(fileName):
    # Load header
    imgFile = open(fileName, 'rb')
    headerStart = imgFile.read(100)
    lblSize = int(re.findall(r'\d+', headerStart.decode())[0])
    headerEnd = imgFile.read(lblSize - 100)
    vicarDict = {}
    vicarHeader = shlex.split(headerStart.decode() + headerEnd.decode()) #, posix=False)
    for i in range(len(vicarHeader) - 1):
        itemSplit = vicarHeader[i].split('=')
        vicarDict[itemSplit[0]] = itemSplit[1]
    
    recordSize = int(vicarDict['RECSIZE'])
                    
    #vicarHeader = vicarHeader.split()
    
    binaryHeaderData = bitstring.BitArray(imgFile.read(recordSize))
    lineHeaderData = []
    eof = False
    while not eof:
        line = imgFile.read(recordSize)
        if not line:
            eof = True
        else:
            #lineHeaderData.append(bitstring.BitArray(line))
            lineHeaderData.append(line)
    #lineHeaderData = bitstring.BitArray(imgFile.read(recordSize))
    #lineHeaderData = bitstring.BitArray(imgFile.read(recordSize))
    imgFile.close()
    
    x = pd.read_csv('binary_header.csv',delimiter=';')
    x.fillna('',inplace=True)
    for i in x.index:
        x.at[i,'Values'] = x.loc[i,'Values'].split(':')
        
        record = x.loc[i]
        word = binaryHeaderData[record.Start:record.Start + record.Size].uint
        
        x.at[i,'Raw'] = word
        if record.Values == ['N']:
            x.at[i,'Data'] = word
        elif record.Values == ['N+1']:
            x.at[i,'Data'] = word+1
        elif record.Values != '':
            if word >= len(record.Values):
                x.at[i,'Data'] = 'Out of range'
            else:
                x.at[i,'Data'] = record.Values[word]
    
    columns = ['Line number','Last valid pixel','First pixel of segment 1','Last valid pixel of Segment 1','First pixel of segment 2',
               'First Overclocked Pixel Sum','Spare','Extended Pixel Sum','Last Overclocked Pixel Sum','']
    sizeBytes = [2,2,2,2,2,2,2,6,2,2]
    lineInfo = pd.DataFrame(columns=columns)
    for j in range(len(lineHeaderData)):
        vals = np.zeros(len(sizeBytes))
        isum = 0
        for i in range(len(sizeBytes)):
            #vals[i] = lineHeaderData[j][8*isum:8*(isum+sizeBytes[1]) - 1].uint
            vals[i] = int.from_bytes(lineHeaderData[j][isum:(isum+sizeBytes[1])], byteorder='big')
            isum += sizeBytes[i]
            lineInfo.loc[j] = vals
    
    img = np.zeros((512,512))
    for i in range(512):
        img[i][:] = np.frombuffer(lineHeaderData[i][24:-1], dtype=np.uint8, count=512)        
    
    return [vicarDict, x, lineInfo, img]

def dateConv(dateStr):
    if re.search('\d+-\d+T\d+:\d+:\d+.\d+', dateStr):
        res = re.search('(\d+)-(\d+)T(\d+):(\d+):(\d+).(\d+)', dateStr)
        retDate = datetime.datetime(year=int(res.group(1)), month=1, day=1, 
                                 hour=int(res.group(3)), 
                                 minute=int(res.group(4)), 
                                 second=int(res.group(5)))
        retDate = retDate + datetime.timedelta(days=int(res.group(2)))
    else:
        if dateStr.find('/') >= 0:
            # Fix invalid time string
             dateStr = dateStr.replace('/','T')
        try:
            retDate = datetime.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%S')
        except:
            retDate = datetime.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%S.%f')
    return retDate
