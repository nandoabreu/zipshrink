#! /usr/bin/python3

npDir = "sample"
repositoryDir = npDir #+ "/images"
tmpDir = npDir + "/tmp"

import os
import glob
repoFiles = [f for f in glob.glob(repositoryDir + "/*.zip", recursive = False)]
for filename in repoFiles:
    if "NEW" in filename: continue

    print("Expanding file", filename)
    shCmd = "rm -fr " + tmpDir + " && unzip -q " + filename + " -d " + tmpDir
    os.system(shCmd)

    print("Cleaning unused files from", tmpDir)
    shCmd = "cat /tmp/repositoryResults.csv | grep 'NOT Used' | cut -d';' -f1"
    for line in os.popen(shCmd).read().splitlines():
        shCmd = "rm -fr \"" + tmpDir + "/" + line + "\""
        os.system(shCmd)

    i = filename.find("\.zip") - 3
    newFile = filename[:i] + ".NEW" + filename[i:]
    shCmd = "rm -fr \"" + newFile + "\""
    os.system(shCmd)

    print("Recreating new package in", newFile)
    shCmd = "cd " + tmpDir + " && zip -q \"" + newFile + "\" * && cd -"
    os.system(shCmd)

