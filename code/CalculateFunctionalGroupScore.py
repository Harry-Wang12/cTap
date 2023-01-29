#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/12/2020 9:59 PM
# Filename: CalculateFunctionalGroupScore

import os
from ComparisonPair import ComparisonPair
from CalculateModel import CalculateModel
import time


def loadblockinformation(blockdir):
    g = os.walk(blockdir)
    Blocks= []

    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepath = os.path.join(path, file_name)
            blockgenes = {}
            blockgenes["name"] = os.path.basename(filepath)
            blockgenes["id"] = os.path.basename(filepath)
            blockgenes["list"] = []
            for line in open(filepath):
                line = line.strip()
                blockgenes["list"].append(line.upper())
            Blocks.append(blockgenes)
    return  Blocks
# only design for OC right now
def evaluateresult(labelfile,SamplesScore,Blocks,outputfile):
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
    with open(outputfile,"w") as Evaluateresult:
        line = "CohortName\tScore\n"
        Evaluateresult.write(line)
        for Samplename, score in SamplesScore.items():
            line = Samplename+"\t"
            totalScore = 0
            for block in Blocks:
                value = score[block["name"]]["score"]

                if (value >=0.0 and blocklist[block["name"]][score["effect"]] == "positive") or (
                        value <= 0.0 and blocklist[block["name"]][score["effect"]] == "negative"):
                    totalScore += 1
                # elif (value >= 0 and blocklist[block["name"]][score["effect"]] == "positive") or (
                #         value <= 0 and blocklist[block["name"]][score["effect"]] == "negative"):
                #     totalScore += 2




                # if (value >= 0.5 and blocklist[block["name"]][score["effect"]] == "positive") or (
                #         value <= -0.5 and blocklist[block["name"]][score["effect"]] == "negative"):
                #     totalScore += 3
                # elif (value >= 0 and blocklist[block["name"]][score["effect"]] == "positive") or (
                #         value <= 0 and blocklist[block["name"]][score["effect"]] == "negative"):
                #     totalScore += 2
            line+=str(totalScore)+"\n"
            Evaluateresult.write(line)































def readlabelfile(labelfile):
    blocklist = {}
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
    return blocklist




def evaluateresultValue(labelinformation,SamplesScore,Blocks):
#     read file
#     blocklist ={}
#     effectlist=[]
#     with open(labelfile,"r") as labels:
#         header = True
#         for line in labels.readlines():
#             if header:
#                 linedata = line.strip().split("\t")[1:]
#                 effectlist = linedata
#                 header = False
#             else:
#                 linedata = line.strip().split("\t")
#                 blockname = linedata[0]
#                 blocklist[blockname] = {}
#                 sign = linedata[1:]
#                 for i in range(len(sign)):
#                     blocklist[blockname][effectlist[i]] = sign[i]
    returnscore = 0
    for Samplename, score in SamplesScore.items():
        totalScore = 0
        for block in Blocks:
            value = score[block["name"]]["score"]
            if (value >= 0.5 and labelinformation[block["name"]][score["effect"]] == "positive") or (
                    value <= -0.5 and labelinformation[block["name"]][score["effect"]] == "negative"):
                totalScore += 4
            elif (value >= 0 and value < 0.5 and labelinformation[block["name"]][score["effect"]] == "positive") or (
                    value <= 0 and value > -0.5 and labelinformation[block["name"]][score["effect"]] == "negative"):
                totalScore += 3
        returnscore+=totalScore

    return returnscore




# def evaluateresultWithintensity(labelfile,resultdir,Blocks,outputdir,ispart):
#     if not os.path.exists(outputdir):
#         os.mkdir(outputdir)
#
#     blocklist = {}
#     effectlist = []
#     with open(labelfile, "r") as labels:
#         header = True
#         for line in labels.readlines():
#             if header:
#                 linedata = line.strip().split("\t")[1:]
#                 effectlist = linedata
#                 header = False
#             else:
#                 linedata = line.strip().split("\t")
#                 blockname = linedata[0]
#                 blocklist[blockname] = {}
#                 sign = linedata[1:]
#                 for i in range(len(sign)):
#                     blocklist[blockname][effectlist[i]] = sign[i]
#     # readresultdir
#     SamplesScore={}
#     g = os.walk(resultdir)
#     samplelist= []
#     for path, dir_list, file_list in g:
#         for file_name in file_list:
#             filepath = os.path.join(path, file_name)
#
#             if (ispart and "Score" in file_name) or not ispart:
#                 with open(filepath,"r") as scorefile:
#                     header = True
#                     for line in scorefile.readlines():
#                         if header:
#                             linedata = line.strip().split("\t")[1:]
#                             samplelist= linedata
#                             for samplename in linedata:
#                                 SamplesScore[samplename]={}
#                                 if "UP" in samplename:
#                                     SamplesScore[samplename]["effect"] = "OC_up"
#                                 else:
#                                     SamplesScore[samplename]["effect"] = "OC_down"
#                             header=False
#                         else:
#                             linedata =  line.strip().split("\t")
#                             blockname= linedata[0]
#                             linedata = linedata[1:]
#                             for i in range(len(samplelist)):
#                                 SamplesScore[samplelist[i]][blockname] = float(linedata[i])
#                 outputfile = outputdir+filepath.replace("Score","Effectevaluateresult")
#                 returnscore = 0
#                 with open(outputfile,"w") as Evaluateresult:
#                     line = "CohortName\tScore\n"
#                     Evaluateresult.write(line)
#                     for Samplename, score in SamplesScore.items():
#                         line = Samplename+"\t"
#                         totalScore = 0
#                         for block in Blocks:
#                             value = score[block["name"]]
#                             if (value >=0.5 and blocklist[block["name"]][score["effect"]] == "positive") or (value <=-0.5 and blocklist[block["name"]][score["effect"]] == "negative"):
#                                 totalScore+=2
#                             elif (value >=0 and blocklist[block["name"]][score["effect"]] == "positive") or (value <=0 and blocklist[block["name"]][score["effect"]] == "negative"):
#                                 totalScore+=1
#                         line+=str(totalScore)+"\n"
#                         returnscore+=totalScore
#                         Evaluateresult.write(line)
#                 return returnscore
#
















# T=0.25,mi=2,power=0.5,B = 2,W = 2

# def CalculateScore(inputdir,outputfile,outresultdir,Method,Blocks,T="False",mi="False",power="False",B = "False",W = "False"):
#     SamplesScore = {}
#
#     # Paramater Check
#
#     if Method == 1:
#         if T == "False" or mi=="False" or power=="False":
#             print("error paramater input method" + str(Method))
#             return
#
#     elif Method == 2:
#         if T == "False" or W=="False" or B=="False":
#             print("error paramater input method" + str(Method))
#             return
#
#     elif Method == 3:
#         if T == "False" or W=="False" or B=="False":
#             print("error paramater input method" + str(Method))
#             return
#
#
#     M = CalculateModel(Block=Blocks)
#     g = os.walk(inputdir)
#
#
#
#     for path, dir_list, file_list in g:
#         for file_name in file_list:
#             filepath = os.path.join(path, file_name)
#             S = ComparisonPair()
#             S.load(filepath)
#
#             if Method == 0:
#                 S = M.preprocess_0(sample=S)
#             elif Method == 1:
#                 S = M.preprocess_1(sample=S,T=T,mi=mi,power=power)
#             elif Method == 2:
#                 S = M.preprocess_2(sample=S,  W =W,T=T,B=B)
#             elif Method == 3:
#                 S = M.preprocess_3(sample=S, W =W,T=T,B=B)
#             elif Method == 4:
#                 S = M.preprocess_4(sample=S, BM=T,BG=mi,WM=power,WG=B)
#
#             SamplesScore[S.getname()] = M.calculateScoreMatraix(sample=S)
#     evaluateresultfile=outresultdir+"effectevaluateresult_"+str(Method)+"_"+str(T)+"_"+str(mi)+"_"+str(power)+"_"+str(B)+"_"+str(W)+".txt"
#     evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
#
#     with open(outputfile, "w") as file:
#         line = "result"
#
#         for Samplename, score in SamplesScore.items():
#             # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
#             line += "\t"+Samplename+"\t"+Samplename+"_pval"
#             # line += "\t" + Samplename
#         line += "\n"
#         # line = ""
#         for block in Blocks:
#             line += block["name"]
#             for Samplename, score in SamplesScore.items():
#                 # line += "\t" + str(score[block["name"]]["score"])
#                 line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(score[block["name"]]["pval"])
#             line += "\n"
#
#         file.write(line)

def CalculateScorebatch(inputdir, outresultdir, Blocks,Method):


    # Paramater Check

    # if Method == 1:
    #     if T == "False" or mi == "False" or power == "False":
    #         print("error paramater input method" + str(Method))
    #         return
    #
    # elif Method == 2:
    #     if T == "False" or W == "False" or B == "False":
    #         print("error paramater input method" + str(Method))
    #         return
    #
    # elif Method == 3:
    #     if T == "False" or W == "False" or B == "False":
    #         print("error paramater input method" + str(Method))
    #         return

    M = CalculateModel(Block=Blocks)
    g = os.walk(inputdir)
    Slist = []
    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepath = os.path.join(path, file_name)
            S = ComparisonPair()
            S.load(filepath)
            Slist.append(S)
    inputdirtitle = inputdir.split("/")[-1]
    # Methodlist = [0,1,2,3,4]
    # for Method in Methodlist:

    if Method == 0:
        newSlist = Slist

        SamplesScore = {}
        for S in newSlist:
            CP = M.preprocess_0(sample=S)
            SamplesScore[CP.getname()] = M.calculateScoreMatraix(sample=S)
        evaluateresultfile = outresultdir + inputdirtitle + "_Effectevaluateresult_" + str(Method) +".txt"
        outputfile =outresultdir + inputdirtitle  + "_Score_" + str(Method) +".txt"
        evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
        with open(outputfile, "w") as file:
            line = "result"
            for Samplename, score in SamplesScore.items():
                # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
                line += "\t" + Samplename + "\t" + Samplename + "_pval"
                # line += "\t" + Samplename
            line += "\n"
            # line = ""
            for block in Blocks:
                line += block["name"]
                for Samplename, score in SamplesScore.items():
                    # line += "\t" + str(score[block["name"]]["score"])
                    line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(score[block["name"]]["pval"])
                line += "\n"

            file.write(line)
            print("finish" + outputfile)

    elif Method == 1:
        for T in [ 0.25, 0.5, 0.75, 1, 2]:
            for mi in [2,3]:
                    for power in [0.25,0.5,0.75]:
                        newSlist = Slist
                        SamplesScore = {}
                        for S in newSlist:
                            CP = M.preprocess_1(sample=S, T=T, mi=mi, power=power)
                            SamplesScore[CP.getname()] = M.calculateScoreMatraix(sample=CP)
                        evaluateresultfile = outresultdir + inputdirtitle + "_Effectevaluateresult_" + str(Method) + "_" + str(T) + "_" + str(mi) + "_" + str(power) + ".txt"
                        outputfile = outresultdir + inputdirtitle  + "_Score_" + str(Method) + "_" + str(T) + "_" + str(mi) + "_" + str(power) + ".txt"
                        evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
                        with open(outputfile, "w") as file:
                            line = "result"
                            for Samplename, score in SamplesScore.items():
                                # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
                                line += "\t" + Samplename + "\t" + Samplename + "_pval"
                                # line += "\t" + Samplename
                            line += "\n"
                            # line = ""
                            for block in Blocks:
                                line += block["name"]
                                for Samplename, score in SamplesScore.items():
                                    # line += "\t" + str(score[block["name"]]["score"])
                                    line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
                                        score[block["name"]]["pval"])
                                line += "\n"

                            file.write(line)
                        print("finish" + outputfile)

    elif Method == 2:
        for T in [ 0.25, 0.5, 0.75, 1, 2]:
            for B in [ 1, 2, 3]:
                for W in [1.5,2,2.5]:
                        newSlist = Slist
                        SamplesScore = {}
                        for S in newSlist:
                            CP = M.preprocess_2(sample=S, W=W, T=T, B=B)
                            SamplesScore[CP.getname()] = M.calculateScoreMatraix(sample=CP)
                        evaluateresultfile = outresultdir + inputdirtitle + "_Effectevaluateresult_" + str(Method) + "_" + str(T) + "_" + str(B) + "_" + str(W) + ".txt"
                        outputfile = outresultdir + inputdirtitle  + "_Score_" + str(Method) + "_" + str(T) + "_" + str(B) + "_" + str(W) + ".txt"
                        evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
                        with open(outputfile, "w") as file:
                            line = "result"
                            for Samplename, score in SamplesScore.items():
                                # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
                                line += "\t" + Samplename + "\t" + Samplename + "_pval"
                                # line += "\t" + Samplename
                            line += "\n"
                            # line = ""
                            for block in Blocks:
                                line += block["name"]
                                for Samplename, score in SamplesScore.items():
                                    # line += "\t" + str(score[block["name"]]["score"])
                                    line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
                                        score[block["name"]]["pval"])
                                line += "\n"

                            file.write(line)
                        print("finish" + outputfile)



        # S = M.preprocess_2(sample=S, W=W, T=T, B=B)

    elif Method == 3:
        for T in [0.25, 0.5, 0.75, 1, 2]:
            for B in [1, 2, 3]:
                for W in [1.5, 2, 2.5]:
                    newSlist = Slist
                    SamplesScore = {}
                    for S in newSlist:
                        CP = M.preprocess_3(sample=S, W=W, T=T, B=B)
                        SamplesScore[CP.getname()] = M.calculateScoreMatraix(sample=CP)
                    evaluateresultfile = outresultdir + inputdirtitle + "_Effectevaluateresult_" + str(
                        Method) + "_" + str(T) + "_" + str(B) + "_" + str(W) + ".txt"
                    outputfile = outresultdir + inputdirtitle + "_Score_" + str(Method) + "_" + str(T) + "_" + str(
                        B) + "_" + str(W) + ".txt"
                    evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
                    with open(outputfile, "w") as file:
                        line = "result"
                        for Samplename, score in SamplesScore.items():
                            # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
                            line += "\t" + Samplename + "\t" + Samplename + "_pval"
                            # line += "\t" + Samplename
                        line += "\n"
                        # line = ""
                        for block in Blocks:
                            line += block["name"]
                            for Samplename, score in SamplesScore.items():
                                # line += "\t" + str(score[block["name"]]["score"])
                                line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
                                    score[block["name"]]["pval"])
                            line += "\n"

                        file.write(line)
                    print("finish" + outputfile)
    elif Method == 4:
        for BM in [0.5, 0.75,1, 1.5, 2]:
            for BG in [0.5, 0.75,1, 1.5, 2]:
                for WM in [0.5,0.75, 1, 1.5, 2]:
                    for WG in [0.5, 0.75,1, 1.5, 2]:
                        newSlist = Slist
                        SamplesScore = {}
                        for S in newSlist:
                            CP = M.preprocess_4(sample=S, BM=BM, BG=BG, WM=WM, WG=WG)
                            SamplesScore[S.getname()] = M.calculateScoreMatraix(sample=CP)
                        evaluateresultfile = outresultdir + inputdirtitle + "_Effectevaluateresult_" + str(
                            Method) + "_" + str(BM) + "_" + str(BG) + "_" + str(WM)+ "_" + str(WG) + ".txt"
                        outputfile = outresultdir + inputdirtitle + "_Score_" + str(
                            Method) + "_" + str(BM) + "_" + str(BG) + "_" + str(WM)+ "_" + str(WG) + ".txt"
                        evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
                        with open(outputfile, "w") as file:
                            line = "result"
                            for Samplename, score in SamplesScore.items():
                                # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
                                line += "\t" + Samplename + "\t" + Samplename + "_pval"
                                # line += "\t" + Samplename
                            line += "\n"
                            # line = ""
                            for block in Blocks:
                                line += block["name"]
                                for Samplename, score in SamplesScore.items():
                                    # line += "\t" + str(score[block["name"]]["score"])
                                    line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
                                        score[block["name"]]["pval"])
                                line += "\n"

                            file.write(line)
                        print("finish " + outputfile)




                # S = M.preprocess_4(sample=S, BM=T, BG=mi, WM=power, WG=B)







                #
                # SamplesScore[S.getname()] = M.calculateScoreMatraix(sample=S)
    #     evaluateresultfile = outresultdir + inputdir + "effectevaluateresult_" + str(Method) + "_" + str(T) + "_" + str(
    #         mi) + "_" + str(power) + "_" + str(B) + "_" + str(W) + ".txt"
    #     evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
    #
    # with open(outputfile, "w") as file:
    #     line = "result"
    #
    #     for Samplename, score in SamplesScore.items():
    #         # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
    #         line += "\t" + Samplename + "\t" + Samplename + "_pval"
    #         # line += "\t" + Samplename
    #     line += "\n"
    #     # line = ""
    #     for block in Blocks:
    #         line += block["name"]
    #         for Samplename, score in SamplesScore.items():
    #             # line += "\t" + str(score[block["name"]]["score"])
    #             line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(score[block["name"]]["pval"])
    #         line += "\n"
    #
    #     file.write(line)