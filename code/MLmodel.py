#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@author:honglin 
@file: MLmodel.py 
@time: 2020/07/23
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

import itertools
from sklearn import metrics
import os
import CalculateFunctionalGroupScore
from ComparisonPair import ComparisonPair
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import sklearn.naive_bayes
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.neural_network import MLPClassifier
from CalculateModel import CalculateModel
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from random import choice
from sklearn.ensemble import RandomForestClassifier
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


def loadfile(inputfile,labelnumber):
    returnlist = {}
    returnlist["x"] = []
    returnlist["y"] = []
    title = True
    with open(inputfile,"r") as samplefile:
        for line in samplefile.readlines():
            if title:
                title = False
            else:
                linearray = line.strip().split("\t")
                label  = int(linearray.pop(-1))
                if label in labelnumber:
                    if label == labelnumber[0]:
                        Y = -1
                    elif label == labelnumber[1]:
                        Y = 1
                    # Y=label
                    linearray.pop(0)
                    X = np.array(linearray)
                    X= X.astype(np.float)
                    returnlist["x"].append(X)
                    returnlist["y"].append(Y)
    return returnlist














def loadblockinformation(blockdir,labelfile):

    blocklist = {}
    effectlist = []
    with open(labelfile, "r") as labels:
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
    g = os.walk(blockdir)
    Blocks= []


    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepath = os.path.join(path, file_name)
            blockgenes = {}
            blockgenes["name"] = os.path.basename(filepath)
            blockgenes["id"] = os.path.basename(filepath)
            blockgenes["OC_up"] =blocklist[os.path.basename(filepath)]["OC_up"]
            blockgenes["OC_down"] =blocklist[os.path.basename(filepath)]["OC_down"]
            blockgenes["list"] = []
            for line in open(filepath):
                line = line.strip()
                blockgenes["list"].append(line.upper())
            Blocks.append(blockgenes)
    return  Blocks




def GenerateDataSet(inputdir,Blocks,TFlist):
    returnlist={}
    returnlist["x"]=[]
    returnlist["y"]=[]
    ComparisonParirlist = loadsamplefile(inputdir)

    with open("./journalresult/totalfile.txt","w") as outfile:
        for block in Blocks:
            for CP in ComparisonParirlist:
                for genename in TFlist:
                    line = genename + "\t" + CP.getname() + "\t" + str(CP.getratioValue(genename)) + "\t" + str(
                        CP.getCMZC(genename)) + "\t" + str(CP.getCMZT(genename)) + "\t" + str(
                        CP.getCGZC(genename)) + "\t" + str(CP.getCGZT(genename))
                    X = [CP.getratioValue(genename),CP.getCMZC(genename),CP.getCMZT(genename),CP.getCGZC(genename),CP.getCGZT(genename)]
                    Y = 0
                    if genename == "IRF8":
                        if CP.geteffect() == "OC_down":
                            Y = 1
                            line += "\t" + str(1) + "\n"
                        if CP.geteffect() == "OC_up":
                            line += "\t" + str(-1) + "\n"
                            Y = -1
                    if genename == "NFATC1":
                        if CP.geteffect() == "OC_down":
                            Y = -1
                            line+="\t"+str(-1)+"\n"
                        if CP.geteffect() == "OC_up":
                            Y = 1
                            line+="\t"+str(1)+"\n"
                    outfile.write(line)
                    returnlist["x"].append(X)
                    returnlist["y"].append(Y)

                for genename in block["list"]:
                    if genename in CP.totalgenelist:
                        line =genename+"\t"+CP.getname()+"\t"+str(CP.getratioValue(genename))+"\t"+str(CP.getCMZC(genename))+"\t"+str(CP.getCMZT(genename))+"\t"+str(CP.getCGZC(genename))+"\t"+str(CP.getCGZT(genename))
                        # line =genename+"\t"+CP.getname()+"\t"+str(CP.getratioValue(genename)+"\t"+str(CP.getCGZC(genename))+"\t"+str(CP.getCGZT(genename))
                        X = [CP.getratioValue(genename),CP.getCMZC(genename),CP.getCMZT(genename),CP.getCGZC(genename),CP.getCGZT(genename)]
                        # X = [CP.getCMZC(genename),CP.getCMZT(genename),CP.getCGZC(genename),CP.getCGZT(genename)]
                        Y = 0
                        if block[CP.geteffect()]=="negative":
                            line+="\t"+str(-1)+"\n"
                            Y = -1
                        elif block[CP.geteffect()]=="positive":
                            line+="\t"+str(1)+"\n"
                            Y = 1
                        outfile.write(line)
                        returnlist["x"].append(X)
                        returnlist["y"].append(Y)
    return returnlist

def GeneraterandomDataSet(inputdir, Blocks,TFlist):
    returnlist={}
    returnlist["x"]=[]
    returnlist["y"]=[]
    ComparisonParirlist = loadsamplefile(inputdir)
    for block in Blocks:
        for CP in ComparisonParirlist:
            for genename in TFlist:
                randgenename = choice(CP.totalgenelist)
                X = [CP.getratioValue(randgenename),CP.getCMZC(randgenename),CP.getCMZT(randgenename),CP.getCGZC(randgenename),CP.getCGZT(randgenename)]
                Y = 0
                if genename == "IRF8":
                    if CP.geteffect() == "OC_down":
                        Y = 1
                    if CP.geteffect() == "OC_up":
                    # line+="\t"+str(-1)+"\n"
                        Y = -1
                if genename == "NFATC1":
                    if CP.geteffect() == "OC_down":
                        Y = -1
                    if CP.geteffect() == "OC_up":
                        Y = 1
                returnlist["x"].append(X)
                returnlist["y"].append(Y)

            for genename in block["list"]:
                if genename in CP.totalgenelist:
                    randgenename = choice(CP.totalgenelist)
                    # line =genename+"\t"+CP.getname()+"\t"+str(CP.getratioValue(genename))+"\t"+str(CP.getCMZC(genename))+"\t"+str(CP.getCMZT(genename))+"\t"+str(CP.getCGZC(genename))+"\t"+str(CP.getCGZT(genename))
                    # line =genename+"\t"+CP.getname()+"\t"+str(CP.getratioValue(genename)+"\t"+str(CP.getCGZC(genename))+"\t"+str(CP.getCGZT(genename))
                    X = [CP.getratioValue(randgenename),CP.getCMZC(randgenename),CP.getCMZT(randgenename),CP.getCGZC(randgenename),CP.getCGZT(randgenename)]
                    # X = [CP.getCMZC(genename),CP.getCMZT(genename),CP.getCGZC(genename),CP.getCGZT(genename)]
                    Y = 0
                    if block[CP.geteffect()]=="negative":
                        # line+="\t"+str(-1)+"\n"
                        Y = -1
                    elif block[CP.geteffect()]=="positive":
                        # line+="\t"+str(1)+"\n"
                        Y = 1
                    # outfile.write(line)
                    returnlist["x"].append(X)
                    returnlist["y"].append(Y)
    return returnlist





def replaceRatio(inputdir,model,outputdir):
    ComparisonParirlist = loadsamplefile(inputdir)
    for CP in ComparisonParirlist:
        for genename in CP.totalgenelist:
            # X = [[CP.getratioValue(genename),CP.getCGZC(genename),CP.getCGZT(genename)]]
            X = [[CP.getratioValue(genename),CP.getCMZC(genename),CP.getCMZT(genename),CP.getCGZC(genename),CP.getCGZT(genename)]]
            # X = [[CP.getCMZC(genename),CP.getCMZT(genename),CP.getCGZC(genename),CP.getCGZT(genename)]]
            revisedR = model.predict(X)
            CP.updateRatio(genename,revisedR[0])
        CP.writerevisedresult(outputdir+"/")



if __name__ == '__main__':
    # trainingdir  = "./MachineLearningPart/trainingsamples"
    # testdir = "./MachineLearningPart/testsamples"
    # blockdir  = "./testblock"
    # effectsign = "./effectsign.txt"
    # trainingsampledata = "./MachineLearningPart/trainingsampledatamaterial.txt"
    # testsampledata = "./MachineLearningPart/testsampledatamaterial.txt"
    
    # GenerateDataSet(trainingdir,blockdir,effectsign,trainingsampledata)
    # GenerateDataSet(testdir,blockdir,effectsign,testsampledata)
    ####################################################################################
    # inputdir =  "./journalresult/Zratio"
    # # inputdir =  "./MachineLearningPart/trainingsamples"
    # blockdir  = "./testblock"
    # effectsign = "./effectsign.txt"
    # sampledata = "./journalresult/total.txt"
    # TFlist=["IRF8","NFATC1"]
    # Blocks = loadblockinformation(blockdir, effectsign)



    #####################################random###############################################

    # totaldata = GenerateDataSet(inputdir, Blocks,TFlist)
    # # inputfile="C:/Users/how17003/Documents/pujan/BRCA_COAD_STAD_scores_T.txt"
    # inputfile="C:/Users/how17003/Documents/pujan/BRCA_scores_T.txt"
    # # inputfile="C:/Users/how17003/Documents/pujan/COAD_scores_T.txt"
    # listnumber = [0,1,2,3,4,5]
    # for labels in list(itertools.combinations(listnumber,2)):

    #     labelnumber = list(labels)
    #     i = labelnumber[0]
    #     j = labelnumber[1]
    #     title = "BRCA_subtype_"+str(i)+"_"+str(j)
    #     totaldata = loadfile(inputfile,labelnumber)
    #     # totaldata = GeneraterandomDataSet(inputdir, Blocks,TFlist)
    #     totaldataX = totaldata["x"]
    #     totaldataY = totaldata["y"]
    # #     # random_state = np.random.RandomState(0)
    #     X_train = totaldataX
    #     y_train = totaldataY
    #     X_train, X_test, y_train, y_test = train_test_split(totaldataX, totaldataY, test_size=0.3, random_state=0) #NEED CHANGE FOR AUC
    #     # lr = LogisticRegression(C=1)
    #     # y_score =lr.fit(X_train, y_train).decision_function(X_test)
    #     # = lr
    #     plt.figure()

    #     lw = 2
    #     plt.figure(figsize=(10, 10))

    #     for modelname in ["SVM","GaussianNB","NN","Logistic Regression","KNN","Random Forest","DecisionTree","AdaBoost","GDBT"]:
    #     # for modelname in ["SVM"]:
    #         outputdir = "./paper_material/" + modelname
    #         if not os.path.exists(outputdir):
    #             os.mkdir(outputdir)
    #         if modelname == "SVM":
    #             model = svm.SVC(kernel='rbf', gamma=0.8, probability=True)
    #             # model = svm.SVC(decision_function_shape='ovo',probability=True)

    #             # y_score = model.fit(X_train, y_train)
    #             # replaceRatio(inputdir, model, outputdir)
    #             y_score = model.fit(X_train, y_train).decision_function(X_test)
    #             # metrics.roc_auc_score(y_score, y_test, average='micro')
    #             fpr, tpr, threshold = roc_curve(y_test,y_score)

    #         elif modelname == "GaussianNB":
    #             model = sklearn.naive_bayes.GaussianNB()
    #             # y_score = model.fit(X_train, y_train)
    #             # replaceRatio(inputdir, model, outputdir)
    #             y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #             # metrics.roc_auc_score(y_score[:,1], y_test, average='micro')
    #             # fpr, tpr, threshold = roc_curve(y_score[:,1], y_test)

    #             # metrics.roc_auc_score(y_score[:,1], y_train, average='micro')
    #             fpr, tpr, threshold = roc_curve(y_test, y_score[:,1])
    #         elif modelname == "NN":
    #             model = MLPClassifier(max_iter = 500000)
    #             # y_score = model.fit(X_train, y_train)
    #             # replaceRatio(inputdir, model, outputdir)
    #             #
    #             # metrics.roc_auc_score(y_score[:, 1], y_test, average='micro')
    #             # fpr, tpr, threshold = roc_curve(y_score[:, 1].ravel(), y_test.ravel())
    #             y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #             fpr, tpr, threshold = roc_curve(y_test, y_score[:,1])
    #         elif modelname == "Logistic Regression":
    #             model = LogisticRegression()
    #             # y_score = model.fit(X_train, y_train)
    #             y_score = model.fit(X_train, y_train).decision_function(X_test)
    #             fpr, tpr, threshold = roc_curve(y_test, y_score)
    #             # replaceRatio(inputdir, model, outputdir)
    #         elif modelname == "DecisionTree":
    #             model = tree.DecisionTreeClassifier()
    #             # y_score = model.fit(X_train, y_train)
    #             y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #             fpr, tpr, threshold = roc_curve(y_test, y_score[:,1])
    #             # replaceRatio(inputdir, model, outputdir)
    #         elif modelname == "KNN":
    #             model = KNeighborsClassifier()
    #             # y_score = model.fit(X_train, y_train)
    #             y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #             fpr, tpr, threshold = roc_curve(y_test, y_score[:, 1])
    #             # replaceRatio(inputdir, model, outputdir)
    #         elif modelname == "AdaBoost":
    #             model = AdaBoostClassifier()
    #             # y_score = model.fit(X_train, y_train)
    #             y_score = model.fit(X_train, y_train).decision_function(X_test)
    #             fpr, tpr, threshold = roc_curve(y_test, y_score)
    #             # replaceRatio(inputdir, model, outputdir)
    #         elif modelname == "Random Forest":
    #             model = RandomForestClassifier()
    #             # y_score = model.fit(X_train, y_train)
    #             y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #             fpr, tpr, threshold = roc_curve(y_test, y_score[:, 1])
    #             # replaceRatio(inputdir, model, outputdir)
    #         elif modelname == "GDBT":
    #             model = GradientBoostingClassifier()
    #             # y_score = model.fit(X_train, y_train)
    #             y_score = model.fit(X_train, y_train).decision_function(X_test)
    #             fpr, tpr, threshold = roc_curve(y_test, y_score)
    #             # replaceRatio(inputdir, model, outputdir)

    #         roc_auc = auc(fpr, tpr)
    #         plt.plot(fpr, tpr, lw=lw, label=modelname+" AUC="+str(round(roc_auc,3)))

    # #####################################correct###############################################
    #
    # totaldata = GenerateDataSet(inputdir, Blocks, TFlist)
    # totaldataX = totaldata["x"]
    # totaldataY = totaldata["y"]
    # # random_state = np.random.RandomState(0)
    # X_train = totaldataX
    # y_train = totaldataY
    # X_train, X_test, y_train, y_test = train_test_split(totaldataX, totaldataY, test_size=0.3,
    #                                                     random_state=0)  # NEED CHANGE FOR AUC
    # # lr = LogisticRegression(C=1)
    # # y_score =lr.fit(X_train, y_train).decision_function(X_test)
    # # = lr
    # # plt.figure()
    # lw = 2
    # plt.figure(figsize=(10, 10))

    # for modelname in ["SVM", "GaussianNB", "NN", "Logistic Regression"]:
    #     # for modelname in ["SVM"]:
    #     outputdir = "./journalresult/" + modelname
    #     if not os.path.exists(outputdir):
    #         os.mkdir(outputdir)
    #     if modelname == "SVM":
    #         model = svm.SVC(kernel='rbf', gamma=0.8, probability=True)

    #         # y_score = model.fit(X_train, y_train)
    #         # replaceRatio(inputdir, model, outputdir)
    #         y_score = model.fit(X_train, y_train).decision_function(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score)

    #     elif modelname == "GaussianNB":
    #         model = sklearn.naive_bayes.GaussianNB()
    #         # y_score = model.fit(X_train, y_train)
    #         # replaceRatio(inputdir, model, outputdir)
    #         y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score[:, 1])
    #     elif modelname == "NN":
    #         model = MLPClassifier(max_iter=500000)
    #         # y_score = model.fit(X_train, y_train)
    #         # replaceRatio(inputdir, model, outputdir)
    #         #
    #         y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score[:, 1])
    #     elif modelname == "Logistic Regression":
    #         model = LogisticRegression()
    #         # y_score = model.fit(X_train, y_train)
    #         y_score = model.fit(X_train, y_train).decision_function(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score)
    #         replaceRatio(inputdir, model, outputdir)
    #     elif modelname == "DecisionTree":
    #         model = tree.DecisionTreeClassifier()
    #         # y_score = model.fit(X_train, y_train)
    #         y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score[:, 1])
    #         # replaceRatio(inputdir, model, outputdir)
    #     elif modelname == "KNN":
    #         model = KNeighborsClassifier()
    #         # y_score = model.fit(X_train, y_train)
    #         y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score[:, 1])
    #         # replaceRatio(inputdir, model, outputdir)
    #     elif modelname == "AdaBoost":
    #         model = AdaBoostClassifier()
    #         # y_score = model.fit(X_train, y_train)
    #         y_score = model.fit(X_train, y_train).decision_function(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score)
    #         # replaceRatio(inputdir, model, outputdir)
    #     elif modelname == "Random Forest":
    #         model = RandomForestClassifier()
    #         # y_score = model.fit(X_train, y_train)
    #         y_score = model.fit(X_train, y_train).predict_proba(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score[:, 1])
    #         # replaceRatio(inputdir, model, outputdir)
    #     elif modelname == "GDBT":
    #         model = GradientBoostingClassifier()
    #         # y_score = model.fit(X_train, y_train)
    #         y_score = model.fit(X_train, y_train).decision_function(X_test)
    #         fpr, tpr, threshold = roc_curve(y_test, y_score)
    #         # replaceRatio(inputdir, model, outputdir)

    #     roc_auc = auc(fpr, tpr)
    #     plt.plot(fpr, tpr, lw=lw, label=modelname + " AUC=" + str(round(roc_auc, 3)))

    
    #     # plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    #     plt.xlim([0.0, 1.0])
    #     plt.ylim([0.0, 1.05])
    #     plt.xlabel('False Positive Rate',fontsize=22)
    #     plt.ylabel('True Positive Rate',fontsize=22)
    #     # plt.title(title, fontsize=22)
    #     plt.legend(loc="lower right", prop={'size':16})

    #     # plt.savefig("C:/Users/how17003/Documents/pujan/BRCA_sub/"+title+".jpg",bbox_inches='tight')
    # plt.show()

######################################################################################################################################
    inputdir =  "./journalresult/Zratio"
    # inputdir =  "./MachineLearningPart/trainingsamples"
    blockdir  = "./testblock"
    effectsign = "./effectsign.txt"
    sampledata = "./journalresult/total.txt"
    TFlist=["IRF8","NFATC1"]
    Blocks = loadblockinformation(blockdir, effectsign)



    # inputdir = "./paper_material/datamaterial"
    # blockdir = "./testblock"
    # effectsign = "./effectsign.txt"
    # TFlist = ["IRF8", "NFATC1"]
    # Blockslist = loadblockinformation(blockdir,effectsign)
    number=0
    totaldata = GenerateDataSet(inputdir, Blocks, TFlist)
    totaldataX = totaldata["x"]
    totaldataY = totaldata["y"]
    # for block in Blockslist:
    #     number+=1
    #     print(number)
    #     Trainingblock = []
    #     Testblock = [block]
    #     CModle = CalculateModel(Block=Testblock)
    #     for B in Blockslist:
    #         if B != block:
    #             Trainingblock.append(B)
    #     Traningdata = GenerateDataSet(inputdir, Trainingblock,TFlist)
    #     X_train = Traningdata["x"]
    #     y_train = Traningdata["y"]
    X_train = totaldataX
    y_train = totaldataY
        # for modelname in ["SVM", "GaussianNB", "NN", "Logistic Regression"]:
    for modelname in ["SVM", "GaussianNB", "NN", "Logistic Regression"]:
        # for modelname in ["NN"]:
            print(modelname)
            outputdir = inputdir+"_"+modelname
            if not os.path.exists(outputdir):
                os.mkdir(outputdir)
            if modelname == "SVM":
                model = svm.SVC(kernel='rbf', gamma=0.8, probability=True)
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
    
            elif modelname == "GaussianNB":
                model = sklearn.naive_bayes.GaussianNB()
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
    
            elif modelname == "NN":
                model = MLPClassifier(max_iter=500000)
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
    
            elif modelname == "Logistic Regression":
                model = LogisticRegression()
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
            elif modelname == "DecisionTree":
                model = tree.DecisionTreeClassifier()
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
            elif modelname == "KNN":
                model = KNeighborsClassifier()
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
            elif modelname == "AdaBoost":
                model = AdaBoostClassifier()
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
            elif modelname == "Random Forest":
                model = RandomForestClassifier()
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
                # replaceRatio(inputdir, model, outputdir)
            elif modelname == "GDBT":
                model = GradientBoostingClassifier()
                y_score = model.fit(X_train, y_train)
                replaceRatio(inputdir, model, outputdir)
            # ComparisonParirlist = loadsamplefile(outputdir)
            # SamplesScore = {}
            # for CP in ComparisonParirlist:
            #     SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)
            # outputfile = outputdir+"_score.txt"
            # with open(outputfile, "w") as file:
            #     line = "result"
            #     for Samplename, score in SamplesScore.items():
            #         # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
            #         # line += "\t" + Samplename + "\t" + Samplename + "_pval"
            #         line += "\t" + Samplename
            #     line += "\n"
            #     # line = ""
            #     for block in Testblock:
            #         line += block["name"]
            #         for Samplename, score in SamplesScore.items():
            #             line += "\t" + str(score[block["name"]]["score"])
            #             # line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
            #             #     score[block["name"]]["pval"])
            #         line += "\n"
            #     file.write(line)
        # socreMatrix[blockgene["id"]] = {}
        # ComparisonParirlist = loadsamplefile("./paper_material/datamaterial")
        # # for modelname in ["SVM","GaussianNB","NN","Logistic Regression"]:
        # for modelname in ["SVM","GaussianNB","NN","Logistic Regression"]:
        #     outputdir = "./paper_material/FIG7/"+modelname+"_revised.txt"
        #     SamplesScore = {}
        #     for CP in ComparisonParirlist:
        #         SamplesScore["revised_"+CP.getname()] = {}
        #         SamplesScore["revised_"+CP.getname()]["effect"] = CP.geteffect()
        #     addfile = "./paper_material/FIG7/"+modelname+"_add.txt"
        #     with open(outputdir,"w") as Tscorefile:
        #         for block in Blockslist:
        #             scorefile = "./paper_material/FIG7/"+modelname+"_revised_"+block["name"]+"_score.txt"
        #             linenumber = 0
        #             with open(scorefile, "r") as file:
        #                 for line in file.readlines():
        #                     if linenumber==0:
        #                         namelist = line.strip().split("\t")[1:]
        #                         linenumber+=1
        #                     else:
        #                         line = line.strip()
        #                         Tscorefile.write(line+"\n")
        #                         scorelist = line.strip().split("\t")[1:]
        #                 for i in range(len(namelist)):
        #                     SamplesScore[namelist[i]][block["name"]] = {}
        #                     SamplesScore[namelist[i]][block["name"]]["name"] = block["name"]
        #                     SamplesScore[namelist[i]][block["name"]]["score"] = float(scorelist[i])
            # CalculateFunctionalGroupScore.evaluateresult("./effectSign.txt", SamplesScore, Blockslist, addfile)
# #



