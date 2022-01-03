import os
import pandas as pd
import common
import time
  
basePath = '../local_data/image_cache/'
summary = pd.DataFrame(columns=['Start','Stop','Created','Start clk', 'Stop clk', 'Phase', 'ID', 'Filters', 't'])

for x in os.listdir(basePath):
    if os.path.isdir(basePath+x):
        for y in os.listdir(basePath+x):
            if os.path.isdir(basePath+x+'/'+y):
                for z in os.listdir(basePath+x+'/'+y):
                    t0 = time.time()
                    filePath = basePath+x+'/'+y+'/'+z
                    with open(filePath, 'r') as file:
                        data = file.read()
                    labelDict = common.labelToDict(data)
            
                    summary.loc[z] = [  common.dateConv(labelDict['START_TIME']),
                                        common.dateConv(labelDict['STOP_TIME']),
                                        common.dateConv(labelDict['PRODUCT_CREATION_TIME']),
                                        labelDict['SPACECRAFT_CLOCK_START_COUNT'],
                                        labelDict['SPACECRAFT_CLOCK_STOP_COUNT'],
                                        labelDict['MISSION_PHASE_NAME'],
                                        labelDict['OBSERVATION_ID'],
                                        labelDict['FILTER_NAME'], time.time() - t0  ]

summary.to_csv('../out/label_summary.csv')