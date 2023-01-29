#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/6/2020 7:39 PM
# @Author  : honglin wang
# @File    : cohort.py
# @Software: PyCharm

class cohort:
    name = ""
    control={}
    test={}

    def __init__(self):
        self.name=""
        self.control={}
        self.test={}

    def addname(self,name):
        self.name=name

    def addvalue(self,genename,controlvalue,testvalue):
        self.control[genename.upper()]=controlvalue
        self.test[genename.upper()]=testvalue

    def getname(self):
        return self.name

    def getvalue(self,genename):
        returnlist={}
        if genename in self.control:
            returnlist["control"] = self.control[genename]
            returnlist["test"] = self.test[genename]
        else:
            returnlist["control"] = "0.0"
            returnlist["test"] = "0.0"
        return returnlist

