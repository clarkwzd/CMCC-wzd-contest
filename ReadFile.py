import datetime

f = open("./data/Alert_BTS_HW_1001-0309history.txt", "r", encoding='utf-8')
warningSet = set()
for oneLine in f:
    lineArray = oneLine.split(',', 3)
    warningSet.add(lineArray[2].strip('\n'))
f.close()
#print(warningSet)


a = '2016-09-18'
b = '2016-09-20'
a_ = datetime.datetime.strptime(a,'%Y-%M-%d')
b_ = datetime.datetime.strptime(b,'%Y-%M-%d')
c = b_ - a_
print(c.days)

start = '2019-09-30'
end = '2020-03-09'

datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')

days = dateend - datestart
daysNum = days.days

its = daysNum - 6
print(its)

printOnce = True
for index in range(0, 154):
    dateList = []
    for added in range(1, 8):
        dateList.append(datestart + datetime.timedelta(days=index + added))
    if(printOnce):
        for oneDate in dateList:
            print(oneDate.date())
        dateY = datestart + datetime.timedelta(days=8)
        print(dateY.date())
        printOnce = False


