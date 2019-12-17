#! /usr/bin/python3

npDir = "/Host/Temp/repository"
repoDir = npDir + "/images"
imgFiles = { "reserved.csv": "APP", "x.xml": "APP", "y.xml": "APP", "z.xml": "SCREEN", "p.xml": "PRODUCT" }

tmpDir = npDir + "/tmp"
csvFile = npDir + "/repositoryResults.csv"
csvHeader = [ "IMAGE", "1st SOURCE", "FULL SIZE", "COMPRESSED SIZE", "USAGE", "APP", "SCREEN", "PRODUCT" ]

import os
if not os.path.exists(tmpDir): os.mkdir(tmpDir)

import json
def printDic(dic):
    print(json.dumps(dic, indent = 4))

