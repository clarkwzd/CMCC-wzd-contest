import os
import datetime
import CommonFuncs

list = os.listdir("./mnt/5/Alert_BTS_HW_0316-0322")

start = '2020-03-16'
end = '2020-03-22'

datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

allStationMap = {}

for i in range(0, len(list)):
    filePath = "./mnt/5/Alert_BTS_HW_0316-0322/"+list[i]
    f = open(filePath, "r", encoding='utf-8')
    for oneLine in f:
        if(oneLine.find(',')):
            lineArray = oneLine.split(',', 3)
            if(len(lineArray) == 3):
                warningSet = set()
                oneStationMap = {}
                stationName = lineArray[1]
                allStationMap[stationName] = oneStationMap
                break
    f.close()

warningList = CommonFuncs.getAllWarningList()

