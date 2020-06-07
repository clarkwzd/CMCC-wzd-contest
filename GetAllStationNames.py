import os
#获取所有基站ID
#list = os.listdir("./data")
list = os.listdir("/mnt/5/Alert_BTS_HW_0324-0330")
stationSet = set()

for i in range(0, len(list)):
    filePath = "/mnt/5/Alert_BTS_HW_0324-0330/"+list[i]
    f = open(filePath, "r")
    for oneLine in f:
        if(oneLine.find(',')):
            lineArray = oneLine.split(',', 3)
            print(lineArray)
            if(len(lineArray) == 3):
                stationSet.add(lineArray[1])
    f.close()

filename = "stations0324-0330.txt"
with open(filename, 'w') as file_obj:
    for station in stationSet:
        file_obj.write(station+"\n")


#    files.append(list[i])
#    print(list[i])
