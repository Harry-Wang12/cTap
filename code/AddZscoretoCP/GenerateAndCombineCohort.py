#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/12/2020 4:39 PM
# Filename: GenerateAndCombineCohort

# This file provide necessary function for generate and combine which is the step 2 (file 2)

import os

import time
import shutil
from cohort import cohort



def generatfromdir(dirpath):
    returnlist={}
    cohortlist = []
    genelist=[]
    g = os.walk(dirpath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            rawfilepath = os.path.join(path, file_name)
            samplenamelist = []
            header = True
            print("start reading " + file_name)
            C = cohort()
            C.addname(file_name)
            with open(rawfilepath, "r") as inputfile:

                for line in inputfile.readlines():
                    if not line.startswith("!"):
                        if header:
                            header=False
                        else:
                            linedata = line.strip().split("\t")
                            if len(linedata)==4:
                                genename = linedata[0].upper()
                                controlvalue = linedata[2]
                                testvalue = linedata[3]

                                # print(genename)
                                if genename not in genelist:
                                    genelist.append(genename)
                                C.addvalue(genename,controlvalue,testvalue)
            cohortlist.append(C)
                            # for i in range(len(samplenamelist)):
    returnlist["cohorts"] = cohortlist
    returnlist["genelist"] = genelist
    return returnlist

def generatfromBigtable(filepath,dirpath):
    # read from dir
    returnlist={}
    cohortlist = []
    genelist=[]
    g = os.walk(dirpath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            rawfilepath = os.path.join(path, file_name)
            samplenamelist = []
            header = True
            print("start reading " + file_name)
            C = cohort()
            C.addname(file_name)
            with open(rawfilepath, "r") as inputfile:

                for line in inputfile.readlines():
                    if not line.startswith("!"):
                        if header:
                            header=False
                        else:
                            linedata = line.strip().split("\t")
                            genename = linedata[0].upper()
                            controlvalue = linedata[2]
                            testvalue = linedata[3]
                            # print(genename)
                            if genename not in genelist:
                                genelist.append(genename)
                            C.addvalue(genename,controlvalue,testvalue)
            cohortlist.append(C)
    # read from big table
    tablecohortlist = []
    title = []
    with open(filepath,"r") as inputfile:
        header = True
        for line in inputfile.readlines():
            if header:
                title = line.strip().split("\t")[1:]
                for i in range(1,(len(title)/2)+1):
                    Cname =  title[2*(i-1)].strip()[:-8]
                    C = cohort()
                    C.addname(Cname)
                    tablecohortlist.append(C)
                header=False
            else:
                linedata=  line.strip().split("\t")
                genename = linedata[0].upper()
                if genename not in genelist:
                    genelist.append(genename)
                genevalue = linedata[1:]
                for i in range(1, (len(title) / 2) + 1):
                    controlvalue = genevalue[2*(i-1)]
                    testvalue = genevalue[2*i-1]
                    tablecohortlist[i].addvalue(genename, controlvalue, testvalue)
    cohortlist = cohortlist+tablecohortlist



    returnlist["cohorts"] = cohortlist
    returnlist["genelist"] = genelist



    return returnlist





def writetable(totalcohortlist,genelist,outputfile):
    with open(outputfile,"w") as outfile:
        printline= "RNA"
        for C in totalcohortlist:
            printline+="\t"+C.getname()+"_control"+"\t"+C.getname()+"_test"
        printline+="\n"
        outfile.write(printline)
        for gene in genelist:
            printline = gene
            for C in totalcohortlist:
                result = C.getvalue(gene)
                printline+="\t"+result["control"]+"\t"+result["test"]
            printline += "\n"
            outfile.write(printline)

def MoveUnparsedToParsed(unparseddir,parseddir):
    files = os.listdir(unparseddir)
    for f in files:
        if not os.path.exists(parseddir+"/" + f):
            shutil.move(unparseddir+"/" + f, parseddir)




# get from outside
# unparsed dir: "./UnparsedDir"
# parsed dir: "./parsedDir"

unparseddir="./UnparsedDir"
parseddir="./parsedDir"

# Totalbigfilename  = CohortTotalTable + time +.txt

Totalbigfilename = "./CohortTotalTable_"
now = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
Totalbigfilename +=now+".txt"





# GenerateOrCombine = "Generate" # "Combine"
#
# if GenerateOrCombine == "Generate":
#     loadresult = generatfromdir(unparseddir)
#     writetable(loadresult["cohorts"], loadresult["genelist"],Totalbigfilename)
#     MoveUnparsedToParsed(unparseddir,parseddir)
#
# # need to find the most recent bigfilename :#error
# if GenerateOrCombine == "Combine":
#     loadresult = generatfromBigtable(Totalbigfilename,unparseddir)
#     writetable(loadresult["cohorts"], loadresult["genelist"], Totalbigfilename)
#     MoveUnparsedToParsed(unparseddir, parseddir)
#

