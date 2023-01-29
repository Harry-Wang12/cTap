#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@author:honglin 
@file: FunctionalScoreBatch.py 
@time: 2020/09/17
@contact: honglin.wang@uconn.edu  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃             ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃             ┣┓
                ┃　           ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

from CalculateModel import CalculateModel
from ComparisonPair import ComparisonPair
import json
import os



def loadsamplefile(sampledir,blocklist):
    ComparisonParirlist = []
    blockgenelist = []
    for block in blocklist:
        genelist = block["list"]
        blockgenelist +=genelist





    g = os.walk(sampledir)

    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepath = os.path.join(path, file_name)
            print("reading sample "+file_name)
            C = ComparisonPair()
            C.loadblock(filepath,blockgenelist)
            ComparisonParirlist.append(C)

    return ComparisonParirlist






if __name__ == '__main__':

    samplesdir = "C:/Users/how17003/Documents/Code/SmallTool/result/splitlog2_new"
    outputfile = "./Single_Cell_Function_Group_Score.txt"
    json_contentpath = "./BIBCI-OC-loop (7-13).txt"




    f = open(json_contentpath,"r")
    json_content = f.read()
    json_content = json.loads(json_content)

    # makesmaple

    nodes = json_content["elements"]["nodes"]

    # find FGgroup

    FGgroupblock = []
    FGgroupblockdictid = {}
    geneparent = {}
    returnlist ={}
    # analysis jsoncontent
    # try:
    for node in nodes:
        # if "BUNDLE" not in node["data"]["Type"].upper() and "LABEL" not in node["data"]["Type"].upper():
        #gene or FG group
        if "BUNDLE_FG" in node["data"]["Type"]:
            blockgenes = {}
            blockgenes["name"] = node["data"]["name"]
            blockgenes["id"] = node["data"]["name"]
            blockgenes["list"] = []
            FGgroupblockdictid[node["data"]["id"]] = blockgenes
        else:
            if "parent" in node["data"]:
                genename = node["data"]["name"]

                if node["data"]["parent"] in geneparent:
                    geneparent[node["data"]["parent"]].append(genename.upper())
                else:
                    geneparent[node["data"]["parent"]] = []
                    geneparent[node["data"]["parent"]].append(genename.upper())




    for id,genelist in geneparent.items():
        if id in FGgroupblockdictid:
            FGgroupblockdictid[id]["list"] = genelist
            FGgroupblock.append(FGgroupblockdictid[id])

    del(FGgroupblockdictid)

    CModle = CalculateModel(Block=FGgroupblock)

    ComparisonParirlist = loadsamplefile(samplesdir,FGgroupblock)

    # print("11")

    SamplesScore = {}
    for CP in ComparisonParirlist:
        SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)

    with open(outputfile, "w") as file:
        line = "result"
        for Samplename, score in SamplesScore.items():
            # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
            # line += "\t" + Samplename + "\t" + Samplename + "_pval"
            line += "\t" + Samplename
        line += "\n"
        # line = ""
        for block in FGgroupblock:
            line += block["name"]
            for Samplename, score in SamplesScore.items():
                line += "\t" + str(score[block["name"]]["score"])
                # line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
                #     score[block["name"]]["pval"])
            line += "\n"

        file.write(line)