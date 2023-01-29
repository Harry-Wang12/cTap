#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/18/2020 1:43 PM
# Filename: GrabAllGeneInform

import os

from ComparisonPair import ComparisonPair
from CalculateModel import CalculateModel
import time
from multiprocessing import Process

def loadtargetgene(targetgenefile, name="OC"):
    targetgenelist = []
    targetgenesample = {}
    targetgenesample["name"] = name
    targetgenesample["id"] = name
    targetgenesample["list"] = []
    for line in open(targetgenefile):
        line = line.strip()
        targetgenesample["list"].append(line.upper())
    targetgenelist.append(targetgenesample)
    return targetgenelist



# only for method4
# only 1 block
def grabinformation(filedir,outputfir):

    targetgenelist = loadtargetgene("./targetgene.txt")

    CModle = CalculateModel(Block=targetgenelist)

    # ComparisonParirlist = {}

    g = os.walk(filedir)

    for path, dir_list, file_list in g:
        for file_name in file_list:

                filepath = os.path.join(path, file_name)
                title = "GENE\tRNA\tRawValueControl\tRawValueTest\tCohortMatrixZControl\tCohortMatrixZTest\tCohortGenomeZControl\tCohortGenomeZTest\tRevisedRatio\tDiff\n"

                C = ComparisonPair()
                C.load(filepath)
                with open(outputfir + C.getname(), "w") as newfile:
                    totalinform= {}
                    newfile.write(title)

                    for genename in targetgenelist[0]["list"]:

                        totalinform[genename]={}
                        if C.getratioValue(genename) >2 :
                            totalinform[genename]["OriginalRatio"] = 2
                        elif C.getratioValue(genename) <-2 :
                            totalinform[genename]["OriginalRatio"] = -2
                        else:
                            totalinform[genename]["OriginalRatio"] = C.getratioValue(genename)

                        totalinform[genename]["RawValueControl"] = C.getrawValueC(genename)
                        totalinform[genename]["RawValueTest"] = C.getrawValueT(genename)
                        totalinform[genename]["CohortMatrixZControl"] = C.getCMZC(genename)
                        totalinform[genename]["CohortMatrixZTest"] = C.getCMZT(genename)
                        totalinform[genename]["CohortGenomeZControl"] = C.getCGZC(genename)
                        totalinform[genename]["CohortGenomeZTest"] = C.getCGZT(genename)

                    C = CModle.preprocess_4(sample=C, BM=0.5, BG=0.5, WM=0.5, WG=1.5)
                    for genename in targetgenelist[0]["list"]:
                        totalinform[genename]["RevisedRatio"] = C.getratioValue(genename)
                        line = genename+"\t"+str(totalinform[genename]["OriginalRatio"])+"\t"+str(totalinform[genename]["RawValueControl"])+"\t"+str(totalinform[genename]["RawValueTest"])+"\t"+str(totalinform[genename]["CohortMatrixZControl"])+"\t"+str(totalinform[genename]["CohortMatrixZTest"])+"\t"+str(totalinform[genename]["CohortGenomeZControl"])+"\t"+str(totalinform[genename]["CohortGenomeZTest"])+"\t"+str(totalinform[genename]["RevisedRatio"])+"\t"+str(totalinform[genename]["OriginalRatio"]-totalinform[genename]["RevisedRatio"])+"\n"
                        newfile.write(line)







    # return ComparisonParirlist










if __name__ == '__main__':
    inputdir = "./datamaterial/replacedDir_percentage_5_5_2_mean"
    outputdir = "./Best_v2/"
    grabinformation(inputdir,outputdir)
