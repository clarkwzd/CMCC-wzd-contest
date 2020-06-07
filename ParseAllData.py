import os
import datetime

#获取所有基站ID
list = os.listdir("./mnt/5/Alert_BTS_HW_1001-0309")

start = '2019-09-30'
end = '2020-03-09'

datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

allStationMap = {}

for i in range(0, len(list)):
    filePath = "./mnt/5/Alert_BTS_HW_1001-0309/"+list[i]
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

warningFile = open("./allwarnings", "r", encoding='utf-8')
warningList = []
for oneLine in warningFile:
    warningList.append(oneLine.strip('\n'))
print(warningList)

def addIntoStationMap(lineArray, stationMap):
    time = lineArray[0]
    timeArray = time.split(' ', 2)
    day = timeArray[0]
    warningSet = stationMap[day]
    warningSet.add(lineArray[2].strip('\n'))
    return



def checkIfBadWarning(warningSet):
    for warning in warningSet:
        if warning =='小区不可用告警' or warning == '网元连接中断':
            return '1'
        else:
            return warningList.index(warning)

for i in range(0, len(list)):
    filePath = "./mnt/5/Alert_BTS_HW_1001-0309/"+list[i]
    f = open(filePath, "r", encoding='utf-8')

    for oneLine in f:
        lineArray = oneLine.split(',', 3)
        stationName = lineArray[1]
        stationMap = allStationMap[stationName]
        if(stationMap): #not empty
            addIntoStationMap(lineArray, stationMap)
        else: #empty
            stationMap = allStationMap[stationName]
            while datestart < dateend:
                datestart += datetime.timedelta(days=1)
                key = datestart.strftime('%Y-%m-%d')
                warningSet = set()
                stationMap[key] = warningSet
            datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
            addIntoStationMap(lineArray, stationMap)
    f.close()

def printAllStation(map):
    for key in map:
        stationName = key
        sMap = map[stationName]
        print(stationName)
        for day in sMap:
            warningSet = sMap[day]
            print(day)
            print(checkIfBadWarning(warningSet))

    return

printAllStation(allStationMap)

