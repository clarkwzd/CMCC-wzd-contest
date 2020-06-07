import os
#gou

list = os.listdir("/mnt/5/Alert_BTS_HW_1001-0309")
warningSet = set()

for i in range(0, len(list)):
    filePath = "/mnt/5/Alert_BTS_HW_1001-0309/"+list[i]
    f = open(filePath, "r")
    for oneLine in f:
        if(oneLine.find(',')):
            lineArray = oneLine.split(',', 3)
            if(len(lineArray) == 3):
                warningSet.add(lineArray[1])
    f.close()

filename = "warning1001-0309.txt"
with open(filename, 'w') as file_obj:
    for station in warningSet:
        file_obj.write(station+"\n")