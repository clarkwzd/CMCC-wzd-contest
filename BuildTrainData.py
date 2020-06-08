# 构建训练数据集，以 7 天的数据作为输入，预测第 8 天是否会退服
# 以20191001-20200309，中每 8 天的数据构建一条训练数据，其中前面 7 天 对应的是X，第 8 天对应的是Y
# 前面 7 天的数据中，以 163 种告警为特征，只要 7 天中曾经发生过该种告警，就将相应的特征位置处 设置为 1，否则设置为 0
# 第 8 的数据中，如果出现两种退服告警，则设置为 1，否则设置为 0
# 最后每一个文件所形成的数据为一个新的数据集，其中每一列有 164 个数据，其中前面 163 个数据为 X， 第164 个数据为 Y
# 文件名修改为基站的名字
# https://cloud.tencent.com/developer/article/1043093

import os
import datetime
import CommonFuncs

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
                warningSet = set()
                oneStationMap = {}
                stationName = lineArray[1]
                allStationMap[stationName] = oneStationMap
                break
    f.close()

print(allStationMap)
warningList = CommonFuncs.getAllWarningList()
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
    print(dayWarningMap)




