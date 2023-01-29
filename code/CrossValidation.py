#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/20/2020 11:38 AM
# Filename: CrossValidation

'''
 we try to use CVD to test if the training if good separation
 but I need to find a way to show our separation is correct.
'''

import os

from ComparisonPair import ComparisonPair
from CalculateModel import CalculateModel
import time
import random
from multiprocessing import Process

from os import system

def evaluateCVDresult(labelfile,SamplesScore,Blocks):
#     read file
    blocklist ={}
    effectlist=[]
    with open(labelfile,"r") as labels:
        header = True
        for line in labels.readlines():
            if header:
                linedata = line.strip().split("\t")[1:]
                effectlist = linedata
                header = False
            else:
                linedata = line.strip().split("\t")
                blockname = linedata[0]
                blocklist[blockname] = {}
                sign = linedata[1:]
                for i in range(len(sign)):
                    blocklist[blockname][effectlist[i]] = sign[i]

    for Samplename, score in SamplesScore.items():

        totalScore = 0
        for block in Blocks:
            value = score[block["name"]]["score"]
            if (value >= 0.5 and blocklist[block["name"]][score["effect"]] == "positive") or (
                    value <= -0.5 and blocklist[block["name"]][score["effect"]] == "negative"):
                totalScore += 2
            elif (value >= 0 and blocklist[block["name"]][score["effect"]] == "positive") or (
                    value <= 0 and blocklist[block["name"]][score["effect"]] == "negative"):
                totalScore += 1

    return totalScore


def writesplitresult(outputdir,result):
    print("start write :"+outputdir)
    UPfile = outputdir+"/upgenes.txt"
    with open(UPfile,"w") as outfile:
        line=""
        for genename in result["Active"]:
            line+=genename+"\n"
        outfile.write(line)
    DOWNfile = outputdir + "/downgenes.txt"
    with open(DOWNfile, "w") as outfile:
        line = ""
        for genename in result["Inhibit"]:
            line += genename + "\n"
        outfile.write(line)
    print("finish write :" + outputdir)


def loadsamplefile(sampledir):
    ComparisonParirlist = []

    g = os.walk(sampledir)

    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepath = os.path.join(path, file_name)
            C = ComparisonPair()
            C.load(filepath)
            ComparisonParirlist.append(C)

    return ComparisonParirlist

def writerevisedCPlist(samplelist,Method,M,outputdir,BM, BG, WM, WG):
    print("write: "+outputdir)
    if Method == 4:
        for CP in samplelist:
            CPR = M.preprocess_4(sample=CP, BM=BM, BG=BG, WM=WM, WG=WG)
            CPR.writerevisedresult(outputdir+ "/")
    elif Method == 0:
        for CP in samplelist:
            CPR = M.preprocess_0(sample=CP)
            CPR.writerevisedresult(outputdir + "/")


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

def checktotal(totalresultdir):

    Combine=totalresultdir+"/combine.txt"
    with open(Combine,"w") as combinefile:
        line=""

        for BM in [0.5, 0.75, 1, 1.5]:
            # for BM in [0.75]:
            for BG in [0.5, 0.75, 1, 1.5]:
                # for BG in [0.75]:
                for WM in [0.5, 0.75, 1, 1.5]:
                    for WG in [0.5, 0.75, 1, 1.5]:
                        resultfilepath = totalresultdir + "/CVD_" + str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG)+"/"+ str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG)+"_Analysis.txt"
                        with open(resultfilepath,"r") as resultfile:
                            lines = resultfile.readlines()
                            method0 = int(lines[0].strip().split("\t")[1])
                            method4 = int(lines[1].strip().split("\t")[1])

                            if method4> method0:
                                line+="CVD_" + str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG)+"\tlarge\n"
                                # combinefile.write(line)

                            elif method4== method0:
                                line+="CVD_" + str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG)+"\tequal\n"
        combinefile.write(line)











def CVD(totalresultdir,inputdir,Upeffect,Downeffect,testrate,itertime,M,Blockname,tolerance, BM = 0.5, BG = 0.5,  WM = 0.5, WG = 0.5):
    Gtime=totalresultdir
    title = Gtime + "/CVD_" + str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG)
    if not os.path.exists(title):
        os.mkdir(title)

    Method0score = 0
    Method4score = 0

    for j in range(itertime):


        ComparisonParirlist = loadsamplefile(inputdir)
        upsamplelist=[]
        downsamplelist=[]

        for CP in ComparisonParirlist:
            if CP.geteffect() == Upeffect:
                upsamplelist.append(CP)
            elif CP.geteffect() == Downeffect:
                downsamplelist.append(CP)



        #     separate first
        lenup = upsamplelist.__len__()
        lendown = downsamplelist.__len__()

        testupnumber = int(lenup*((testrate)/100))
        testdownnumber = int(lendown*((testrate)/100))



        indexupList = range(lenup)
        randomupIndex = random.sample(indexupList,testupnumber )
        indexupList = range(lendown)
        randomdownIndex = random.sample(indexupList,testdownnumber)


#         process
        for method in [0,4]:
#         for method in [4]:
            if method == 0:
                ComparisonParirlist = loadsamplefile(inputdir)
                upsamplelist = []
                downsamplelist = []

                for CP in ComparisonParirlist:
                    if CP.geteffect() == Upeffect:
                        upsamplelist.append(CP)
                    elif CP.geteffect() == Downeffect:
                        downsamplelist.append(CP)


                uppositivelist = []
                upnegativelist = []
                downpositivelist = []
                downnegativelist = []

                trainupset = []
                traindownset = []
                testupset = []
                testdownset = []
                for i in range(lenup):
                    if i in randomupIndex:
                        testupset.append(upsamplelist[i])
                    else:
                        trainupset.append(upsamplelist[i])

                for i in range(lendown):
                    if i in randomdownIndex:
                        testdownset.append(downsamplelist[i])
                    else:
                        traindownset.append(downsamplelist[i])

                result = {}
                result["Active"] = []
                result["Inhibit"] = []
                # totoalUPgenelist = {}
                # totoalDOWNgenelist = {}
                # BM = 0.5
                # BG = 0.5
                # WM = 0.5
                # WG = 1.5
                totoalUPgenelist={}
                totoalDOWNgenelist={}


                # process up
                preProcessedlist=[]
                # if method==0:
                for S in trainupset:
                    CP = M.preprocess_0(sample=S)
                    preProcessedlist.append(CP)
                # elif method ==4 :
                #     for S in trainupset:
                #         S = M.preprocess_4(sample=S, BM=BM, BG=BG, WM=WM, WG=WG)
                #         preProcessedlist.append(S)
                # outputfilepath = "./splitresult/" + title + "_targetgenesplit" + "_" + str(Method) + "_" + str(BM) + "_" + str(
                #     BG) + "_" + str(WM) + "_" + str(WG) + ".txt"
                #   block already in C
                Upcasegenevaluelist={}
                for CP in preProcessedlist:
                    genevaluelist = M.getgenefromblock(CP, Blockname)
                    Upcasegenevaluelist[CP.getname()] = genevaluelist

                for samplename, UC in Upcasegenevaluelist.items():
                    for genename, genevalue in UC.items():
                        if genename.upper() not in totoalUPgenelist:
                            totoalUPgenelist[genename.upper()] = []
                            totoalUPgenelist[genename.upper()].append(genevalue)
                        else:
                            totoalUPgenelist[genename.upper()].append(genevalue)
                for genename, genevaluelist in totoalUPgenelist.items():
                    upnumber = 0
                    downnumber = 0
                    for value in genevaluelist:
                        if value > 0:
                            upnumber += 1
                        elif value < 0:
                            downnumber += 1
                    upactuallyrate = upnumber / len(genevaluelist)
                    downactuallyrate = downnumber / len(genevaluelist)
                    expectedrate = (100 - tolerance) / 100

                    if upactuallyrate >= expectedrate:
                        uppositivelist.append(genename.upper())
                    elif downactuallyrate >= expectedrate:
                        upnegativelist.append(genename.upper())

                # process down
                preProcessedlist = []

                for S in traindownset:
                    CP = M.preprocess_0(sample=S)
                    preProcessedlist.append(CP)


                Downcasegenevaluelist = {}
                for CP in preProcessedlist:
                    genevaluelist = M.getgenefromblock(CP, Blockname)
                    Downcasegenevaluelist[CP.getname()] = genevaluelist

                for samplename, UD in Downcasegenevaluelist.items():
                    for genename, genevalue in UD.items():
                        if genename.upper() not in totoalDOWNgenelist:
                            totoalDOWNgenelist[genename.upper()] = []
                            totoalDOWNgenelist[genename.upper()].append(genevalue)
                        else:
                            totoalDOWNgenelist[genename.upper()].append(genevalue)

                for genename, genevaluelist in totoalDOWNgenelist.items():
                    upnumber = 0
                    downnumber = 0
                    for value in genevaluelist:
                        if value > 0:
                            upnumber += 1
                        elif value < 0:
                            downnumber += 1
                    upactuallyrate = upnumber / len(genevaluelist)
                    downactuallyrate = downnumber / len(genevaluelist)
                    expectedrate = (100 - tolerance) / 100

                    if upactuallyrate >= expectedrate:
                        downpositivelist.append(genename.upper())
                    elif downactuallyrate >= expectedrate:
                        downnegativelist.append(genename.upper())


                for gene in uppositivelist:
                    if gene in downnegativelist:
                        result["Active"].append(gene)
                for gene in upnegativelist:
                    if gene in downpositivelist:
                        result["Inhibit"].append(gene)


                outputdir = title + "/" + str(j) + "_" + str(method)
                if not os.path.exists(outputdir):
                    os.mkdir(outputdir)
                # outputfilepath = outputdir + "/trainingset.txt"
                writesplitresult(outputdir, result)



                # new Module with new block
                Blocks = []
                # up
                blockgenes = {}
                blockgenes["name"] = "irf8active.txt"
                blockgenes["id"] = "irf8active.txt"
                blockgenes["list"] = []
                for genename in result["Inhibit"]:
                    blockgenes["list"].append(genename.upper())
                Blocks.append(blockgenes)
                # down
                blockgenes = {}
                blockgenes["name"] = "irf8inhibit.txt"
                blockgenes["id"] = "irf8inhibit.txt"
                blockgenes["list"] = []
                for genename in result["Active"]:
                    blockgenes["list"].append(genename.upper())
                Blocks.append(blockgenes)

                newC = CalculateModel(Block=Blocks)
                SamplesScore = {}
                for CP in testupset:
                    CPR = newC.preprocess_0(sample=CP)
                    SamplesScore[CPR.getname()] = newC.calculateScoreMatraix(sample=CPR)
                    CPR.writerevisedresult(outputdir + "/")
                    # CPR.writerevisedresult("./CVD7-20/CVD_" + str(j) + "/")
                for CP in testdownset:
                    CPR = newC.preprocess_0(sample=CP)
                    SamplesScore[CPR.getname()] = newC.calculateScoreMatraix(sample=CPR)
                    CPR.writerevisedresult(outputdir + "/")

                Method0score += evaluateCVDresult("./effectsign.txt", SamplesScore, Blocks)

                with open(outputdir+"/testresult.txt", "w") as file:
                    line = "result"
                    for Samplename, score in SamplesScore.items():
                        # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
                        # line += "\t" + Samplename + "\t" + Samplename + "_pval"
                        line += "\t" + Samplename
                    line += "\n"
                    # line = ""
                    for block in Blocks:
                        line += block["name"]
                        for Samplename, score in SamplesScore.items():
                            line += "\t" + str(score[block["name"]]["score"])
                            # line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(score[block["name"]]["pval"])
                        line += "\n"
                    file.write(line)
##########################################################################################################################################################################################################



            if method ==4:

                ComparisonParirlist = loadsamplefile(inputdir)
                upsamplelist = []
                downsamplelist = []

                for CP in ComparisonParirlist:
                    if CP.geteffect() == Upeffect:
                        upsamplelist.append(CP)
                    elif CP.geteffect() == Downeffect:
                        downsamplelist.append(CP)

                uppositivelist = []
                upnegativelist = []
                downpositivelist = []
                downnegativelist = []

                trainupset = []
                traindownset = []
                testupset = []
                testdownset = []
                for i in range(lenup):
                    if i in randomupIndex:
                        testupset.append(upsamplelist[i])
                    else:
                        trainupset.append(upsamplelist[i])

                for i in range(lendown):
                    if i in randomdownIndex:
                        testdownset.append(downsamplelist[i])
                    else:
                        traindownset.append(downsamplelist[i])

                result = {}
                result["Active"] = []
                result["Inhibit"] = []
                # totoalUPgenelist = {}
                # totoalDOWNgenelist = {}
                # BM = 0.5
                # BG = 0.5
                # WM = 0.5
                # WG = 0.5
                totoalUPgenelist = {}
                totoalDOWNgenelist = {}

                # process up
                preProcessedlist = []
                for S in trainupset:
                    CP = M.preprocess_4(sample=S, BM=BM, BG=BG, WM=WM, WG=WG)
                    preProcessedlist.append(CP)
                # outputfilepath = "./splitresult/" + title + "_targetgenesplit" + "_" + str(Method) + "_" + str(BM) + "_" + str(
                #     BG) + "_" + str(WM) + "_" + str(WG) + ".txt"
                #   block already in C
                Upcasegenevaluelist = {}
                for CP in preProcessedlist:
                    genevaluelist = M.getgenefromblock(CP, Blockname)
                    Upcasegenevaluelist[CP.getname()] = genevaluelist

                for samplename, UC in Upcasegenevaluelist.items():
                    for genename, genevalue in UC.items():
                        if genename.upper() not in totoalUPgenelist:
                            totoalUPgenelist[genename.upper()] = []
                            totoalUPgenelist[genename.upper()].append(genevalue)
                        else:
                            totoalUPgenelist[genename.upper()].append(genevalue)
                for genename, genevaluelist in totoalUPgenelist.items():
                    upnumber = 0
                    downnumber = 0
                    for value in genevaluelist:
                        if value > 0:
                            upnumber += 1
                        elif value < 0:
                            downnumber += 1
                    upactuallyrate = upnumber / len(genevaluelist)
                    downactuallyrate = downnumber / len(genevaluelist)
                    expectedrate = (100 - tolerance) / 100

                    if upactuallyrate >= expectedrate:
                        uppositivelist.append(genename.upper())
                    elif downactuallyrate >= expectedrate:
                        upnegativelist.append(genename.upper())

                # process down
                preProcessedlist = []
                for S in traindownset:
                    CP= M.preprocess_4(sample=S, BM=BM, BG=BG, WM=WM, WG=WG)
                    preProcessedlist.append(CP)

                Downcasegenevaluelist = {}
                for CP in preProcessedlist:
                    genevaluelist = M.getgenefromblock(CP, Blockname)
                    Downcasegenevaluelist[CP.getname()] = genevaluelist

                for samplename, UD in Downcasegenevaluelist.items():
                    for genename, genevalue in UD.items():
                        if genename.upper() not in totoalDOWNgenelist:
                            totoalDOWNgenelist[genename.upper()] = []
                            totoalDOWNgenelist[genename.upper()].append(genevalue)
                        else:
                            totoalDOWNgenelist[genename.upper()].append(genevalue)

                for genename, genevaluelist in totoalDOWNgenelist.items():
                    upnumber = 0
                    downnumber = 0
                    for value in genevaluelist:
                        if value > 0:
                            upnumber += 1
                        elif value < 0:
                            downnumber += 1
                    upactuallyrate = upnumber / len(genevaluelist)
                    downactuallyrate = downnumber / len(genevaluelist)
                    expectedrate = (100 - tolerance) / 100

                    if upactuallyrate >= expectedrate:
                        downpositivelist.append(genename.upper())
                    elif downactuallyrate >= expectedrate:
                        downnegativelist.append(genename.upper())

                for gene in uppositivelist:
                    if gene in downnegativelist:
                        result["Active"].append(gene)
                for gene in upnegativelist:
                    if gene in downpositivelist:
                        result["Inhibit"].append(gene)

                outputdir = title +"/"+str(j)+"_"+ str(method)
                if not os.path.exists(outputdir):
                    os.mkdir(outputdir)

                writesplitresult(outputdir, result)

                # new Module with new block
                Blocks = []
                # up
                blockgenes = {}
                blockgenes["name"] = "irf8active.txt"
                blockgenes["id"] = "irf8active.txt"
                blockgenes["list"] = []
                for genename in result["Inhibit"]:
                    blockgenes["list"].append(genename.upper())
                Blocks.append(blockgenes)
                # down
                blockgenes = {}
                blockgenes["name"] = "irf8inhibit.txt"
                blockgenes["id"] = "irf8inhibit.txt"
                blockgenes["list"] = []
                for genename in result["Active"]:
                    blockgenes["list"].append(genename.upper())
                Blocks.append(blockgenes)

                newC = CalculateModel(Block=Blocks)

                SamplesScore = {}
                for CP in testupset:
                    CPR = newC.preprocess_4(sample=CP, BM=BM, BG=BG, WM=WM, WG=WG)
                    SamplesScore[CPR.getname()] = newC.calculateScoreMatraix(sample=CPR)
                    CPR.writerevisedresult(outputdir + "/")
                for CP in testdownset:
                    CPR = newC.preprocess_4(sample=CP, BM=BM, BG=BG, WM=WM, WG=WG)
                    SamplesScore[CPR.getname()] = newC.calculateScoreMatraix(sample=CPR)
                    CPR.writerevisedresult(outputdir + "/")

                Method4score += evaluateCVDresult("./effectsign.txt", SamplesScore, Blocks)

                with open(outputdir + "/testresult.txt", "w") as file:
                    line = "result"
                    for Samplename, score in SamplesScore.items():
                        # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
                        # line += "\t" + Samplename + "\t" + Samplename + "_pval"
                        line += "\t" + Samplename
                    line += "\n"
                    # line = ""
                    for block in Blocks:
                        line += block["name"]
                        for Samplename, score in SamplesScore.items():
                            line += "\t" + str(score[block["name"]]["score"])
                            # line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(score[block["name"]]["pval"])
                        line += "\n"
                    file.write(line)
    totalscorefile = title+"/"+ str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG)+"_Analysis.txt"
    with open(totalscorefile,"w") as totalscore:
        totalscore.write("Method0 \t"+ str(Method0score)+"\n"+"Method4 \t"+ str(Method4score)+"\n")









if __name__ == '__main__':


# Method = 0
    targetgenelist = loadtargetgene("./targetgene.txt")


    CModle = CalculateModel(Block=targetgenelist)

    ComparisonParirlist = []
    Cutmethod = "percentage"
    totaldir = "./reviseddata7_21_v5_method3"
    Method=4
    if not os.path.exists(totaldir):
        os.mkdir(totaldir)

    # for B_t in [5,10,15]:
    for B_t in [5]:
        B_b = B_t
        for method in [2]:
            # totalresultdir = "./CVD_7_21_"+str(B_t)+"_"+str(B_b)+"_"+str(method)
            # if not os.path.exists(totalresultdir):
            #     os.mkdir(totalresultdir)
            l = []
            method1_type = "mean"
            inputdir = "./datamaterial/replacedDir_percentage" + "_" + str(B_t) + "_" + str(B_b) + "_" + str(
                method) + "_" + str(method1_type)
            ComparisonParirlist = loadsamplefile(inputdir)
            for BM in [0.1]:
            # for BM in [0.2,0.3,0.4,0.5,0.6]:
            # for BM in [0.7,0.8,0.9]:
            # for BM in [1,1.1,1.2]:
            # for BM in [1.3,1.4,1.5]:
            #     for BM in [ 0.75]:
                for BG in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]:
                    # for BG in [0.75]:
                    for WM in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]:
                        for WG in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5]:
                            outputfile = totaldir+"/revised"+"_" + str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG)+"/"
                            if not os.path.exists(outputfile):
                                os.mkdir(outputfile)
                            p = Process(target=writerevisedCPlist, args=(ComparisonParirlist,Method,CModle,outputfile,BM,BG,WM,WG))
                            p.start()
                            l.append(p)
            #                 writerevisedCPlist(ComparisonParirlist,CModle,outputfile,BM,BG,WM,WG)
            #                 print("finish writing: "+outputfile)
            # # Upeffect="OC_up"
            # Downeffect="OC_down"
            # upsamplelist=[]
            # downsamplelist=[]
    Method=0
    inputdir = "./parsedDir/"
    ComparisonParirlist = loadsamplefile(inputdir)
    outputfile = totaldir+"/parsedDir/"
    if not os.path.exists(outputfile):
        os.mkdir(outputfile)
    writerevisedCPlist(ComparisonParirlist,Method, CModle, outputfile, 1, 1, 1, 1)
    # p = Process(target=writerevisedCPlist, args=(ComparisonParirlist,Method, CModle, outputfile, 1, 1, 1, 1))
    # p.start()
    # l.append(p)

            # for CP in ComparisonParirlist:
            #     if CP.geteffect() == Upeffect:
            #         upsamplelist.append(CP)
            #     elif CP.geteffect() == Downeffect:
            #         downsamplelist.append(CP)
            #
            # for BM in [0.5,0.75, 1, 1.5]:
            # # for BM in [0.75]:
            #     for BG in [0.5,0.75, 1, 1.5]:
            #     # for BG in [0.75]:
            #         for WM in [0.5,0.75, 1, 1.5]:
            #         # for WM in [0.5]:
            #             for WG in [0.5,0.75, 1, 1.5]:
            #             # for WG in [0.5]:
            #             # WG = 0.5
            #                 p = Process(target=CVD, args=(totalresultdir,inputdir,Upeffect,Downeffect, 25, 5, CModle, "OC", 0, BM, BG, WM,WG))
            #                 p.start()
            #                 l.append(p)
            #                 # CVD(inputdir,Upeffect,Downeffect, testrate=25, itertime=5, M = CModle, Blockname="OC", tolerance=0,BM=BM, BG=BG, WM=WM, WG=WG)
            #
            #
    # for p in l :
    #     p.join()
            # checktotal(totalresultdir)

