#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:how17003
# datetime:7/12/2020 8:59 PM
# Filename: UpdatecomparisonWithZ
import os


def AddcohortToComparsionPair(replacedir,outputdir,matrixZfile,genomeZfile):

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    #     readfile

    #     readCP
    MatrixZsamplelist = {}
    GenomeZsamplelist = {}
    headersample = []

    #     matrixZ

    header = True
    with open(matrixZfile, "r") as Zfile:
        for line in Zfile.readlines():
            if header:
                headersample = line.strip().split("\t")[1:]
                for sample in headersample:
                    MatrixZsamplelist[sample] = {}
                header = False
            else:
                linedata = line.strip().split("\t")
                genename = linedata[0].upper()
                for i in range(1, len(linedata)):
                    MatrixZsamplelist[headersample[i - 1]][genename] = linedata[i]

    #     genomeZ
    header = True
    with open(genomeZfile, "r") as Zfile:
        for line in Zfile.readlines():
            if header:
                headersample = line.strip().split("\t")[1:]
                for sample in headersample:
                    GenomeZsamplelist[sample] = {}
                header = False
            else:
                linedata = line.strip().split("\t")
                genename = linedata[0].upper()
                for i in range(1, len(linedata)):
                    GenomeZsamplelist[headersample[i - 1]][genename] = linedata[i]

    g = os.walk(replacedir)
    for path,dir_list,file_list in g:
        for file_name in file_list:
            print("Start writing ",file_name)
            with open(outputdir+"/new_"+file_name,"w") as outputfile:
                with open(replacedir+"/"+file_name,"r") as inputfile:                    
                    sampleheader = True
                    for line in inputfile.readlines():
                        if line.startswith("!"):
                            printline = line.strip()+"\n"
                            outputfile.write(printline)
                        else:
                            if sampleheader:
                                linedata = line.strip().split("\t")
                                printline = "GENE\tRNA\tRawValueControl\tRawValueTest\tCohortColumnZControl\tCohortColumnZTest\tCohortGenomeZControl\tCohortGenomeZTest\t" + linedata[-1] + "\n"
                                outputfile.write(printline)
                                sampleheader = False
                            else:
                                
                                genename = line.strip().split("\t")[0].upper().replace(" ","")
                                printline = line.strip()+"\t"+MatrixZsamplelist[file_name+"_control"][genename]+"\t"+MatrixZsamplelist[file_name+"_test"][genename]+"\t"+GenomeZsamplelist[file_name+"_control"][genename]+"\t"+GenomeZsamplelist[file_name+"_test"][genename]+"\n"
                                outputfile.write(printline)





# replacedir = "./parsedDir"
# outputdir = "./replacedDir"
# matrixZfile = "./matrixZ.txt"
# genomeZfile = "./genemoZ.txt"


