#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:how17003
# datetime:7/13/2020 8:39 PM
# Filename: FigureOutGene

import os

from ComparisonPair import ComparisonPair
from CalculateModel import CalculateModel
import time
import random
import scipy.stats
from multiprocessing import Process


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

# def writesplitresult(fileoutput,result,samplegenedict):
#     print("start write :"+fileoutput)
#     with open(fileoutput,"w") as outfile:
#         line = "Active"
#         for genename in result["Active"]:
#             line+="\t"+genename
#         line+="\nInhibit"
#         for genename in result["Inhibit"]:
#             line+="\t"+genename
#         line += "\n"
#         outfile.write(line)
#         # for samplename, UC in samplegenedict.items():
#         #     line = samplename
#         #     for genename, genevalue in UC.items():
#         #         line+="\t"+genename+":"+str(genevalue)
#         #     line+="\n"
#         #     outfile.write(line)
#
#     print("finish write :" + fileoutput)



def writesplitresult(fileoutput,result):
    UPpositivefile = fileoutput + "_UP.txt"
    print("start write :"+fileoutput)
    with open(UPpositivefile, "w") as outfile:
        line=""
        number = 0
        for genename in result["Active"]:
            # number += 1
            # line += genename + "\n"
            line += genename +"\n"
        outfile.write(line)
    DOWNpositivefile = fileoutput + "_DOWN.txt"
    with open(DOWNpositivefile, "w") as outfile:
        line = ""
        number = 0
        for genename in result["Inhibit"]:
            number += 1
            line += genename + "\n"
            # line += genename + ": " + str(Pval) + "\n"
        outfile.write(line)


    # UPpositivefile = fileoutput+"_UPpositivegenes.txt"
    # with open(UPpositivefile,"w") as outfile:
    #     line=""
    #     number = 0
    #     for genename, Pval in result["UPActive"].items():
    #         number += 1
    #         # line += genename + "\n"
    #         line += genename + ": " + str(Pval) + "\n"
    #     outfile.write(line.strip()[:-1])
    # UPneagtiveefile = fileoutput + "_UPneagtivegenes.txt"
    # with open(UPneagtiveefile, "w") as outfile:
    #     line = ""
    #     number = 0
    #     for genename, Pval in result["UPInhibit"].items():
    #         number += 1
    #         # line += genename + "\n"
    #         line += genename + ": "+str(Pval)+"\n"
    #     outfile.write(line.strip()[:-1])
    # DOWNpositivefile = fileoutput + "_DOWNpositivegenes.txt"
    # with open(DOWNpositivefile, "w") as outfile:
    #     line = ""
    #     number = 0
    #     for genename, Pval in result["DOWNActive"].items():
    #         number += 1
    #         # line += genename + "\n"
    #         line += genename + ": " + str(Pval) + "\n"
    #     outfile.write(line.strip()[:-1])
    # print("finish write :" + fileoutput)
    # DOWNnegativefile = fileoutput + "_DOWNnegativegenes.txt"
    # with open(DOWNnegativefile, "w") as outfile:
    #     line = ""
    #
    #     for genename, Pval in result["DOWNInhibit"].items():
    #         number+=1
    #         # line += genename + "\n"
    #         line += genename + ": "+str(Pval)+"\n"
    #
    #     outfile.write(line.strip()[:-1])
    print("finish write :" + fileoutput)

def splitgene(targetgene,CPlist,unsplitgenelist,Upeffect,Downeffect,outfilepath,tolerance):
    result = {}
    result["Inhibit"] = []
    # result["UPInhibit"] = {}
    # result["DOWNActive"] = {}
    result["Active"] = []
#################################################################################################################################################
    # for gene in unsplitgenelist[0]["list"]:
    #     up = 0
    #     down = 0
    #     for CP in CPlist:
    #         targetratio = CP.getratioValue(targetgene.upper())
    #         generatio = CP.getratioValue(gene.upper())
    #         if targetratio * generatio > 0:
    #             up+=1
    #         elif targetratio * generatio < 0:
    #             down+=1
    #         # elif targetratio * generatio == 0:
    #         #     down+=1
    #         #     up += 1
    #     # print(up + down)
    #     # print(gene)
    #     if (up + down) >0:
    #         if (up/(up+down))>= ((100-tolerance)/100):
    #             result["Active"].append(gene.upper())
    #         elif (down/(up+down)) >= ((100-tolerance)/100):
    #             result["Inhibit"].append(gene.upper())
    # writesplitresult(outfilepath, result)
######################################################################################################################################################
    # Upcasegenevaluelist = {}
    # Downcasegenevaluelist = {}
    # uppositivelist=[]
    # downnegativelist=[]
    # upnegativelist=[]
    # downpositivelist=[]
    # for CP in CPlist:
    #     if CP.geteffect() == Upeffect:
    #         genevaluelist = {}
    #         for genename in unsplitgenelist[0]["list"]:
    #             genevaluelist[genename.upper()] = CP.getratioValue(genename.upper())
    #         Upcasegenevaluelist[CP.getname()] = genevaluelist
    #
    #     elif CP.geteffect() == Downeffect:
    #         genevaluelist = {}
    #         for genename in unsplitgenelist[0]["list"]:
    #             genevaluelist[genename.upper()] = CP.getratioValue(genename.upper())
    #         Downcasegenevaluelist[CP.getname()] = genevaluelist
    #
    # totoalUPgenelist = {}
    # for samplename, UC in Upcasegenevaluelist.items():
    #     for genename, genevalue in UC.items():
    #         if genename.upper() not in totoalUPgenelist:
    #             totoalUPgenelist[genename.upper()] = []
    #             totoalUPgenelist[genename.upper()].append(genevalue)
    #         else:
    #             totoalUPgenelist[genename.upper()].append(genevalue)
    # # analysis
    # for genename, genevaluelist in totoalUPgenelist.items():
    #     upnumber = 0
    #     downnumber = 0
    #
    #     for value in genevaluelist:
    #         if value >=0:
    #             upnumber += 1
    #         elif value <=0:
    #             downnumber += 1
    #     upactuallyrate = upnumber / len(genevaluelist)
    #     downactuallyrate = downnumber / len(genevaluelist)
    #     expectedrate = (100 - tolerance) / 100
    #
    #     if upactuallyrate > expectedrate:
    #         # stat,Pval =scipy.stats.mannwhitneyu(genevaluelist,[0,0,0,0,0],alternative="greater")
    #         # result["UPActive"][genename.upper()] = round(Pval,6)
    #         uppositivelist.append(genename.upper())
    #
    #     elif downactuallyrate > expectedrate:
    #         # stat,Pval = scipy.stats.mannwhitneyu(genevaluelist, [0,0,0,0,0], alternative="less")
    #         # result["UPInhibit"][genename.upper()] = round(Pval,6)
    #         upnegativelist.append(genename.upper())
    # # result["UPActive"] = dict(sorted(result["UPActive"].items(),key=lambda obj:obj[1]))
    # # result["UPInhibit"] = dict(sorted(result["UPInhibit"].items(), key=lambda obj: obj[1]))
    # #     we check with in one up and down first then cross effect
    # totoalDOWNgenelist = {}
    # for samplename, UD in Downcasegenevaluelist.items():
    #     for genename, genevalue in UD.items():
    #         if genename.upper() not in totoalDOWNgenelist:
    #             totoalDOWNgenelist[genename.upper()] = []
    #             totoalDOWNgenelist[genename.upper()].append(genevalue)
    #         else:
    #             totoalDOWNgenelist[genename.upper()].append(genevalue)
    # # analysis
    # for genename, genevaluelist in totoalDOWNgenelist.items():
    #     upnumber = 0
    #     downnumber = 0
    #
    #     for value in genevaluelist:
    #         if value >= 0:
    #             upnumber += 1
    #         elif value <= 0:
    #             downnumber += 1
    #
    #     upactuallyrate = upnumber / len(genevaluelist)
    #     downactuallyrate = downnumber / len(genevaluelist)
    #     expectedrate = (100 - tolerance) / 100
    #
    #     if upactuallyrate > expectedrate:
    #         # stat,Pval = scipy.stats.mannwhitneyu(genevaluelist, [0,0,0,0,0], alternative="greater")
    #         # result["DOWNActive"][genename.upper()] = round(Pval,5)
    #         downpositivelist.append(genename.upper())
    #     elif downactuallyrate > expectedrate:
    #         # stat,Pval = scipy.stats.mannwhitneyu(genevaluelist, [0,0,0,0,0], alternative="less")
    #         # result["DOWNInhibit"][genename.upper()] = round(Pval,6)
    #         downnegativelist.append(genename.upper())
    # # result["DOWNActive"] = dict(sorted(result["DOWNActive"].items(), key=lambda obj: obj[1]))
    # # result["DOWNInhibit"] = dict(sorted(result["DOWNInhibit"].items(), key=lambda obj: obj[1]))
    # #         cross the different effect
    # # uppositivelist vs downnegativelist
    # # upnegativelist vs downpositivelist
    #
    # for gene in uppositivelist:
    #     if gene in downnegativelist:
    #         result["Active"].append(gene)
    # for gene in upnegativelist:
    #     if gene in downpositivelist:
    #         result["Inhibit"].append(gene)
    #         # result1["Inhibit"] = []
    # writesplitresult(outfilepath, result)
    ######################################################################################################################################################
    resultlist={}
    for genename in unsplitgenelist[0]["list"]:
        if genename.upper() not in resultlist:
            resultlist[genename.upper()]={}
            resultlist[genename.upper()]["same"] = 0
            resultlist[genename.upper()]["dif"] = 0
            for CP in CPlist:
                genevalue = CP.getratioValue(genename.upper())
                targetgenevalue = CP.getratioValue(targetgene.upper())
                if (targetgenevalue * genevalue) >0:
                    resultlist[genename.upper()]["same"]+=1
                elif (targetgenevalue * genevalue) <0:
                    resultlist[genename.upper()]["dif"] += 1

            if ((resultlist[genename.upper()]["same"])/len(CPlist) )>=((100 - tolerance) / 100):
                result["Active"].append(genename.upper())
            if ((resultlist[genename.upper()]["dif"]) / len(CPlist))>= ((100 - tolerance) / 100):
                result["Inhibit"].append(genename.upper())
    writesplitresult(outfilepath, result)
    return result


def calculatePvalue(CPlist,splistresult,tolerance,iteration = 100000000,upeffect = "OC_up",downeffect = "OC_down"):
    randomscore = []
    Upnumber = 0
    Downnumber = 0
    # analysis the number of up and down in Cplist
    for CP in CPlist:
        if CP.geteffect() == upeffect:
            Upnumber+=1
        elif CP.geteffect() == downeffect:
            Downnumber+=1
    with open("./randomScore.txt", "w") as randomScorefile:
        for i in range(iteration):
            UpCPs = []
            DownCps = []
            # generate UP Case:
            for j in range(Upnumber):
                CPR = {}
                for genename in splistresult["Active"]:
                    CPR[genename] = random.randint(-10,10)
                for genename in splistresult["Inhibit"]:
                    CPR[genename] = random.randint(-10,10)
                UpCPs.append(CPR)
            for j in range(Downnumber):
                CPR = {}
                for genename in splistresult["Active"]:
                    CPR[genename] = random.randint(-10,10)
                for genename in splistresult["Inhibit"]:
                    CPR[genename] = random.randint(-10,10)
                DownCps.append(CPR)

            ACTIVEvalue = 0
            for genename in splitresult["Active"]:
                geneUPeffectvaluelist = []
                geneDOWNeffectvaluelist = []
                for CP in UpCPs:
                    geneUPeffectvaluelist.append(CP[genename])
                for CP in DownCps:
                    geneDOWNeffectvaluelist.append(CP[genename])

                uperrorsample = 0
                for value in geneUPeffectvaluelist:
                    if value <0:
                        uperrorsample+=1
                if (uperrorsample/len(geneUPeffectvaluelist)) > (tolerance/100):
                    continue

                downerrorsample = 0
                for value in geneDOWNeffectvaluelist:
                    if value >0:
                        downerrorsample += 1
                if (downerrorsample/len(geneDOWNeffectvaluelist)) > (tolerance/100):
                    continue
                ACTIVEvalue+=1

            INHIBITvalue = 0
            for genename in splitresult["Inhibit"]:
                geneUPeffectvaluelist = []
                geneDOWNeffectvaluelist = []
                for CP in UpCPs:
                    geneUPeffectvaluelist.append(CP[genename])
                for CP in DownCps:
                    geneDOWNeffectvaluelist.append(CP[genename])

                uperrorsample = 0
                for value in geneUPeffectvaluelist:
                    if value >0:
                        uperrorsample += 1
                if (uperrorsample / len(geneUPeffectvaluelist)) > (tolerance / 100):
                    continue

                downerrorsample = 0
                for value in geneDOWNeffectvaluelist:
                    if value <0:
                        downerrorsample += 1
                if (downerrorsample / len(geneDOWNeffectvaluelist)) > (tolerance / 100):
                    continue
                INHIBITvalue += 1
            totoalvalue= (ACTIVEvalue+INHIBITvalue)/(len( splitresult["Active"])+len( splitresult["Inhibit"]))
            randomScorefile.write(str(totoalvalue)+"\n")
            randomscore.append(totoalvalue)
    # print(len(randomscore))
    kde = scipy.stats.gaussian_kde(randomscore, bw_method=0.01)
    pval = kde.integrate_box_1d(value, 1.0)
    if pval > 0.5:
        pval = 1 - pval
    return pval


def CalculateResivedRatio(title,M, CPlist, Method, Upeffect, Downeffect,Blockname,tolerance):
    time1 = time.time()


    if Method == 0:
        newSlist = CPlist
        preProcessedlist = []
        Upcasegenevaluelist = {}
        Downcasegenevaluelist = {}
        uppositivelist = []
        upnegativelist = []
        downpositivelist = []
        downnegativelist = []
        result = {}
        result["Active"] = []
        result["Inhibit"] = []
        for S in newSlist:
            S = M.preprocess_0(sample=S)
            preProcessedlist.append(S)

        outputfilepath = "./splitresult/"+title+"_targetgenesplit_0.txt"
        totalgeneblock={}
        #   block already in C
        for CP in preProcessedlist:
            if CP.geteffect() == Upeffect:
                genevaluelist = M.getgenefromblock(CP, Blockname)
                Upcasegenevaluelist[CP.getname()] = genevaluelist
                totalgeneblock[CP.getname()] = genevaluelist
            elif CP.geteffect() == Downeffect:
                genevaluelist = M.getgenefromblock(CP, Blockname)
                Downcasegenevaluelist[CP.getname()] = genevaluelist
                totalgeneblock[CP.getname()] = genevaluelist

        #     we check with in one up and down first then cross effect
        totoalUPgenelist = {}
        for samplename,UC in Upcasegenevaluelist.items():
            for genename,genevalue in UC.items():
                if genename.upper() not in totoalUPgenelist:
                    totoalUPgenelist[genename.upper()]=[]
                    totoalUPgenelist[genename.upper()].append(genevalue)
                else:
                    totoalUPgenelist[genename.upper()].append(genevalue)
        # analysis
        for genename,genevaluelist in totoalUPgenelist.items():
            upnumber = 0
            downnumber = 0
            for value in genevaluelist:
                if value>0:
                    upnumber+=1
                elif value <0:
                    downnumber+=1
            upactuallyrate = upnumber / len(genevaluelist)
            downactuallyrate = downnumber / len(genevaluelist)
            expectedrate = (100-tolerance)/100

            if upactuallyrate >= expectedrate:
                uppositivelist.append(genename.upper())
            elif downactuallyrate >= expectedrate:
                upnegativelist.append(genename.upper())

        #     we check with in one up and down first then cross effect
        totoalDOWNgenelist = {}
        for samplename,UD in Downcasegenevaluelist.items():
            for genename, genevalue in UD.items():
                if genename.upper() not in totoalDOWNgenelist:
                    totoalDOWNgenelist[genename.upper()] = []
                    totoalDOWNgenelist[genename.upper()].append(genevalue)
                else:
                    totoalDOWNgenelist[genename.upper()].append(genevalue)
        # analysis
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

#         cross the different effect
        # uppositivelist vs downnegativelist
        # upnegativelist vs downpositivelist

        for gene in uppositivelist:
            if gene in downnegativelist:
                result["Active"] .append(gene)
        for gene in upnegativelist:
            if gene in downpositivelist:
                result["Inhibit"].append(gene)
                # result1["Inhibit"] = []
        writesplitresult(outputfilepath,result)
        time2 = time.time()
        print("Finish writting " + outputfilepath + " spend " + str(time2 - time1) + "s")
    elif Method == 1:
        for T in [0.25, 0.5, 0.75, 1, 2]:
            for mi in [2, 3]:
                for power in [0.25, 0.5, 0.75]:
                    newSlist = CPlist
                    preProcessedlist = []
                    Upcasegenevaluelist = {}
                    Downcasegenevaluelist = {}
                    uppositivelist = []
                    upnegativelist = []
                    downpositivelist = []
                    downnegativelist = []
                    result = {}
                    result["Active"] = []
                    result["Inhibit"] = []

                    for S in newSlist:
                        S = M.preprocess_1(sample=S, T=T, mi=mi, power=power)
                        preProcessedlist.append(S)

                    outputfilepath = "./splitresult/" + title + "_targetgenesplit"+ "_" + str(Method)+"_"+str(T)+"_"+str(mi)+"_"+str(power)+".txt"
                    #   block already in C
                    totalgeneblock = {}
                    #   block already in C
                    for CP in preProcessedlist:
                        if CP.geteffect() == Upeffect:
                            genevaluelist = M.getgenefromblock(CP, Blockname)
                            Upcasegenevaluelist[CP.getname()] = genevaluelist
                            totalgeneblock[CP.getname()] = genevaluelist
                        elif CP.geteffect() == Downeffect:
                            genevaluelist = M.getgenefromblock(CP, Blockname)
                            Downcasegenevaluelist[CP.getname()] = genevaluelist
                            totalgeneblock[CP.getname()] = genevaluelist

                    #     we check with in one up and down first then cross effect
                    totoalUPgenelist = {}
                    for samplename,UC in Upcasegenevaluelist.items():
                        for genename, genevalue in UC.items():
                            if genename.upper() not in totoalUPgenelist:
                                totoalUPgenelist[genename.upper()] = []
                                totoalUPgenelist[genename.upper()].append(genevalue)
                            else:
                                totoalUPgenelist[genename.upper()].append(genevalue)
                    # analysis
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

                    #     we check with in one up and down first then cross effect
                    totoalDOWNgenelist = {}
                    for samplename,UD in Downcasegenevaluelist.items():
                        for genename, genevalue in UD.items():
                            if genename.upper() not in totoalDOWNgenelist:
                                totoalDOWNgenelist[genename.upper()] = []
                                totoalDOWNgenelist[genename.upper()].append(genevalue)
                            else:
                                totoalDOWNgenelist[genename.upper()].append(genevalue)
                    # analysis
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

                    #         cross the different effect
                    # uppositivelist vs downnegativelist
                    # upnegativelist vs downpositivelist

                    for gene in uppositivelist:
                        if gene in downnegativelist:
                            result["Active"].append(gene)
                    for gene in upnegativelist:
                        if gene in downpositivelist:
                            result["Inhibit"].append(gene)
                            # result1["Inhibit"] = []
                    writesplitresult(outputfilepath, result)
                    time2 = time.time()
                    print("Finish writting " + outputfilepath + " spend " + str(time2 - time1) + "s")


    elif Method == 2:
        for T in [0.25, 0.5, 0.75, 1, 2]:
            for B in [1, 2, 3]:
                for W in [1.5, 2, 2.5]:
                    newSlist = CPlist
                    preProcessedlist = []
                    Upcasegenevaluelist = {}
                    Downcasegenevaluelist = {}
                    uppositivelist = []
                    upnegativelist = []
                    downpositivelist = []
                    downnegativelist = []
                    result = {}
                    result["Active"] = []
                    result["Inhibit"] = []

                    for S in preProcessedlist:
                        S = M.preprocess_2(sample=S, W=W, T=T, B=B)
                        preProcessedlist.append(S)
                    outputfilepath = "./splitresult/" + title + "_targetgenesplit"  + "_" + str(Method) + "_" + str(T) + "_" + str(B) + "_" + str(W) + ".txt"
                    #   block already in C
                    totalgeneblock = {}
                    #   block already in C
                    for CP in newSlist:
                        if CP.geteffect() == Upeffect:
                            genevaluelist = M.getgenefromblock(CP, Blockname)
                            Upcasegenevaluelist[CP.getname()] = genevaluelist
                            totalgeneblock[CP.getname()] = genevaluelist
                        elif CP.geteffect() == Downeffect:
                            genevaluelist = M.getgenefromblock(CP, Blockname)
                            Downcasegenevaluelist[CP.getname()] = genevaluelist
                            totalgeneblock[CP.getname()] = genevaluelist

                    #     we check with in one up and down first then cross effect
                    totoalUPgenelist = {}
                    for samplename,UC in Upcasegenevaluelist.items():
                        for genename, genevalue in UC.items():
                            if genename.upper() not in totoalUPgenelist:
                                totoalUPgenelist[genename.upper()] = []
                                totoalUPgenelist[genename.upper()].append(genevalue)
                            else:
                                totoalUPgenelist[genename.upper()].append(genevalue)
                    # analysis
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

                    #     we check with in one up and down first then cross effect
                    totoalDOWNgenelist = {}
                    for samplename,UD in Downcasegenevaluelist.items():
                        for genename, genevalue in UD.items():
                            if genename.upper() not in totoalDOWNgenelist:
                                totoalDOWNgenelist[genename.upper()] = []
                                totoalDOWNgenelist[genename.upper()].append(genevalue)
                            else:
                                totoalDOWNgenelist[genename.upper()].append(genevalue)
                    # analysis
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

                    #         cross the different effect
                    # uppositivelist vs downnegativelist
                    # upnegativelist vs downpositivelist

                    for gene in uppositivelist:
                        if gene in downnegativelist:
                            result["Active"].append(gene)
                    for gene in upnegativelist:
                        if gene in downpositivelist:
                            result["Inhibit"].append(gene)
                            # result1["Inhibit"] = []
                    writesplitresult(outputfilepath, result)
                    time2 = time.time()
                    print("Finish writting " + outputfilepath + " spend " + str(time2 - time1) + "s")


    elif Method == 3:

        for T in [0.25, 0.5, 0.75, 1, 2]:
            for B in [1, 2, 3]:
                for W in [1.5, 2, 2.5]:
                    newSlist = CPlist
                    preProcessedlist = []
                    Upcasegenevaluelist = {}
                    Downcasegenevaluelist = {}
                    uppositivelist = []
                    upnegativelist = []
                    downpositivelist = []
                    downnegativelist = []
                    result = {}
                    result["Active"] = []
                    result["Inhibit"] = []
                    for S in newSlist:
                        S = M.preprocess_3(sample=S, W=W, T=T, B=B)
                        preProcessedlist.append(S)
                    outputfilepath = "./splitresult/" + title + "_targetgenesplit" + "_" + str(Method) + "_" + str(T) + "_" + str(B) + "_" + str(W) + ".txt"
                    #   block already in C
                    totalgeneblock = {}
                    #   block already in C
                    for CP in preProcessedlist:
                        if CP.geteffect() == Upeffect:
                            genevaluelist = M.getgenefromblock(CP, Blockname)
                            Upcasegenevaluelist[CP.getname()] = genevaluelist
                            totalgeneblock[CP.getname()] = genevaluelist
                        elif CP.geteffect() == Downeffect:
                            genevaluelist = M.getgenefromblock(CP, Blockname)
                            Downcasegenevaluelist[CP.getname()] = genevaluelist
                            totalgeneblock[CP.getname()] = genevaluelist
                    #     we check with in one up and down first then cross effect
                    totoalUPgenelist = {}
                    for samplename,UC in Upcasegenevaluelist.items():
                        for genename, genevalue in UC.items():
                            if genename.upper() not in totoalUPgenelist:
                                totoalUPgenelist[genename.upper()] = []
                                totoalUPgenelist[genename.upper()].append(genevalue)
                            else:
                                totoalUPgenelist[genename.upper()].append(genevalue)
                    # analysis
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

                    #     we check with in one up and down first then cross effect
                    totoalDOWNgenelist = {}
                    for samplename, UD in Downcasegenevaluelist.items():
                        for genename, genevalue in UD.items():
                            if genename.upper() not in totoalDOWNgenelist:
                                totoalDOWNgenelist[genename.upper()] = []
                                totoalDOWNgenelist[genename.upper()].append(genevalue)
                            else:
                                totoalDOWNgenelist[genename.upper()].append(genevalue)
                    # analysis
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

                    #         cross the different effect
                    # uppositivelist vs downnegativelist
                    # upnegativelist vs downpositivelist

                    for gene in uppositivelist:
                        if gene in downnegativelist:
                            result["Active"].append(gene)
                    for gene in upnegativelist:
                        if gene in downpositivelist:
                            result["Inhibit"].append(gene)
                            # result1["Inhibit"] = []
                    writesplitresult(outputfilepath, result)
                    time2 = time.time()
                    print("Finish writting " + outputfilepath + " spend " + str(time2 - time1) + "s")

    elif Method == 4:
        for BM in [0.5]:
            for BG in [0.5]:
                for WM in [0.5]:
                    for WG in [1.5]:
                        newSlist = CPlist
                        preProcessedlist = []
                        Upcasegenevaluelist = {}
                        Downcasegenevaluelist = {}
                        uppositivelist = []
                        upnegativelist = []
                        downpositivelist = []
                        downnegativelist = []
                        result = {}
                        result["Active"] = []
                        result["Inhibit"] = []
                        totoalUPgenelist = {}
                        totoalDOWNgenelist = {}

                        for S in newSlist:
                            S = M.preprocess_4(sample=S, BM=BM, BG=BG, WM=WM, WG=WG)
                            preProcessedlist.append(S)
                        outputfilepath = "./splitresult/" + title + "_targetgenesplit"+ "_" + str(Method) + "_" + str(BM)+ "_" + str(BG) + "_" + str(WM) + "_" + str(WG) + ".txt"
                        #   block already in C
                        totalgeneblock = {}
                        #   block already in C
                        for CP in preProcessedlist:
                            if CP.geteffect() == Upeffect:
                                genevaluelist = M.getgenefromblock(CP, Blockname)
                                Upcasegenevaluelist[CP.getname()] = genevaluelist
                                totalgeneblock[CP.getname()] = genevaluelist
                            elif CP.geteffect() == Downeffect:
                                genevaluelist = M.getgenefromblock(CP, Blockname)
                                Downcasegenevaluelist[CP.getname()] = genevaluelist
                                totalgeneblock[CP.getname()] = genevaluelist

                        #     we check with in one up and down first then cross effect

                        for samplename,UC in Upcasegenevaluelist.items():
                            for genename, genevalue in UC.items():
                                if genename.upper() not in totoalUPgenelist:
                                    totoalUPgenelist[genename.upper()] = []
                                    totoalUPgenelist[genename.upper()].append(genevalue)
                                else:
                                    totoalUPgenelist[genename.upper()].append(genevalue)
                        # analysis
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

                        #     we check with in one up and down first then cross effect

                        for samplename,UD in Downcasegenevaluelist.items():
                            for genename, genevalue in UD.items():
                                if genename.upper() not in totoalDOWNgenelist:
                                    totoalDOWNgenelist[genename.upper()] = []
                                    totoalDOWNgenelist[genename.upper()].append(genevalue)
                                else:
                                    totoalDOWNgenelist[genename.upper()].append(genevalue)
                        # analysis
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

                        #         cross the different effect
                        # uppositivelist vs downnegativelist
                        # upnegativelist vs downpositivelist

                        for gene in uppositivelist:
                            if gene in downnegativelist:
                                result["Active"].append(gene)
                        for gene in upnegativelist:
                            if gene in downpositivelist:
                                result["Inhibit"].append(gene)
                                # result1["Inhibit"] = []
                        writesplitresult(outputfilepath, result)
                        time2= time.time()
                        print("Finish writting "+ outputfilepath+" spend "+str(time2-time1)+"s")



if __name__ == '__main__':
    # Method =4
    targetgenelist = loadtargetgene("./journalresult/proteial/NFATC1targetEncode.txt")
    l = []
    tolerance = 20

    CModle = CalculateModel(Block=targetgenelist)
    targetgene = "NFATC1"
    # CPlist = loadsamplefile("E:/reviseddata7_27_method3_v6/SVM")
    # splitresult = splitgene(CPlist, targetgenelist, "OC_up", "OC_down", "./SVMsplit", 20)
    # CPlist = loadsamplefile("E:/reviseddata7_27_method3_v6/revised_0_0_0_0_0_0")
    # splitresult = splitgene(CPlist, targetgenelist, "OC_up", "OC_down", "./baselinesplit", 20)
    # CPlist = loadsamplefile("C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0.5_0.25_0.15_0.5_1.25_0.2_4")
    # # splitresult = splitgene(targetgene, CPlist, targetgenelist,"C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0.5_0.275_0.1_0.55_1.5_0.2_4/split",tolerance)
    # splitresult = splitgene(targetgene,CPlist, targetgenelist,"OC_up", "OC_down","C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0.5_0.25_0.15_0.5_1.25_0.2_4/split",tolerance)
    #
    # CPlist = loadsamplefile("C:/wamp64/www/gse_process/ExploreZscore/paperresult/svmRevisedCPprime")
    # # splitresult = splitgene(targetgene,CPlist, targetgenelist, "C:/wamp64/www/gse_process/ExploreZscore/paperresult/svmRevisedCPprime/split", tolerance)
    # splitresult = splitgene(targetgene,CPlist, targetgenelist,"OC_up", "OC_down", "C:/wamp64/www/gse_process/ExploreZscore/paperresult/svmRevisedCPprime/split", tolerance)
    #
    # CPlist = loadsamplefile("C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0_0_0_0_0_0_0")
    # # splitresult = splitgene(targetgene, CPlist, targetgenelist,"C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0_0_0_0_0_0_0/split", tolerance)
    # splitresult = splitgene(targetgene,CPlist, targetgenelist,"OC_up", "OC_down","C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0_0_0_0_0_0_0/split", tolerance)

    # for inputdirpath in ["Baseline", "LRrevised", "NBrevised", "NNrevised", "SVMrevised","revised_0.5_0.25_0.2_0.5_1.25_0.1_4"]:
    # for inputdirpath in ["SVM","GaussianNB","NN","Logistic Regression"]:
    # for inputdirpath in ["datamaterial"]:
    for tolerance in [0,5,10,15,20,25]:
        # inputdir = "./journalresult/Zratio"+"_"+inputdirpath
        inputdir = "./journalresult/Zratio"
        CPlist = loadsamplefile(inputdir)
        splitresult = splitgene(targetgene, CPlist, targetgenelist, "OC_up", "OC_down",inputdir+"_"+str(tolerance),tolerance)






    # CPlist = loadsamplefile("./revised_0_0.2_0_0.25_1.1_3")
    # CPlist = loadsamplefile("./MachineLearningPart/baseline")



    #
    # print("Pvalue: "+str(calculatePvalue(CPlist, splitresult, 15,iteration = 1000000)))

    # os  .system('shutdown -s')


    # ComparisonParirlist = []
    # Cutmethod = "percentage"
    # # for B_t in [5, 10, 15, 20]:
    # for B_t in [5]:
    #     B_b = B_t
    #     for method in [2]:
    #         if method == 1:
    #             # for method1_type in ["mean", "median"]:
    #             for method1_type in ["mean"]:
    #                 inputdir = "./datamaterial/replacedDir_percentage" + "_" + str(B_t) + "_" + str(B_b) + "_" + str(method) + "_" + str(method1_type)
    #                 title = str(B_t) + "_" + str(B_b) + "_" + str(method) + "_" + str(method1_type)
    #                 ComparisonParirlist = loadsamplefile(inputdir)
    #                 CalculateResivedRatio(title,CModle, ComparisonParirlist, Method, "OC_up", "OC_down", "OC", 25)
    #
    #                 # p = Process(target=CalculateResivedRatio,
    #                 #             args=(title,CModle, ComparisonParirlist, Method, "OC_up", "OC_down", "OC", 25))
    #                 # p.start()
    #                 # l.append(p)
    #
    #
    #         else:
    #             method1_type = "mean"
    #             inputdir = "./datamaterial/replacedDir_percentage" + "_" + str(B_t) + "_" + str(B_b) + "_" + str(method) + "_" + str(method1_type)
    #             title = str(B_t) + "_" + str(B_b) + "_" + str(method) + "_" + str(method1_type)
    #             ComparisonParirlist = loadsamplefile(inputdir)
    #
    #             # CalculateFunctionalGroupScore.CalculateScorebatch(inputdir, outresultdir, Blocks)
    #             # Method = 3  # 0,1,2,3
    #             CalculateResivedRatio(title, CModle, ComparisonParirlist, Method, "OC_up", "OC_down", "OC", 0)
    # #             p = Process(target=CalculateResivedRatio,
    # #                         args=(title,CModle, ComparisonParirlist, Method, "OC_up", "OC_down", "OC", 25))
    # #             p.start()
    # #             l.append(p)
    # # for p in l:
    # #     p.join()

