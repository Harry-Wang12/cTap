#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@author:honglin 
@file: grab genes.py 
@time: 2020/08/26
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
if __name__ == '__main__':
    Genename = "BST2"
    outputdir1 = "./paper_material/SVM"
    outputdir2 = "./paper_material/datamaterial"
    outputdir3 = "./paper_material/NN"
    outputfile1 = "./paper_material/SVM_compare_"+Genename+".txt"
    outputfile2 = "./paper_material/datamaterial_compare" + Genename + ".txt"
    outputfile3 = "./paper_material/NN_compare_" + Genename + ".txt"
    with open(outputfile1,"w") as output1:
        line = ""
        ComparisonParirlist = loadsamplefile(outputdir1)
        for CP in ComparisonParirlist:
            line+=CP.getname()+"\t"+CP.geteffect()+"\t"+str(CP.getratioValue(Genename))+"\n"
        output1.write(line)

    with open(outputfile2, "w") as output2:
        line = ""
        ComparisonParirlist = loadsamplefile(outputdir2)
        for CP in ComparisonParirlist:
            line += CP.getname() + "\t" + CP.geteffect() + "\t" + str(CP.getratioValue(Genename))+"\n"
        output2.write(line)

    with open(outputfile3, "w") as output3:
        line = ""
        ComparisonParirlist = loadsamplefile(outputdir3)
        for CP in ComparisonParirlist:
            line += CP.getname() + "\t" + CP.geteffect() + "\t" + str(CP.getratioValue(Genename)) + "\n"
        output3.write(line)

