def addIntoStationMap(lineArray, stationMap):
    time = lineArray[0]
    timeArray = time.split(' ', 2)
    day = timeArray[0]
    warningSet = stationMap[day]
    warningSet.add(lineArray[2].strip('\n'))
    return

def getAllWarningList():
    warningFile = open("./allwarnings", "r", encoding='utf-8')
    warningList = []
    for oneLine in warningFile:
        warningList.append(oneLine.strip('\n'))
    return warningList

def checkIfBadWarning(warningSet, warningList):
    result = []
    for warning in warningSet:
        if warning =='小区不可用告警' or warning == '网元连接中断':
            result.append(1)
        else:
            result.append(warningList.index(warning))
    return result
