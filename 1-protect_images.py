#! /usr/bin/python3

npDir = "/Host/Temp/STORE"
#repositoryDir = npDir + "/images"
csvFile = "/tmp/repositoryResults.csv"
imgFiles = { "reserved.csv": "APP", "store-db.xml": "APP", "workflow.xml": "APP", "screen.xml": "SCREEN", "product-db.xml": "PRODUCT" }

import json
def printDic(dic):
    print(json.dumps(dic, indent = 4))

import csv
csv.register_dialect("sep", delimiter = ";")
obj = open(csvFile, mode = "r", encoding = "utf8")
header = obj.readline().strip().split(";")

dicKey = header[0]
csvDic = {}
with open(csvFile, "r", encoding="utf8") as obj:
    readFrom = csv.DictReader(obj, dialect = "sep")
    for row in readFrom:
        rowKey = row.get(dicKey)
        csvDic[rowKey.lower()] = {"IMAGE": rowKey}
        for i in range(1, len(header)):
            key = header[i]
            val = row[key]
            csvDic[rowKey.lower()].update({key: val})
#printDic(csvDic)

import os
def readFile(filename, status, group):
    i = filename.rfind("/") + 1
    store = filename[i:(i+3)]
    print("Reading file:", filename, "; store:", store, "; status:", status, "; group:", group)

    shCmd  = "xmllint --format " + filename + " | dos2unix | grep -A1 -i -E '[\.\<](jpe?g|png|gif|bmp|tiff|Product statusCode=\"ACTIVE\"|Screen number=)' 2>&1"
    shCmd += " | grep -i -E '[\.\<](jpe?g|png|gif|bmp|tiff|ProductCode>|Screen number=)'"
    shCmd += " | sed -e 's/.*<ProductCode>\([0-9]\+\)<\/ProductCode>.*/\\1\\.ProductCode/' -e 's/.*<Screen number=\"\([0-9]\+\)\" .*/\\1\\.ScreenNum/'"
    shCmd += " | sed -e 's#=\"#\\n\"#g' -e 's#|#\\n#g' | sed \"s#[;,']#\\n#g\" | grep -E '\.(jpe?g|png|gif|bmp|tiff|ProductCode|ScreenNum)'"
    shCmd += " | sed 's#.*<.*>\(.*\)</.*>.*#\\1#' | sed \"s#[\\\"'][ />].*##\" | sed \"s#'\\$##\" | sed \"s#^[\\\"']##\" | sed 's#^\\.\\.\\\##' | grep -v -E '[:;,<>\"]'"

    global csvDic
    tid = filename[i:]
    k = 0
    for line in os.popen(shCmd).read().splitlines():
        k += 1
        if group == "APP":
            if filename[i:] == "reserved.csv": tid = "Reserved"
            else: tid = tid[:3]
            #print("\t",k,"### TID is set as", tid, "on line", line, "of group", group, "of file", filename)
        else:
            if ".ProductCode" in line: tid = line[:line.index(".")]
            elif ".ScreenNum" in line: tid = line[:line.index(".")]
            #print("\t",k,"### TID is set as", tid, "on line", line, "of group", group, "of file", filename)

        #print("\t",k,"Checking if", line.lower(), "is in repo dictionary...")
        if line.lower() in csvDic:
            #print("\tFOUND in repository/ies:", line, "gonna get tid", tid)
            if csvDic[line.lower()]["USAGE"] == "NOT Used": csvDic[line.lower()]["USAGE"] = status
            if not csvDic[line.lower()][group]:
                #print("\t\tSetting group:", group)
                csvDic[line.lower()][group] = {}
            if not tid in csvDic[line.lower()][group]:
                #print("\t\t\tUpdating group:", group, "of", line.lower(), "with TID", tid)
                csvDic[line.lower()][group].update({tid: 1})
        else:
            print("\tNot found in repository/ies:", line)


import glob
for filename in imgFiles:
    status = "Used"
    if filename == "reserved.csv": status = "Reserved"
    group = imgFiles[filename]

    files = [f for f in glob.glob(npDir + "/*" + filename, recursive = False)]
    for imgFile in files:
        readFile(imgFile, status, group)

# Convert ProductCodes and ScreenNums from disctionary/json into string for csv optimization
for line in csvDic:
    groups = [ "APP", "SCREEN", "PRODUCT" ]
    for group in groups:
        if csvDic[line.lower()][group]:
            csvDic[line.lower()][group] = " ".join(csvDic[line.lower()][group].keys())

#printDic(csvDic)

########################################################### TENTAR GRAVAR EM UM TMP FILE
obj = open(csvFile + ".tmp", mode="w")
writeTo = csv.DictWriter(obj, delimiter=";", fieldnames = header)
writeTo.writeheader()

for img in csvDic:
    rowDic = {}
    for key in csvDic[img]:
        rowDic.update({key: csvDic[img][key]})

    writeTo.writerow(rowDic)

obj.close()
os.replace(csvFile + ".tmp", csvFile)


#tmpObj.close()
#print("(TOTALS);{};{}".format(totalSize, compressedSize))

#M# zip file repository package content images list read size read update csv charcode utf8 utf-8

