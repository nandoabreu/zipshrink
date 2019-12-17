#! /usr/bin/python3

import f0_globalization as f0

import re
from zipfile import ZipFile

imgDic = {}
totalSize = 0
compressedSize = 0
def readRepository(filename):
    i = filename.rfind("/") + 1
    source = "Package " + filename[i:(i+9)]
    print("Reading file:", filename, "; source:", source)

    global imgDic, totalSize, compressedSize
    with ZipFile(filename, "r") as obj:
        repository = obj.infolist()
        for item in repository:
            fileID = re.sub("[^A-Za-z0-9\.-_ ]+", "", item.filename.lower(), flags=re.I)

            if not fileID in imgDic:
                imgDic[fileID] = { "IMAGE": item.filename, "1st SOURCE": source, "FULL SIZE": item.file_size, "COMPRESSED SIZE": item.compress_size, "USAGE": "NOT Used" }
                #writeTo.writerow([item.filename, "Package", item.file_size, item.compress_size, "NOT Used", 0, 0, 0])
                totalSize += int(imgDic[fileID]["FULL SIZE"])
                compressedSize += int(imgDic[fileID]["COMPRESSED SIZE"])


import glob
repoFiles = [f for f in glob.glob(f0.repoDir + "/*.zip", recursive = False)]
for filename in repoFiles:
    readRepository(filename)

f0.printDic(imgDic)

import csv
with open(f0.csvFile, mode="w") as obj:
    writeTo = csv.DictWriter(obj, delimiter=";", fieldnames = f0.csvHeader)
    writeTo.writeheader()
    for img in imgDic:
        rowDic = {}
        for key in imgDic[img]:
            rowDic.update({ key: imgDic[img][key] })
        writeTo.writerow(rowDic)

print("TOTAL images size: {} ({} as compressed).".format(totalSize, compressedSize))
print("Data written to:", f0.csvFile)

#M# python-import json-import zip file repository package content images list read size write csv regexp remove-nonalpha

