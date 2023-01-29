#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/12/2020 11:31 PM
# Filename: CalculateModel





import numpy as np
import os
from ComparisonPair import ComparisonPair
from scipy import stats
import decimal

# import DBoperation as DBO



class CalculateModel:

    Block  = []
    Z_weight = 0
    WeightList = {}
    randomBlock={}
    alreayresult=""
    randomSamplepath=""
    cohort = False



    def __init__(self,randomSamplepath="E:/file/simulationRandomFiles",alreadyresult= "./randomSample.txt",Block= [],Z_weight=0.1,WeightList={},cohort = False):
        self.Block  = []
        self.Z_weight = 0
        self.WeightList = {}
        self.randomBlock = {}
        self.alreadyresult = alreadyresult
        self.randomSamplepath = randomSamplepath
        self.cohort = cohort
        self.Block = Block
        self.Z_weight = Z_weight
        self.WeightList = WeightList

        for line in open(alreadyresult):
            linedata = line.strip().split("\t")
        values = np.array(linedata).astype(np.float)
        self.randomScore = values

    def add_Samples(self,Samples):
        self.Samples = self.Samples+Samples

    def add_Block(self,Block):
        self.Block = self.Block + Block

    # do not consider z socre
    def preprocess_0(self, sample):
        newSample= sample

        # for blockgene in self.Block:
        #
        #     for genename in blockgene["list"]:

        for genename in newSample.totalgenelist:

            if not newSample.genelist[genename]["preprocessed"]:
                #   remove the higher value down to -1 to 1
                if newSample.genelist[genename]["ratio"] > 2:
                    newSample.genelist[genename]["ratio"] = 2.0
                if newSample.genelist[genename]["ratio"] < -2:
                    newSample.genelist[genename]["ratio"] = -2.0
                newSample.genelist[genename]["preprocessed"] = True
        # else:
        #     newSample.genelist[genename] = {}
        #     newSample.genelist[genename]["ratio"] = 0.0
        #     newSample.genelist[genename]["preprocessed"] = True
        return newSample


    # only consider sample matrix z socre
    def preprocess_1(self,sample,T=0.25,mi=2,power=0.5):
        newSample= sample
        for blockgene in self.Block:

            for genename in blockgene["list"]:

                if genename in newSample.totalgenelist:

                    if not newSample.genelist[genename]["preprocessed"]:
                        # adjust ratio based on z score
                        if newSample.genelist[genename]["Z_dn"] * newSample.genelist[genename]["Z_n"] < 0:
                    #         R negative: amplify (magnitude only)
                            x = abs(newSample.genelist[genename]["Z_dn"]-newSample.genelist[genename]["Z_n"])
                            w = mi**x
                            newSample.genelist[genename]["ratio"] =w * newSample.genelist[genename]["ratio"]
                        else:
                            x = abs(newSample.genelist[genename]["Z_dn"] - newSample.genelist[genename]["Z_n"])
                            if x >T:
                                w = mi**(x-T)
                            elif x <=T:
                                w = x ** power
                            newSample.genelist[genename]["ratio"] = w * newSample.genelist[genename]["ratio"]
                        if newSample.genelist[genename]["ratio"] > 2:
                            newSample.genelist[genename]["ratio"] = 2.0
                        if newSample.genelist[genename]["ratio"] < -2:
                            newSample.genelist[genename]["ratio"] = -2.0
                        # newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] / 2

                # else:
                #     newSample.genelist[genename]={}
                #     newSample.genelist[genename]["ratio"] =0.0
                #     newSample.genelist[genename]["preprocessed"]=True
        return newSample


    # only consider cohort Z
    def preprocess_2(self,sample,W =2,T=0.5,B=2):
        newSample= sample
        # for blockgene in self.Block:
        #     # print(blockgene["name"])
        #     for genename in blockgene["list"]:
        #         # print(genename)
        #         # print(newSample.name)
        for genename in newSample.totalgenelist:
            # print(True)
            # print(newSample.genelist[genename])
            if not newSample.genelist[genename]["preprocessed"]:
                # introduce the concept of absent
                if newSample.genelist[genename]["ratio"] >0:
            #         we penate the ratio value if both are low
                    if newSample.genelist[genename]["cZ_dn"]<-1*B and newSample.genelist[genename]["cZ_n"]<-1*B and abs(
                            newSample.genelist[genename]["cZ_dn"]-newSample.genelist[genename]["cZ_n"])<T:
                        newSample.genelist[genename]["ratio"]=newSample.genelist[genename]["ratio"] + W* max(
                            [newSample.genelist[genename]["cZ_dn"],newSample.genelist[genename]["cZ_n"]])
                # introduce the concept of present
                if newSample.genelist[genename]["ratio"] <0:
                    #         we amplify the ratio value if both are low
                    if newSample.genelist[genename]["cZ_dn"] > B and newSample.genelist[genename]["cZ_n"] > B and abs(
                            newSample.genelist[genename]["cZ_dn"] - newSample.genelist[genename]["cZ_n"]) < T:
                        newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] + W * min(
                            [newSample.genelist[genename]["cZ_dn"], newSample.genelist[genename]["cZ_n"]])
                if newSample.genelist[genename]["ratio"] > 2:
                    newSample.genelist[genename]["ratio"] = 2.0
                    # newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] / 2
                if newSample.genelist[genename]["ratio"] < -2:
                    newSample.genelist[genename]["ratio"] = -2.0
                    # newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] / 2
        # else:
        #     newSample.genelist[genename]={}
        #     newSample.genelist[genename]["ratio"] =0.0
        #     newSample.genelist[genename]["preprocessed"]=True
        return newSample



    # only consider cohort genome Z right now same as preprocess_2
    def preprocess_3(self,sample,BG,WP,T):
        newSample = sample
        # for blockgene in self.Block:
        #     # print(blockgene["name"])
        #     for genename in blockgene["list"]:
        #         # print(genename)
        #         # print(newSample.name)
        for genename in newSample.totalgenelist:
            # print(True)
            # print(newSample.genelist[genename])
            if not newSample.genelist[genename]["preprocessed"]:
                # introduce the concept of absent
                if newSample.genelist[genename]["ratio"] > 0:
                    #         we penate the ratio value if both are low
                    if newSample.genelist[genename]["cgZ_dn"] < -1 * BG and newSample.genelist[genename]["cgZ_n"] < -1 * BG and abs(newSample.genelist[genename]["cgZ_dn"] - newSample.genelist[genename]["cgZ_n"]) < T:
                    # if newSample.genelist[genename]["cgZ_dn"] < -1 * BG and newSample.genelist[genename]["cgZ_n"] < -1 * BG :
                        x = abs(newSample.genelist[genename]["cgZ_dn"] - newSample.genelist[genename]["cgZ_n"])
                        WG = x**WP
                        newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] + WG * max([newSample.genelist[genename]["cgZ_dn"], newSample.genelist[genename]["cgZ_n"]])
                # introduce the concept of present
                if newSample.genelist[genename]["ratio"] < 0:
                    #         we amplify the ratio value if both are low
                    if newSample.genelist[genename]["cgZ_dn"] > BG and newSample.genelist[genename]["cgZ_n"] > BG and abs(newSample.genelist[genename]["cgZ_dn"] - newSample.genelist[genename]["cgZ_n"]) < T:
                    # if newSample.genelist[genename]["cgZ_dn"] > BG and newSample.genelist[genename]["cgZ_n"] > BG :
                        x = abs(newSample.genelist[genename]["cgZ_dn"] - newSample.genelist[genename]["cgZ_n"])
                        WG = x ** WP
                        newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] + WG * min([newSample.genelist[genename]["cgZ_dn"], newSample.genelist[genename]["cgZ_n"]])
                if newSample.genelist[genename]["ratio"] > 2:
                    newSample.genelist[genename]["ratio"] = 2.0
                    # newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] / 2

                if newSample.genelist[genename]["ratio"] < -2:
                    newSample.genelist[genename]["ratio"] = -2.0
                    # newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] / 2

        # else:
        #     newSample.genelist[genename]={}
        #     newSample.genelist[genename]["ratio"] =0.0
        #     newSample.genelist[genename]["preprocessed"]=True
        return newSample

        # Using Cohort matrix Z, Cohort genome Z and Sample Z to define concept of absent and present
        # def preprocess_4(self, sample, BM=2,BG=1,WM=1.5,WG=2):
        #     for blockgene in self.Block:
        #         # print(blockgene["name"])
        #         for genename in blockgene["list"]:
        #             # print(genename)
        #             # print(sample.name)
        #             if genename in sample.genelist:
        #                 # print(True)
        #                 # print(sample.genelist[genename])
        #                 if not sample.genelist[genename]["preprocessed"]:
        #                     # introduce the concept of absent
        #                     if sample.genelist[genename]["ratio"] > 0:
        #                         #         we penate the ratio value if both are low
        #                         if sample.genelist[genename]["cZ_dn"] < -1 * BM and sample.genelist[genename]["cZ_n"] < -1 * BM and sample.genelist[genename]["cgZ_dn"] < -1 * BG and sample.genelist[genename]["cgZ_n"] < -1 * BG:
        #                             sample.genelist[genename]["ratio"] = sample.genelist[genename]["ratio"] + WM * max([sample.genelist[genename]["cZ_dn"], sample.genelist[genename]["cZ_n"]])+ WG * max([sample.genelist[genename]["cgZ_dn"], sample.genelist[genename]["cgZ_n"]])
        #                     if sample.genelist[genename]["ratio"] < 0:
        #                         #         we penate the ratio value if both are low
        #                         if sample.genelist[genename]["cZ_dn"] > BM and sample.genelist[genename]["cZ_n"] > BM and sample.genelist[genename]["cgZ_dn"] > BG and sample.genelist[genename]["cgZ_n"] > BG:
        #                             sample.genelist[genename]["ratio"] = sample.genelist[genename]["ratio"] + WM * min(
        #                                 [sample.genelist[genename]["cZ_dn"],
        #                                  sample.genelist[genename]["cZ_n"]]) + WG * min(
        #                                 [sample.genelist[genename]["cgZ_dn"], sample.genelist[genename]["cgZ_n"]])
        #
        #                     if sample.genelist[genename]["ratio"] > 2:
        #                         sample.genelist[genename]["ratio"] = 2.0
        #                         sample.genelist[genename]["ratio"] = sample.genelist[genename]["ratio"] / 2
        #
        #                     if sample.genelist[genename]["ratio"] < -2:
        #                         sample.genelist[genename]["ratio"] = -2.0
        #                         sample.genelist[genename]["ratio"] = sample.genelist[genename]["ratio"] / 2
        #             else:
        #                 sample.genelist[genename] = {}
        #                 sample.genelist[genename]["ratio"] = 0.0
        #                 sample.genelist[genename]["preprocessed"] = True
        #     return sample



    def preprocess_4(self, sample, BM=2,BG=1,WM=1.5,WG=2,TM = 1,TG=1):
        newSample = sample


        # for blockgene in self.Block:
        #     # print(blockgene["name"])
        #     for genename in blockgene["list"]:


                # print(genename)
                # print(sample.name)
        for genename in newSample.totalgenelist:
            # print(True)
            # print(sample.genelist[genename])
            if not newSample.genelist[genename]["preprocessed"]:
                xG = abs(newSample.genelist[genename]["cgZ_dn"] - newSample.genelist[genename]["cgZ_n"])
                xM = abs(newSample.genelist[genename]["cZ_dn"] - newSample.genelist[genename]["cZ_n"])
                # introduce the concept of absent
                if newSample.genelist[genename]["ratio"] > 0:
                    #         we penate the ratio value if both are low
                    if newSample.genelist[genename]["cZ_dn"] < (-1 * BM) \
                            and newSample.genelist[genename]["cZ_n"] < (-1 * BM) \
                            and newSample.genelist[genename]["cgZ_dn"] < (-1 * BG) \
                            and newSample.genelist[genename]["cgZ_n"] < (-1 * BG) \
                            and xG < TG \
                            and xM < TM :
                        # if newSample.genelist[genename]["cgZ_dn"] < -1 * BG and newSample.genelist[genename]["cgZ_n"] < -1 * BG :
                        Wg = xG ** WG
                        Wm = xM ** WM
                        newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] + Wg * max([newSample.genelist[genename]["cgZ_dn"], newSample.genelist[genename]["cgZ_n"]])+Wm*max([newSample.genelist[genename]["cZ_dn"], newSample.genelist[genename]["cZ_n"]])
                    # introduce the concept of present
                if newSample.genelist[genename]["ratio"] < 0:
                    #         we amplify the ratio value if both are low
                    if newSample.genelist[genename]["cZ_dn"] > BM \
                            and newSample.genelist[genename]["cZ_n"] > BM \
                            and newSample.genelist[genename]["cgZ_dn"] > BG \
                            and newSample.genelist[genename]["cgZ_n"] > BG \
                            and xG < TG \
                            and xM < TM:
                        Wg = xG ** WG
                        Wm = xM ** WM
                        newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] + Wg * min(
                            [newSample.genelist[genename]["cgZ_dn"], newSample.genelist[genename]["cgZ_n"]]) + Wm * min(
                            [newSample.genelist[genename]["cZ_dn"], newSample.genelist[genename]["cZ_n"]])

                if newSample.genelist[genename]["ratio"] > 2:
                    newSample.genelist[genename]["ratio"] = 2.0
                    # newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] / 2

                if newSample.genelist[genename]["ratio"] < -2:
                    newSample.genelist[genename]["ratio"] = -2.0


                # if newSample.genelist[genename]["ratio"] > 0:
                #     #         we penate the ratio value if both are low
                #     if newSample.genelist[genename]["cZ_dn"] < (-1 * BM) and newSample.genelist[genename][
                #         "cZ_n"] < (-1 * BM) and newSample.genelist[genename]["cgZ_dn"] < (-1 * BG) and newSample.genelist[genename]["cgZ_n"] < (-1 * BG):
                #         newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] + WM * max(
                #             [newSample.genelist[genename]["cZ_dn"], newSample.genelist[genename]["cZ_n"]]) + WG * max(
                #             [newSample.genelist[genename]["cgZ_dn"], newSample.genelist[genename]["cgZ_n"]])
                # if newSample.genelist[genename]["ratio"] < 0:
                #     #         we penate the ratio value if both are low
                #     if newSample.genelist[genename]["cZ_dn"] > BM and newSample.genelist[genename]["cZ_n"] > BM and newSample.genelist[genename]["cgZ_dn"] > BG and newSample.genelist[genename]["cgZ_n"] > BG:
                #         newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"] + WM * min(
                #             [newSample.genelist[genename]["cZ_dn"],
                #              newSample.genelist[genename]["cZ_n"]]) + WG * min(
                #             [newSample.genelist[genename]["cgZ_dn"], newSample.genelist[genename]["cgZ_n"]])
                #
                # if newSample.genelist[genename]["ratio"] > 2:
                #     newSample.genelist[genename]["ratio"] = 2.0
                # # newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"]
                #
                # if newSample.genelist[genename]["ratio"] < -2:
                #     newSample.genelist[genename]["ratio"] = -2.0
                #     # newSample.genelist[genename]["ratio"] = newSample.genelist[genename]["ratio"]
        # else:
        #     newSample.genelist[genename] = {}
        #     newSample.genelist[genename]["ratio"] = 0.0
        #     newSample.genelist[genename]["preprocessed"] = True

        return newSample


    def calculateScoreMatraix(self,sample,WeightList={}):
        socreMatrix={}
        for blockgene in self.Block:
            # print(blockgene)
            socreMatrix[blockgene["id"]] = {}
            value = 0
            count = 0
            for genename in blockgene["list"]:
                if genename in WeightList:
                    score = sample.getratioValue(genename)*WeightList[genename]
                else:
                    score  = sample.getratioValue(genename)
                if not score==0:
                    value += score
                    count += 1
            AVG = value/(count*2)
            if AVG >=0:
                value =AVG **2
            else:
                value = -1*(AVG **2)


            # calcualte pvalue
            kde = stats.gaussian_kde(self.randomScore, bw_method=0.01)
            pval = kde.integrate_box_1d(value, 1.0)
            if pval > 0.5:
                pval = 1 - pval

            # t, pval = scipy.stats.ttest_1samp(self.randomScore, popmean=value)
            # value = round(value,2)
            socreMatrix[blockgene["id"]]["score"] = value
            # pval = '%.2E' % decimal.Decimal(pval)
            socreMatrix[blockgene["id"]]["pval"] = pval
            socreMatrix[blockgene["id"]]["id"] = blockgene["id"]
            socreMatrix[blockgene["id"]]["name"] = blockgene["name"]
            socreMatrix["effect"] = sample.geteffect()
        #         need to have P-value
        #         socreMatrix[blockgene["name"]][sample.getname()]["pvalue"] = 0
        return socreMatrix


    def getgenefromblock(self,CP,blockname):
        blocklist = []
        for block in self.Block:
            if block["name"] == blockname:
                blocklist = block["list"]

        returnlist={}
        for gene in blocklist:
            returnlist[gene.upper()] = CP.getratioValue(gene.upper())

        return returnlist


            # blockgenes["name"] = os.path.basename(filepath)
            # blockgenes["id"] = os.path.basename(filepath)

    # def calculateScoreMatraixGenePvalue(self,sample,WeightList={}):
    #     socreMatrix={}
    #     for blockgene in self.Block:
    #         socreMatrix[blockgene["id"]] = {}
    #         value = 0
    #         count = 0
    #         for genename in blockgene["list"]:
    #             genePvalue = self.getGenePvalue(genename,sample)
    #             if genename in WeightList:
    #                 score = sample.getratioValue(genename)*WeightList[genename]*(1-genePvalue)
    #             else:
    #                 score  = sample.getratioValue(genename)*(1-genePvalue)
    #             if not score==0:
    #                 value += score
    #                 count += 1
    #
    #         value = value/count
    #
    #
    #         # calcualte pvalue
    #         kde = stats.gaussian_kde(self.randomScore, bw_method=0.01)
    #         pval = kde.integrate_box_1d(value, 1.0)
    #         if pval > 0.5:
    #             pval = 1 - pval
    #
    #         # t, pval = scipy.stats.ttest_1samp(self.randomScore, popmean=value)
    #         value = round(value,2)
    #         socreMatrix[blockgene["id"]]["score"] = value
    #         pval = '%.2E' % decimal.Decimal(pval)
    #         socreMatrix[blockgene["id"]]["pval"] = pval
    #         socreMatrix[blockgene["id"]]["id"] = blockgene["id"]
    #         socreMatrix[blockgene["id"]]["name"] = blockgene["name"]
    #         socreMatrix["effect"] = sample.geteffect()
    #     #         need to have P-value
    #     #         socreMatrix[blockgene["name"]][sample.getname()]["pvalue"] = 0
    #     return socreMatrix


    # def calculateScoreMatraixOutBlock(self,sample,blockgene,WeightList={}):
    #     socreMatrix={}
    #     socreMatrix[blockgene["name"]] = {}
    #     value = 0
    #     count = 0
    #     for genename in blockgene["list"]:
    #         if genename in WeightList:
    #             score = sample.getratioValue(genename)*WeightList[genename]
    #         else:
    #             score  = sample.getratioValue(genename)
    #         if not score==0:
    #             value += score
    #             count += 1
    #
    #     value = value/count
    #     socreMatrix[blockgene["name"]] = {}
    #     socreMatrix[blockgene["name"]]["score"] = value
    #     #         need to have P-value
    #     #         socreMatrix[blockgene["name"]][sample.getname()]["pvalue"] = 0
    #     return socreMatrix
    #
    # def addValue(self,socreMatrix):
    #     return socreMatrix

    # def getGenePvalue(self,genename,sample):
    #     genescore = sample.getratioValue(genename)
    #     connection = DBO.generateconnction()
    #     result = DBO.getgene(genename,connection)
    #     kde = stats.gaussian_kde(result, bw_method=0.01)
    #     pval = kde.integrate_box_1d(genescore, 1.0)
    #     if pval > 0.5:
    #         pval = 1 - pval
    #
    #     return pval


    # def








    # def randomvalue(self,blockgene):
    #     g = os.walk(self.randomSamplepath)
    #     SampleScores = []
    #     for path, dir_list, file_list in g:
    #         for file_name in file_list:
    #             filepath = os.path.join(path, file_name)
    #             S = Sample()
    #             S.load(filepath)
    #             S = self.preprocessOutBlock(sample=S,blockgene=blockgene)
    #             sampleScore = self.calculateScoreMatraixOutBlock(sample=S,blockgene=blockgene)
    #             SampleScores.append(sampleScore)
    #     self.randomBlock[blockgene["name"]] = SampleScores
    #     with open(self.alreadyresult,"a") as result:
    #         line = blockgene["name"]
    #         for score in SampleScores:
    #             line +="\t"+str(score)
    #         line +="\n"
    #         result.write(line)


        # # t, pval = scipy.stats.ttest_1samp(SampleScores, popmean=Score)
        #
        # return pval









            # valueMean = np.mean(sample.value)
            # N = np.max(sample.value) - np.min(sample.value)
            # for genename, genevalue in sample.genelist.items():
            #     sample.genelist[genename]["ratio"] = (genevalue["ratio"] - valueMean)/N








#  ratio from -1 to 1






