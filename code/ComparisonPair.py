#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/12/2020 11:19 PM
# Filename: ComparisonPair



import os


class ComparisonPair:

    genelist = {}
    name = ""
    value = []
    effect = ""
    totalgenelist=[]


    def __init__(self):
        self.genelist = {}
        self.totalgenelist=[]
        self.name = ""
        self.value = []
        self.effect = ""



    def load(self,filepath):
        self.name = os.path.basename(filepath)
        header = True
        for line in open(filepath):
            if not line.startswith("!"):
                if header:
                    linedata = line.strip().split("\t")
                    self.effect = linedata[-1][1:]
                    header=False
                    continue
                else:
                    line = line.strip()
#                     1:genename 2:ratio 3:d 4:n 5:AVG_dn 6:Z_dn 7:AVG_n 8:Z_n

                    linedata = line.split("\t")
                    # if linedata[0].upper()=="DCSTAMP":
                    #     print("!!")
                    if len(linedata) == 2:
                        genedata = {}
                        genedata["preprocessed"] =False
                        genedata["ratio"] = float(linedata[1])
                        self.genelist[linedata[0].upper()] = genedata
                        self.totalgenelist.append(linedata[0].upper())
    # Intensity   P_avg     Z - score



                    if len(linedata) == 8:
                        genedata = {}
                        genedata["preprocessed"] =False
                        genedata["ratio"] = float(linedata[1])
                        genedata["RawC"] = float(linedata[2])
                        genedata["RawT"] = float(linedata[3])

                        self.value.append(genedata["ratio"])

                        genedata["cZ_dn"] = float(linedata[4])
                        genedata["cZ_n"] = float(linedata[5])
                        genedata["cgZ_dn"] = float(linedata[6])
                        genedata["cgZ_n"] = float(linedata[7])





                        self.genelist[linedata[0].upper()] = genedata
                        self.totalgenelist.append(linedata[0].upper())
                    if len(linedata) == 10:
                        genedata = {}
                        genedata["preprocessed"] =False
                        genedata["ratio"] = float(linedata[1])
                        genedata["RawC"] = float(linedata[2])
                        genedata["RawT"] = float(linedata[3])
                        self.value.append(genedata["ratio"])
                        genedata["Z_dn"] = float(linedata[5])
                        genedata["Z_n"] = float(linedata[7])
                        genedata["cZ_dn"] = float(linedata[8])
                        genedata["cZ_n"] = float(linedata[9])
                        self.genelist[linedata[0].upper()] = genedata
                        self.totalgenelist.append(linedata[0].upper())
                    if len(linedata) == 12:
                        genedata = {}
                        genedata["preprocessed"] = False
                        genedata["ratio"] = float(linedata[1])
                        genedata["RawC"] = float(linedata[2])
                        genedata["RawT"]= float(linedata[3])
                        self.value.append(genedata["ratio"])
                        genedata["Z_dn"] = float(linedata[5])
                        genedata["Z_n"] = float(linedata[7])
                        genedata["cZ_dn"] = float(linedata[8])
                        genedata["cZ_n"] = float(linedata[9])
                        genedata["cgZ_dn"] = float(linedata[10])
                        genedata["cgZ_n"] = float(linedata[11])
                        self.genelist[linedata[0].upper()] = genedata
                        self.totalgenelist.append(linedata[0].upper())

    def loadblock(self, filepath,blockgenelist):
        self.name = os.path.basename(filepath)
        header = True
        for line in open(filepath):
            if not line.startswith("!"):
                if header:
                    linedata = line.strip().split("\t")
                    self.effect = linedata[-1][1:]
                    header = False
                    continue
                else:
                    line = line.strip()
                    linedata = line.split("\t")
                    if linedata[0].upper() in blockgenelist:
                        genedata = {}
                        genedata["ratio"] = float(linedata[1])
                        self.genelist[linedata[0].upper()] = genedata





    def getratioValue(self,geneName):
        if geneName not in self.genelist:
            return 0.0
        else:
            return self.genelist[geneName]["ratio"]

    def getrawValueC(self,geneName):
        # print(geneName)
        # print(self.name)
        if geneName not in self.genelist:
            return 0.0
        else:
            return self.genelist[geneName]["RawC"]

    def getrawValueT(self,geneName):
        if geneName not in self.genelist:
            return 0.0
        else:
            return self.genelist[geneName]["RawT"]

    def updateRatio(self,geneName,Value):
         self.genelist[geneName]["ratio"] = Value


    def getCMZC(self,geneName):
        if geneName not in self.genelist or "cZ_dn" not in self.genelist[geneName].keys():
            return  0.0
        else:
            return self.genelist[geneName]["cZ_dn"]

    def getCMZT(self,geneName):
        if geneName not in self.genelist or "cZ_n" not in self.genelist[geneName]:
            return   0.0
        else:
            return self.genelist[geneName]["cZ_n"]


    def getCGZC(self,geneName):
        if geneName not in self.genelist or "cgZ_dn" not in self.genelist[geneName]:
            return   0.0
        else:
            return self.genelist[geneName]["cgZ_dn"]

    def getCGZT(self,geneName):
        if geneName not in self.genelist or "cgZ_n" not in self.genelist[geneName]:
            return   0.0
        else:
            return self.genelist[geneName]["cgZ_n"]




    def writerevisedresult(self,dir):
        with open(dir+"revised_"+self.getname(),"w") as outputfile:

            title = "GENE\tRNA\tRawValueControl\tRawValueTest\tCohortMatrixZControl\tCohortMatrixZTest\tCohortGenomeZControl\tCohortGenomeZTest\t@"+self.geteffect()+"\n"
            outputfile.write(title)

            for genename in self.totalgenelist:

                RawValueControl = self.getrawValueC(genename)
                RawValueTest = self.getrawValueT(genename)
                CohortMatrixZControl =self.getCMZC(genename)
                CohortMatrixZTest = self.getCMZT(genename)
                CohortGenomeZControl = self.getCGZC(genename)
                CohortGenomeZTest = self.getCGZT(genename)
                RevisedRatio = self.getratioValue(genename)
                line = genename + "\t" + str(RevisedRatio) + "\t" + str(
                    RawValueControl) + "\t" + str(
                    RawValueTest) + "\t" + str(
                    CohortMatrixZControl) + "\t" + str(
                    CohortMatrixZTest) + "\t" + str(
                    CohortGenomeZControl) + "\t" + str(
                    CohortGenomeZTest) + "\n"
                outputfile.write(line)


    def getratioValueRound(self,geneName,R):
        return round(self.genelist[geneName]["ratio"], R)


    def getname(self):
        return self.name

    def addname(self,name):
        self.name = name

    def geteffect(self):
        return self.effect




















