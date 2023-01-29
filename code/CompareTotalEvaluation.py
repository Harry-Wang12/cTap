#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/13/2020 9:51 PM
# Filename: CompareTotalEvaluation

import os



if __name__ == '__main__':
    dirpath = "./paper_material/FIG7"
    g = os.walk(dirpath)
    totalresult={}
    # outresult = dirpath+"_evaluatetotal.txt"
    methodlist = []

    for path, dir_list, file_list in g:
        for file_name in file_list:
            # if "_combine" in file_name:
            if "_add" in file_name:
                # methodnumber = file_name[:-4].strip().split("_")[7]
                methodnumber = 3
                if methodnumber not in methodlist:
                    methodlist.append(methodnumber)
                if methodnumber not in totalresult:
                    totalresult[methodnumber]={}
                    totalresult[methodnumber][file_name] = 0
                else:
                    totalresult[methodnumber][file_name] = 0
                rawfilepath = os.path.join(path, file_name)

                header = True
                print("start reading " + file_name)
                with open(rawfilepath,"r") as evaluatefile:
                    for line in evaluatefile.readlines():
                        if header:
                            header=False
                        else:
                            gainscore= int(line.strip().split("\t")[1])
                            totalresult[methodnumber][file_name] +=gainscore

    for method in methodlist:
        outresult=dirpath+"/evaluatetotal_"+str(method)+".txt"
        with open(outresult,"w") as resultfile:
            for filename,totalscore in totalresult[method].items():
                line = filename + "\t"+str(totalscore)+"\n"
                resultfile.write(line)





