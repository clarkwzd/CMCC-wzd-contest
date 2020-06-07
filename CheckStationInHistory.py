
#检查基站是否在列表中

#f = open("stations1001-0309.txt", "r")
f = open("stations1001-0309.txt", "r")
stationSet = set()
for oneLine in f:
    stationSet.add(oneLine)
f.close()

#f2 = open("stations.txt", "r")
f2 = open("stations0316-0322.txt", "r")
stationSet2 = set()
for oneLine in f2:
    stationSet2.add(oneLine)
f2.close()

filename = "stations0316-0322-check.txt"
with open(filename, 'w') as file_obj:
    for station in stationSet2:
        if station in stationSet:
            file_obj.write(station + "\n")

