#! /usr/bin/python3

import f0_globalization as f0

import os
import glob
repoFiles = [f for f in glob.glob(f0.repoDir + "/*.zip", recursive = False)]
for filename in repoFiles:
    if "NEW" in filename: continue

    print("Expanding file", filename)
    shCmd = "rm -fr " + f0.tmpDir + "/* && unzip -q " + filename + " -d " + f0.tmpDir
    os.system(shCmd)

    print("Cleaning unused files from", f0.tmpDir)
    shCmd = "cat " + f0.csvFile + " | grep 'NOT Used' | cut -d';' -f1"
    for line in os.popen(shCmd).read().splitlines():
        shCmd = "rm -fr \"" + f0.tmpDir + "/" + line + "\""
        os.system(shCmd)

    i = filename.find("\.zip") - 3
    newFile = filename[:i] + ".NEW" + filename[i:]
    shCmd = "rm -fr \"" + newFile + "\""
    os.system(shCmd)

    print("Recreating new package in", newFile)
    shCmd = "cd " + f0.tmpDir + " && zip -q \"" + newFile + "\" * && cd -"
    os.system(shCmd)

