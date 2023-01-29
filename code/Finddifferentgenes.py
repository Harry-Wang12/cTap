#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@author:honglin 
@file: Finddifferentgenes.py 
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


    genelist1= []
    genelist2= []
    file1="C:/Users/whl19/Documents/Code/cTAP/journalresult/NFATC1_target/COMPARE/SVM.txt"
    file2="C:/Users/whl19/Documents/Code/cTAP/journalresult/NFATC1_target/COMPARE/ratio.txt"
    result1 = "C:/Users/whl19/Documents/Code/cTAP/journalresult/NFATC1_target/COMPARE/SVMlog2diff.txt"
    result2 = "C:/Users/whl19/Documents/Code/cTAP/journalresult/NFATC1_target/COMPARE/log2SVM.txt"


    with open(file1,"r") as file1open:
        for line in file1open.readlines():
            genelist1.append(line.strip())
    with open(file2,"r") as file2open:
        for line in file2open.readlines():
            genelist2.append(line.strip())


            
    with open(result1,"w") as result1open:
        for gene in genelist1:
            if gene not in genelist2:
                result1open.write(gene+"\n")

    with open(result2,"w") as result2open:
        for gene in genelist2:
            if gene not in genelist1:
                result2open.write(gene+"\n")
