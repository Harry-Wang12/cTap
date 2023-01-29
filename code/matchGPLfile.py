#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@author:honglin 
@file: matchGPLfile.py 
@time: 2020/07/25
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
    mapfile="E:/GPL17791-1234_match.txt"
    Unmatchfile = "E:/GPL17791-1234.txt"
    matchedColumn = 2
    matchedfile = "E:/GPL17791-1234_matched.txt"
    startchar  = "#"

    maplist = {}
    with open(mapfile,"r") as mapF:
        for line in mapF.readlines():
            linedata = line.strip().split("\t")
            Mkey = linedata[0]
            Mvalue = linedata[1]
            maplist[Mkey] = Mvalue
    with open(matchedfile,"w") as outputfile:
        with open(Unmatchfile,"r") as UM:
            title = True
            for line in UM.readlines():
                if line.startswith(startchar):
                    outputfile.write(line)
                else:
                    if title:
                        outputfile.write(line)
                        title = False
                    else:
                        linedata = line.strip().split("\t")
                        if len(linedata)>=matchedColumn:
                            keycol = linedata[matchedColumn-1]
                            if keycol in maplist:
                                printline = ""
                                for D in linedata:
                                    printline+=D+"\t"
                                printline+=maplist[keycol]+"\n"
                                outputfile.write(printline)












