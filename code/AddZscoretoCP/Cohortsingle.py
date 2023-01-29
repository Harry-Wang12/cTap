#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/9/2020 2:53 PM
# @Author  : honglin wang
# @File    : Sample.py
# @Software: PyCharm

import statistics
from scipy import stats
import time


class Cohortsingle:
    rawvalue = {}
    normalizevalue = {}
    orderedvalue = {}
    name = ""
    top = {}
    bottom={}
    middle={}


    def __init__(self):
        self.rawvalue = {}
        self.normalizevalue = {}
        self.orderedvalue = {}
        self.name = ""
        self.top = {}
        self.bottom = {}
        self.middle = {}


    def addname(self,name):
        self.name = name

    def addrawvalue(self,genename,genevalue):
        self.rawvalue[genename.upper()] = genevalue

    def ordergene(self):
        # print("start order" + self.name)
        self.orderedvalue = {k: v for k, v in sorted(self.rawvalue.items(), key=lambda item: item[1])}

    def sperateValues(self,Cutmethod,toprate,bottomrate):

        # print("start sperate"+self.name)

        if Cutmethod == "percentage":
            number = 1
            for key, value in self.orderedvalue.items():
                rate = number / len(self.orderedvalue)
                number += 1
                if rate <= (toprate / 100):
                    self.top[key] = value
                if rate > (toprate / 100) and rate < (1 - (bottomrate / 100)):
                    # if not value == 0.0:
                    self.middle[key] = value
                if rate >= (1 - (bottomrate / 100)):
                    self.bottom[key] = value
        if  Cutmethod == "Zscore":
            genelist = []
            for key, value in self.orderedvalue.items():
                genelist.append(value)
            average = statistics.mean(genelist)
            STD = statistics.stdev(genelist)
            for key, gvalue in self.orderedvalue.items():
                Zscore = (gvalue-average)/STD
                if Zscore <= (-1*toprate):
                    self.top[key] = float(gvalue)
                elif Zscore > (-1*toprate) and Zscore < bottomrate:
                    self.middle[key] =float(gvalue)
                elif Zscore >= bottomrate:
                    self.bottom[key] = float(gvalue)

    def generateVectorofMiddle(self):

        genelist = []

        for key,value in self.middle.items():
            genelist.append(value)
        # print(max(genelist))
        # print(min(genelist))

        return genelist



    # type
    def remapmidpart(self,midvector,method,method1_type):
        # print("start remapmidpart" + self.name)
        time1 = time.time()
        number = 0
        for key,value in self.middle.items():
            self.normalizevalue [key] = midvector[number]
            number+=1

        if method==1:
            orimid = self.generateVectorofMiddle()
            if method1_type =="median":
                old = statistics.median(orimid)
                new = statistics.median(midvector)
            elif method1_type=="mean":
                old = statistics.mean(orimid)
                new = statistics.mean(midvector)
            if not old==0:
                prob = new/old
            else:
                prob = new / (old+0.01)
            for key,value in self.top.items():
                self.normalizevalue[key] = value*prob
            for key, value in self.bottom.items():
                self.normalizevalue[key] = value * prob
        else:
            topZscore =(-1* (midvector[0] - statistics.mean(midvector))/statistics.stdev(midvector))

            BottomZscore = (midvector[-1] - statistics.mean(midvector))/statistics.stdev(midvector)
            halfnumber = int(len(midvector)/2)
            topRate = topZscore /halfnumber
            bottomRate = BottomZscore/halfnumber

            midaverage = statistics.mean(midvector)
            midstdv = statistics.stdev(midvector)

#             top number minus
            topnumber = len(self.top)+1
            for key,value in self.top.items():
                newZvalue = (topnumber+halfnumber) * topRate
                newValue = newZvalue*midstdv+midaverage
                self.normalizevalue[key] = newValue
                topnumber-=1


#             bottom number plus
            bottomnumber = 1

            for key,value in self.bottom.items():
                newZvalue = (bottomnumber+halfnumber) * bottomRate
                newValue = newZvalue*midstdv+midaverage
                self.normalizevalue[key] = newValue
                bottomnumber+=1
        time2 = time.time()
        # print("finish remape"+self.name+ " cost :"+ str(time2 - time1))





    def getnormalizevaluebyname(self,genename):
        return self.normalizevalue[genename]


    def getvaluelist(self):
        genelist = []
        for key, value in self.rawvalue.items():
            genelist.append(value)
        return genelist

    def getZscorevalue(self):

        genevaluelist = self.getvaluelist()
      
        return stats.zscore(genevaluelist)

    def getcorhortZscorevalue(self, totalgenelistMeanlist,totalgenelistSTDVlist, Ztype):
        Zlist = []
        if Ztype =="sample":

            genevaluelist = self.getZscorevalue()
            for value in genevaluelist:
                Zlist.append(value)
        if Ztype == "genome":
            for genename, rawvalue in self.rawvalue.items():
                average =totalgenelistMeanlist[genename]
                STD = totalgenelistSTDVlist[genename]
                if not STD == 0:
                    Zlist.append((rawvalue-average)/STD)
                else:
                    Zlist.append(0.0)


        return Zlist




























