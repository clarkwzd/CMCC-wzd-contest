import os
#获取所有告警类型

list = os.listdir("./mnt/5/Alert_BTS_HW_1001-0309")
warningSet = set()

warningMap = {}  #  key: warning  value: number

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
                if(lineArray[2] in warningMap.keys()):
                    warningMap[lineArray[2]] = warningMap[lineArray[2]] + 1
                else:
                    warningMap[lineArray[2]] = 1
                #warningSet.add(lineArray[1])
    f.close()

for key in warningMap.keys():
    print(key.strip()+","+str(warningMap[key]))

"""
filename = "warningMap1001-0309.txt"
with open(filename, 'w') as file_obj:
    for key in warningMap.keys():
        print(key.strip()+","+str(warningMap[key]))
        file_obj.write(key.strip()+","+str(warningMap[key]))
"""
