#! /usr/bin/python3

npDir = "/Host/Temp/STORE"
repositoryDir = npDir + "/images"
csvFile = "/tmp/repositoryResults.csv"

header = [ "IMAGE", "1st SOURCE", "FULL SIZE", "COMPRESSED SIZE", "USAGE", "APP", "SCREEN", "PRODUCT" ]

import json
def printDic(dic):
    print(json.dumps(dic, indent = 8))

imgDic = {}
totalSize = 0
compressedSize = 0
from zipfile import ZipFile
def readRepository(filename):
    i = filename.rfind("/") + 1
    source = "Package " + filename[i:(i+9)]
    print("Reading file:", filename, "; source:", source)

    global imgDic, totalSize, compressedSize
    with ZipFile(filename, "r") as obj:
        repository = obj.infolist()
        for item in repository:
            if not item.filename.lower() in imgDic:
                imgDic[item.filename.lower()] = { "IMAGE": item.filename, "1st SOURCE": source, "FULL SIZE": item.file_size, "COMPRESSED SIZE": item.compress_size, "USAGE": "NOT Used" }
                #writeTo.writerow([item.filename, "Package", item.file_size, item.compress_size, "NOT Used", 0, 0, 0])
                totalSize += int(imgDic[item.filename.lower()]["FULL SIZE"])
                compressedSize += int(imgDic[item.filename.lower()]["COMPRESSED SIZE"])


import glob
repoFiles = [f for f in glob.glob(repositoryDir + "/*.zip", recursive = False)]
for filename in repoFiles:
    readRepository(filename)

#printDic(imgDic)

import csv
with open(csvFile, mode="w") as obj:
    writeTo = csv.DictWriter(obj, delimiter=";", fieldnames = header)
    writeTo.writeheader()
    for img in imgDic:
        rowDic = {}
        for key in imgDic[img]:
            rowDic.update({ key: imgDic[img][key] })
        writeTo.writerow(rowDic)

print("TOTAL images size: {} ({} as compressed).".format(totalSize, compressedSize))

#M# zip file repository package content images list read size write csv

