#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@author:honglin 
@file: Transpose.py 
@time: 2020/08/15
@contact: honglin.wang@uconn.edu  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
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
import pandas as pd
if __name__ == '__main__':
    inputpath = "E:/test/Small.csv"
    outputpath = "E:/test/Small_test.csv"

    df = pd.read_csv(inputpath)
    data = df.T
    data.to_csv(outputpath,header=0)