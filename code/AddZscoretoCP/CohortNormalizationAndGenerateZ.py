#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/12/2020 5:45 PM
# Filename: CohortNormalizationAndGenerateZ


# This file provide necessary function for normalization and calculate Z score (file3, file 4,file 5)

import os.path
import numpy as np
from Cohortsingle import Cohortsingle
import time
import statistics
from scipy import stats


def my_interpolate(pos, v):
    """Return interpolated value pos from v.
    Args:
      pos: 0 <= x <= 1 fractional position in v
      v: [num] vector
    Returns:
      num of interpolated v @ pos
    """
    n = len(v) - 1
    low, high = int(np.floor(n * pos)), int(np.ceil(n * pos))
    if low == high:
        return v[low]
    else:
        frac = pos * n - low
        return v[low] * (1 - frac) + v[high] * (frac)


def frac_intervals(n):
    """n intervals uniformly spaced from 0 to 1 inclusive"""
    q = np.arange(0, n) / (n - 1)
    q[0], q[-1] = 0, 1
    return q


def quantile_norm_only_sorted(Matrix):
    L = Matrix.tolist()
    newL = []
    for line in L:
        Avg = np.mean(line)
        newline = []
        for x in range(len(line)):
            newline.append(Avg)
        newL.append(newline)

    return  np.asmatrix(newL)



def TrimedNormalization(inputpath,outputpath,Cutmethod,B_t,B_b,method,method1_type=False):
    #  check
    if not os.path.exists(inputpath):
        print("No big table")
        return
    if method == 1:
        if  method1_type not in ["mean" ,"median"]:
            print("No effective method1 type")
            return

    genelist = []
    samplelist = {}
    headername = []

    header = True

    with open(inputpath, "r") as inputfile:
        lines = inputfile.readlines()
        for line in lines:
            if len(line) > 0 and not line.startswith("!") and not line.startswith("#"):
                if header:
                    linedata = line.strip()
                    linedata = linedata.split("\t")
                    del (linedata[0])
                    for samplename in linedata:
                        S = Cohortsingle()
                        S.addname(samplename)
                        samplelist[samplename] = S
                        headername.append(samplename)
                    header = False

                else:
                    linedata = line.strip()
                    linedata = linedata.split("\t")
                    genename = linedata[0].replace(" ", "").upper()
                    del (linedata[0])
                    linedata = [float(i) for i in linedata]
                    if genename not in genelist:
                        genelist.append(genename)
                    for i in range(len(linedata)):
                        samplelist[headername[i]].addrawvalue(genename, linedata[i])

    UnNormalizationMatrix = []
    for samplename, value in samplelist.items():
        samplelist[samplename].ordergene()

        samplelist[samplename].sperateValues(Cutmethod,B_t,B_b)

        UnNormalizationMatrix.append(samplelist[samplename].generateVectorofMiddle())

    print("finish split")
    UnNormalizationMatrix = np.asmatrix(UnNormalizationMatrix).transpose()


    qmatrix = quantile_norm_only_sorted(UnNormalizationMatrix)

    qlist = qmatrix.transpose().tolist()

    number = 0
    time1 = time.time()
    for samplename, value in samplelist.items():
        samplelist[samplename].remapmidpart(qlist[number],method,method1_type)
        number += 1

    time2 = time.time()
    print("finish remape total cost :" + str(time2 - time1))
    print("finish calculate")
    with open(outputpath, "w") as outputfile:
        line = "ID_REF"
        for samplename in headername:
            line += "\t" + samplename
        line += "\n"

        for gene in genelist:
            line += gene
            for samplename in headername:
                line += "\t" + str(samplelist[samplename].getnormalizevaluebyname(gene))
            line += "\n"
        outputfile.write(line)

    print("done")


def generateZscore(inputpath,outputpath):
    print("start calculating Z score")

    header = True
    genelist = []
    samplelist = {}
    headername = []
    totallist = []
    totalgenelist = {}
    totalgenelistMeanlist={}
    totalgenelistSTDVlist={}
    with open(inputpath, "r") as inputfile:
        lines = inputfile.readlines()
        for line in lines:
            if len(line) > 0 and not line.startswith("!") and not line.startswith("#"):
                if header:
                    linedata = line.strip()
                    linedata = linedata.split("\t")
                    del (linedata[0])
                    for samplename in linedata:
                        S = Cohortsingle()
                        S.addname(samplename)
                        samplelist[samplename] = S
                        headername.append(samplename)
                    header = False

                else:
                    linedata = line.strip()
                    linedata = linedata.split("\t")
                    genename = linedata[0].replace(" ", "").upper()
                    del (linedata[0])
                    linedata = [float(i) for i in linedata]
                    if genename not in genelist:
                        genelist.append(genename)
                    for i in range(len(linedata)):
                        samplelist[headername[i]].addrawvalue(genename, linedata[i])
                        totallist.append(float(linedata[i]))
                        if genename not in totalgenelist:
                            totalgenelist[genename] = []
                            totalgenelist[genename].append(float(linedata[i]))
                        else:
                            totalgenelist[genename].append(float(linedata[i]))
                    totalgenelistMeanlist[genename] =  statistics.mean(totalgenelist[genename])
                    totalgenelistSTDVlist[genename] = statistics.stdev(totalgenelist[genename])


    # matrixMean = statistics.mean(totallist)
    # matrixSTDV = statistics.stdev(totallist)

    Ztypelist = ["sample","genome"]
    for Ztype in Ztypelist:
        print("start calculating Z score: "+Ztype)
        newZscoredict = {}
        outputfilepath = outputpath+Ztype+"_Z.txt"

        for samplename, value in samplelist.items():

            newZscoredict[samplename] = samplelist[samplename].getcorhortZscorevalue(totalgenelistMeanlist,totalgenelistSTDVlist, Ztype)

        with open(outputfilepath, "w") as outputfile:
            line = "ID_REF"
            for samplename in headername:
                line += "\t" + samplename
            line += "\n"
            for i in range(len(genelist)):
                line += genelist[i]
                for samplename in headername:
                    line += "\t" + str(newZscoredict[samplename][i])
                line += "\n"
            outputfile.write(line)
    print("done")




#
# inputpath = "CohortTotalTable_2020-07-07-21_15_02.txt" #get from outside
# outputpath = "./QNresult_Cohort.txt" #get from outside
#
# Cutmethod = "percentage" #"Zscore"
# B_t = 10 #3
# B_b = 10 #3
#
# # BZ_t = 3
# # BZ_b = 3
# method1_type = "mean" #"median"
# method = 1 #2