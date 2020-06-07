import datetime
start = '2019-09-30'
end = '2020-03-09'

datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

stationMap = {}

while datestart < dateend:
    datestart += datetime.timedelta(days=1)
    key = datestart.strftime('%Y-%m-%d')
    warningSet = set()
    stationMap[key] = warningSet

file = open("./data/Alert_BTS_HW_1001-0309history.txt", "r")
for oneLine in file:
    lineArray = oneLine.split(',', 3)
    time = lineArray[0]
    timeArray = time.split(' ', 2)
    day = timeArray[0]
    stationMap[day].add(lineArray[2].strip('\n'))
file.close()
print(stationMap)




