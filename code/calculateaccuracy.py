#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@author:honglin 
@file: calculateaccuracy.py 
@time: 2020/08/09
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

if __name__ == '__main__':

    correctupgene = []
    correctdowngene = []
    correctupgenefile="C:/wamp64/www/gse_process/ExploreZscore/paperresult/genes/up.txt"
    correctdowngenefile = "C:/wamp64/www/gse_process/ExploreZscore/paperresult//genes/down.txt"
    with open(correctupgenefile,"r") as fileopen:
        for line in fileopen.readlines():
            correctupgene.append(line.strip().upper())

    with open(correctdowngenefile,"r") as fileopen:
        for line in fileopen.readlines():
            correctdowngene.append(line.strip().upper())

    for inputdirpath in ["Baseline", "LRrevised", "NBrevised", "NNrevised", "SVMrevised",
                         "revised_0.5_0.25_0.2_0.5_1.25_0.1_4"]:
        inputdir = "./paperresult/" + inputdirpath
        testupgenefile = inputdir+"_split_upgenes.txt"
        testdowngenefile = inputdir+"_split_downgenes.txt"
        testupgene = []
        testdowngene = []

        with open(testupgenefile,"r") as fileopen:
            for line in fileopen.readlines():
                testupgene.append(line.strip().upper())

        with open(testdowngenefile,"r") as fileopen:
            for line in fileopen.readlines():
                testdowngene.append(line.strip().upper())

        score = 0
        for gene in testupgene:
            if gene in correctupgene:
                score+=1

        for gene in testdowngene:
            if gene in correctdowngene:
                score+=1

        score = score / (len(testupgene) + len(testdowngene))

        print(inputdirpath+": "+str(score))








# testupgenefile="C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0_0_0_0_0_0_0/split_upgenes.txt"
    # testdowngenefile = "C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0_0_0_0_0_0_0/split_downgenes.txt"
    #
    # testupgene=[]
    # testdowngene = []
    #
    # with open(testupgenefile,"r") as fileopen:
    #     for line in fileopen.readlines():
    #         testupgene.append(line.strip().upper())
    #
    # with open(testdowngenefile,"r") as fileopen:
    #     for line in fileopen.readlines():
    #         testdowngene.append(line.strip().upper())
    #
    # score = 0
    # for gene in testupgene:
    #     if gene in correctupgene:
    #         score+=1
    #
    # for gene in testdowngene:
    #     if gene in correctdowngene:
    #         score+=1
    #
    # score = score / (len(testupgene) + len(testdowngene))
    #
    # print("raw:"+str(score))
    #
    # testupgenefile = "C:/wamp64/www/gse_process/ExploreZscore/paperresult/svmRevisedCPprime/split_upgenes.txt"
    # testdowngenefile = "C:/wamp64/www/gse_process/ExploreZscore/paperresult/svmRevisedCPprime/split_downgenes.txt"
    #
    # testupgene = []
    # testdowngene = []
    #
    # with open(testupgenefile, "r") as fileopen:
    #     for line in fileopen.readlines():
    #         testupgene.append(line.strip().upper())
    #
    # with open(testdowngenefile, "r") as fileopen:
    #     for line in fileopen.readlines():
    #         testdowngene.append(line.strip().upper())
    #
    # score = 0
    # for gene in testupgene:
    #     if gene in correctupgene:
    #         score += 1
    #
    # for gene in testdowngene:
    #     if gene in correctdowngene:
    #         score += 1
    #
    # score = score / (len(testupgene) + len(testdowngene))
    #
    # print("svm:" + str(score))
    #
    # testupgenefile = "C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0.5_0.25_0.15_0.5_1.25_0.2_4/split_upgenes.txt"
    # testdowngenefile = "C:/wamp64/www/gse_process/ExploreZscore/paperresult/revised_0.5_0.25_0.15_0.5_1.25_0.2_4/split_downgenes.txt"
    #
    # testupgene = []
    # testdowngene = []
    #
    # with open(testupgenefile, "r") as fileopen:
    #     for line in fileopen.readlines():
    #         testupgene.append(line.strip().upper())
    #
    # with open(testdowngenefile, "r") as fileopen:
    #     for line in fileopen.readlines():
    #         testdowngene.append(line.strip().upper())
    #
    # score = 0
    # for gene in testupgene:
    #     if gene in correctupgene:
    #         score += 1
    #
    # for gene in testdowngene:
    #     if gene in correctdowngene:
    #         score += 1
    #
    # score = score / (len(testupgene) + len(testdowngene))
    #
    # print("m1:" + str(score))