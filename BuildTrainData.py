# 构建训练数据集，以 7 天的数据作为输入，预测第 8 天是否会退服
# 以20191001-20200309，中每 8 天的数据构建一条训练数据，其中前面 7 天 对应的是X，第 8 天对应的是Y
# 前面 7 天的数据中，以 163 种告警为特征，只要 7 天中曾经发生过该种告警，就将相应的特征位置处 设置为 1，否则设置为 0
# 第 8 天的数据中，如果出现两种退服告警，则设置为 1，否则设置为 0
# 最后每一个文件所形成的数据为一个新的数据集，其中每一列有 164 个数据，其中前面 163 个数据为 X， 第164 个数据为 Y
# 文件名修改为基站的名字
# https://cloud.tencent.com/developer/article/1043093

# Update 由于采用 163种警告信息，发现有些告警出现的次数太少，可以暂不考虑这部分特征，因此，统计选取出现 100 次以上的特征
# 将所选取出来的特征放在 selectedwarnings 中，一共 112 种

import os
import datetime
import CommonFuncs
import numpy as np

list = os.listdir("./mnt/5/Alert_BTS_HW_1001-0309")

start = '2019-09-30'
end = '2020-03-09'

datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

days = dateend - datestart
daysNum = days.days
its = daysNum - 6  # 每一个基站构建出 its 条特征数据

allStationMap = {}

for i in range(0, len(list)):
    filePath = "./mnt/5/Alert_BTS_HW_1001-0309/"+list[i]
    f = open(filePath, "r", encoding='utf-8')
    isFirstLine = True
    for oneLine in f:
        if (isFirstLine):
            isFirstLine = False
            continue
        if(oneLine.find(',')):
            lineArray = oneLine.split(',', 3)
            if(len(lineArray) == 3):
                oneStationMap = {}
                stationName = lineArray[1]
                allStationMap[stationName] = oneStationMap
                break
    f.close()

print(allStationMap)

warningFile = open("./selectedwarnings", "r", encoding='utf-8')
warningList = []
for oneLine in warningFile:
    warningList.append(oneLine.strip('\n'))

print(warningList)

stationDayWarningMap = {}  # key: stationName, value: dayWarningMap

for i in range(0, len(list)):
    filePath = "./mnt/5/Alert_BTS_HW_1001-0309/"+list[i]
    f = open(filePath, "r", encoding='utf-8')

    # 开始分析每一个文件
    isFirstLine = True
    stationMyName = ""
    dayWarningMap = {}  # key: day, value: warningSet (the int number of warning)
    for oneLine in f:
        if(isFirstLine):
            isFirstLine = False
            continue  # 越过第一行
        lineArray = oneLine.split(',', 3)  # 2020-03-17 20:56:10,ACZDoAAEUAAAdoKAHu,X2接口故障告警
        time = lineArray[0]
        timeArray = time.split(' ', 2)
        day = timeArray[0]
        if(len(stationMyName) == 0):
            stationMyName =lineArray[1]
        warning = lineArray[2].strip('\n')
        warningFeature = warningList.index(warning)
        if(day in dayWarningMap.keys()):  # not empty
            warningSet = dayWarningMap[day]
            warningSet.add(warningFeature)
        else:  # empty
            warningSet = set()
            warningSet.add(warningFeature)
            dayWarningMap[day] = warningSet
    f.close()
    stationDayWarningMap[stationMyName] = dayWarningMap


print(stationDayWarningMap)

trainData = {}  # key: 7 days value in 112 features ; value: if the 8th day is two bad warning

for key in stationDayWarningMap:  # key: stationName, value: dayWarningMap
    fileName = "./mnt/5/trainData/" + key + ".txt"
    openFile = open(fileName, 'w')
    dayWarningMap = stationDayWarningMap[key]  # key: day, value: warningSet (the int number of warning)
    print(dayWarningMap)
    for index in range(0, 154):  # 154 lines data
        dateList = []  # 7 days
        for added in range(1, 8):
            dateList.append(datestart + datetime.timedelta(days=index + added))
        dateY = str((datestart + datetime.timedelta(days=index + 8)).date())
        inputX = np.zeros((112), dtype=np.int)  # 112 rows data
        outputY = 0  # 0 if safe, 1 if danger
        for oneDate in dateList:  # 7 days
            dateKey = str(oneDate.date())
            if(dateKey in dayWarningMap.keys()):
                warningSetInThisDate = dayWarningMap[dateKey]
                for warningIndex in warningSetInThisDate:
                    inputX[warningIndex] = 1
        if(dateY in dayWarningMap.keys()):
            warningSetInThisDate = dayWarningMap[dateY]
            if 110 in warningSetInThisDate or 111 in warningSetInThisDate:
                outputY = 1

        if np.sum(inputX) > 1:
            #if outputY == 1:
            line = ""
            for x in inputX:
                line = line + str(x) + ","
            line = line + str(outputY)
            print(line)
            openFile.write(line+"\n")
    openFile.close()





filename = "stations0324-0330.txt"
#with open(filename, 'w') as file_obj:
#    for station in stationSet:
#        file_obj.write(station+"\n")
