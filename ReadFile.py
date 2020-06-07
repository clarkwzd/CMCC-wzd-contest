f = open("Alert_BTS_HW_1001-0309history.txt", "r")
warningSet = set()
for oneLine in f:
    lineArray = oneLine.split(',', 3)
    warningSet.add(lineArray[2].strip('\n'))
f.close()
print(warningSet)
