#! /usr/bin/python3

import f0_globalization as f0

import csv
csv.register_dialect("sep", delimiter = ";")
obj = open(f0.csvFile, mode = "r", encoding = "utf8")
csvHeader = obj.readline().strip().split(";")

dicKey = csvHeader[0]
csvDic = {}
with open(f0.csvFile, "r", encoding="utf8") as obj:
    readFrom = csv.DictReader(obj, dialect = "sep")
    for row in readFrom:
        rowKey = row.get(dicKey)
        csvDic[rowKey.lower()] = {"IMAGE": rowKey}
        for i in range(1, len(csvHeader)):
            key = csvHeader[i]
            val = row[key]
            csvDic[rowKey.lower()].update({key: val})
#f0.printDic(csvDic)

import os
def readFile(filename, status, group):
    i = filename.rfind("/") + 1
    store = filename[i:(i+3)]
    print("Reading file:", filename, "; store:", store, "; status:", status, "; group:", group)

    shCmd  = "xmllint --format " + filename + " | dos2unix | grep -v -e '^#^' -e '^$' | grep -A1 -i -E '[\.\<](jpe?g|png|gif|bmp|tiff|Product statusCode=|Screen number=)' 2>&1"
    shCmd += " | grep -i -E '[\.\<](jpe?g|png|gif|bmp|tiff|Product statusCode|ProductCode>|Screen number=)' | sed 's/.*<Product statusCode=\"\(\w\+\)\" productClass.*/\\1.IS_NEXT_PRODUCT/'"
    shCmd += " | sed -e 's/.*<ProductCode>\([0-9]\+\)<\/ProductCode>.*/\\1\\.ProductCode/' -e 's/.*<Screen number=\"\([0-9]\+\)\" .*/\\1\\.ScreenNum/'"
    shCmd += " | sed -e 's#=\"#\\n\"#g' -e 's#|#\\n#g' | sed \"s#[;,']#\\n#g\" | grep -E '\.(jpe?g|png|gif|bmp|tiff|IS_NEXT_PRODUCT|ProductCode|ScreenNum)'"
    shCmd += " | sed 's#.*<.*>\(.*\)</.*>.*#\\1#' | sed \"s#[\\\"'][ />].*##\" | sed \"s#'\\$##\" | sed \"s#^[\\\"']##\" | sed 's#^\\.\\.\\\##' | grep -v -E '[:;,<>\"]'"
    print(shCmd)

    global csvDic
    tid = filename[i:]
    prodStatus = None
    titleLine = False
    k = 0
    for line in os.popen(shCmd).read().splitlines():
        #print("##### parsing line", line)
        k += 1
        if group == "APP":
            if filename[i:] == "reserved.csv": tid = "Reserved"
            else: tid = tid[:3]
            #print("\t",k,"### TID is set as", tid, "on line", line, "of group", group, "of file", filename)
        elif group == "SCREEN":
            if ".ScreenNum" in line:
                tid = line[:line.index(".")]
                titleLine = True
            elif titleLine: titleLine = False
        elif group == "PRODUCT":
            if ".IS_NEXT_PRODUCT" in line:
                prodStatus = line[:line.index(".")]
                titleLine = True
            elif ".ProductCode" in line:
                tid = line[:line.index(".")]
                titleLine = True
            elif titleLine: titleLine = False
            #print("\t",k,"### TID is set as", tid, "on line", line, "of group", group, "of file", filename)

        if titleLine: continue
        print("\t", k, "Checking if", line.lower(), "is in repo dictionary...")

        if line.lower() in csvDic:
            print("\tFOUND in repository/ies:", line, "gonna get tid", tid)
            if csvDic[line.lower()]["USAGE"] == "NOT Used" or csvDic[line.lower()]["USAGE"] == "Inactive PLU":
                if prodStatus == "INACTIVE":
                    csvDic[line.lower()]["USAGE"] = "Inactive PLU"
                    print("\t\t:: INACTIVE :: product ::",tid)
                else:
                    csvDic[line.lower()]["USAGE"] = status

            if not csvDic[line.lower()][group]:
                #print("\t\tSetting group:", group)
                csvDic[line.lower()][group] = {}
            if not tid in csvDic[line.lower()][group]:
                #print("\t\t\tUpdating group:", group, "of", line.lower(), "with TID", tid)
                csvDic[line.lower()][group].update({tid: 1})
        elif not titleLine:
            print("\tNot found in repository/ies:", line)
        else: print("\tThis is a title line:", line)


import glob
for filename in f0.imgFiles:
    status = "Used"
    if filename == "reserved.csv": status = "Reserved"
    group = f0.imgFiles[filename]

    files = [f for f in glob.glob(f0.npDir + "/*" + filename, recursive = False)]
    for imgFile in files:
        readFile(imgFile, status, group)

# Convert ProductCodes and ScreenNums from disctionary/json into string for csv optimization
for line in csvDic:
    groups = [ "APP", "SCREEN", "PRODUCT" ]
    for group in groups:
        if csvDic[line.lower()][group]:
            csvDic[line.lower()][group] = " ".join(csvDic[line.lower()][group].keys())

#f0.printDic(csvDic)

########################################################### TENTAR GRAVAR EM UM TMP FILE
obj = open(f0.csvFile + ".tmp", mode="w")
writeTo = csv.DictWriter(obj, delimiter=";", fieldnames = csvHeader)
writeTo.writeheader()

for img in csvDic:
    rowDic = {}
    for key in csvDic[img]:
        rowDic.update({key: csvDic[img][key]})

    writeTo.writerow(rowDic)

obj.close()
os.replace(f0.csvFile + ".tmp", f0.csvFile)


#tmpObj.close()
#print("(TOTALS);{};{}".format(totalSize, compressedSize))

#M# zip file repository package content images list read size read update csv charcode utf8 utf-8

