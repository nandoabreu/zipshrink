#! /usr/bin/python3

npDir = "/Host/Temp/store_repository"
repoDir = npDir + "/images"
imgFiles = { "reserved.csv": "APP", "store-db.xml": "APP", "workflow.xml": "APP", "screen.xml": "SCREEN", "product-db.xml": "PRODUCT" }

tmpDir = npDir + "/tmp"
csvFile = npDir + "/repositoryResults.csv"
csvHeader = [ "IMAGE", "1st SOURCE", "FULL SIZE", "COMPRESSED SIZE", "USAGE", "APP", "SCREEN", "PRODUCT" ]

import os
if not os.path.exists(tmpDir): os.mkdir(tmpDir)

import json
def printDic(dic):
    print(json.dumps(dic, indent = 4))

