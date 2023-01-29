#!/usr/bin/env python
#-*- coding:utf-8 _*-  
""" 
@author:honglin 
@file: VennDigram.py 
@time: 2020/08/27
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
from matplotlib import pyplot as plt
from matplotlib_venn import venn3
import numpy as np

# venn3(subsets={'000':1,'001':2,'011':3,'100':4,'101':5,'110':6,'111':7,'010':8},set_labels=("SVM_combine","NN_combine","Baseline_combine"),set_colors=('r','g','b'))
# plt.show()

figure, axes = plt.subplots(1, 1,figsize=(20,13))

# IRF8SVMup=["AIF1","BID","CASP1","CTPS2","H2-M3","IRF5","LSP1","SLC15A3","TLR6"]
# IRF8SVMdown=["NDUFS7","PARP8","NUDT13","MCRS1","COX15","ATP5L","ALG9"]

# IRF8NNup=["AIF1","BID","CTPS2","MARCKS","RNASE4","H2-M3","SLC15A3","NOTCH1","LSP1"]
# IRF8NNdown=["NDUFS7","RAB3IP","NUDT13","MCRS1","TAP2","COX15","ATP5"]

# IRF8log2up = ["AIF1","CD164","MARCKS","MEF2C","RNASE4","TLR6","LSP1"]
# IRF8log2down=["NDUFS7","RAB3IP","NUDT13","MCRS1","COX15","ATP5L"]

# IRF8SVM = IRF8SVMup+IRF8SVMdown

# IRF8NN = IRF8NNup+IRF8NNdown

# IRF8log2=IRF8log2up+IRF8log2down


# log2 SVM NN

#IRF8 all
#IRF8 UP
# list111= len([i for i in IRF8SVM if i in IRF8NN and i in IRF8log2])
# list011 = len([i for i in IRF8SVM if i in IRF8NN]) - list111
# list101 = len([i for i in IRF8log2 if i in IRF8NN]) - list111
# list110 = len([i for i in IRF8log2 if i in IRF8SVM]) - list111
# list001 = len(IRF8NN)-list111-list011 -list101
# list010 = len(IRF8SVM)-list111-list011 -list110
# list100 = len(IRF8log2)-list111-list101 -list110
# allsubsets={
# '001':1045,
# '011':3,
# '100':93-28,
# '101':28,
# '110':0,
# '111':0,
# '010':25-3,
# }
# venn3(subsets=allsubsets,set_labels=("AD","SCSIM","NASH"),set_colors=('r','g','b'))


# #IRF8 UP
# list111= len([i for i in IRF8SVMup if i in IRF8NNup and i in IRF8log2up])
# list011 = len([i for i in IRF8SVMup if i in IRF8NNup]) - list111
# list101 = len([i for i in IRF8log2up if i in IRF8NNup]) - list111
# list110 = len([i for i in IRF8log2up if i in IRF8SVMup]) - list111
# list001 = len(IRF8NNup)-list111-list011 -list101
# list010 = len(IRF8SVMup)-list111-list011 -list110
# list100 = len(IRF8log2up)-list111-list101 -list110
# allsubsets={
# '001':list001,
# '011':list011,
# '100':list100,
# '101':list101,
# '110':list110,
# '111':list111,
# '010':list010,
# }
# venn3(subsets=allsubsets,set_labels=("log2FC only","SVM","NN"),set_colors=('r','g','b'),ax=axes[0][1])
# axes[0][1].title.set_text('Venn-diagram of IRF8 up targets')


# IRF8 DOWN
# list111= len([i for i in IRF8SVMdown if i in IRF8NNdown and i in IRF8log2down])
# list011 = len([i for i in IRF8SVMdown if i in IRF8NNdown]) - list111
# list101 = len([i for i in IRF8log2down if i in IRF8NNdown]) - list111
# list110 = len([i for i in IRF8log2down if i in IRF8SVMdown]) - list111
# list001 = len(IRF8NNdown)-list111-list011 -list101
# list010 = len(IRF8SVMdown)-list111-list011 -list110
# list100 = len(IRF8log2down)-list111-list101 -list110
# allsubsets={
# '001':list001,
# '011':list011,
# '100':list100,
# '101':list101,
# '110':list110,
# '111':list111,
# '010':list010,
# }
# venn3(subsets=allsubsets,set_labels=("log2FC only","SVM","NN"),set_colors=('r','g','b'),ax=axes[0][2])
# axes[0][2].title.set_text('Venn-diagram of IRF8 down targets')












# NFATC1SVMup=["ABCB4","ACAD10","ACADS","AP1G2","ATP5L","CIAPIN1","CNIH4","COX15","COX7A2","CYC1",
#               "DLAT","DNAJA3","DUS3L","EXT1","FAHD1","FDXR","FEM1A","HAGH","HINT3","IDH3A","IMMT",
#               "LRP-PRC","MANBAL","MCAT","MCRS1","MRPL36","MRPL38","MRPL9","MRPS34","MRPS35","NDUFB10",
#               "NDUFB5","NDUFB6","NDUFS3","NDUFS7","NS-MAF","PABPC4","PEX16","PGLS","PIGQ","PIP5K1B",
#               "PPARGC1B","PRDX3","PT-GES2","PTPN12","SEMA7A","SLC25A19","SLC39A13","SSNA1","ST5","TIMM44",
#               "TTC19","TUFM","USP4"]
# NFATC1SVMdown=["ANXA6","ATF3","CCL3","CD48","CDC42EP3","CHST12","CPEB2","DCK","EBI3","FLI1","GNG2","IRF5",
#               "IRF8","LSP1","LXN","MAP4K2","PIK3CG","SLC15A3","SLC9A3R1","SP100","TEX2","TLR6","TNFSF9","ZFP90"]

# NFATC1NNup=["ABCB4","ACAD10","ACADS","AK2","AP1G2","ATP5G3","ATP5L","BCAT2","CIAPIN1","COG8","COQ6","COX15","COX17",
#             "CYC1","DLAT","DNAJA3","DUS3L","ECSIT","ETFDH","EXT1","FASTK","FDXR","GSS","HAGH","HINT2","HINT3","IDH3A",
#             "LRPPRC","MANBAL","MBTPS1","MCRS1","MRPL12","MRPL38","MRPL9","MRPS25","MRPS34","MRPS35","NDUFB10","NDUFC1",
#             "NDUFS3","NDUFS7","NSMAF","NUDT8","OX-NAD1","PABPC4","PIP5K1B","PITPNM1","PPARGC1B","PRDX3","PTDSS2","PT-GES2",
#             "RABGEF1","RELB","SLC39A13","STARD7","TANK","TAX1BP3","TBRG4","TCF12","TTC19","TUFM","UBE2G1","UBLCP1","UMPS","USP4"]
# NFATC1NNdown=["ADAM15","CCL3","CD48","CHST12","CPEB2","EBI3","FLI1","GNG2","IL10RA","IRF8","LSP1","LXN","MAP4K2","MARCKS","MS4A7",
#               "NAB2","NOTCH1","NUCB2","P2RY6","POU2F2","RB1","RNASE4","RPS6KA3","SLC15A3","SLC9A3R1","SNAP29","TEX2","TMBIM1","TNFSF9"]

# NFATC1log2up = ["ABCB4","ACADM","ACADS","ACADVL","ACAT1","ACBD6","ACO2","AK2","ALDH4A1",
#                 "AP1G2","APBA3","ATP5E","ATP5G1","ATP5G2","ATP5G3","ATP5J","ATP5L","ATP6V0B",
#                 "ATP6V1C1","ATP6V1D","ATP6V1H","BCAT2","BCL2L13","BSG","C1QBP","CIAPIN1",
#                 "COMTD1","COQ6","COX15","COX5B","COX7A2","COX7A2L","CS","CTTN","CYC1","CYCS",
#                 "DLAT","DLST","ECSIT","ETFA","ETFDH","EXT1","FAHD1","FASTK","FDXR","GNB1L",
#                 "GPX4","GSS","GTF2H3","HAGH","HINT3","IDH3A","IDH3B","IK","IMMT","KIF13A",
#                 "LETM1","LRPPRC","MANBAL","MCAT","MCRS1","MDH1","MDH2","MFN2","MRPL1","MRPL14",
#                 "MRPL34","MRPL36","MRPL38","MRPL46","MRPL48","MRPL51","MRPL9","MRPS25","MRPS34",
#                 "MRPS35","MTX2","ND-UFA10","NDUFA4","NDUFA5","NDUFA6","NDUFAB1","NDUFAF1","NDUFB10",
#                 "NDUFB3","NDUFB5","NDUFB6","NDUFB7","NDUFC1","NDUFS3","NDUFS7","NDUFS8","NHEJ1",
#                 "NS-MAF","NUDT8","OGDH","OPA1","OX-NAD1","PABPC4","PGAM5","PGLS","PIGO","PIP5K1B","PITPNM1",
#                 "PPA2","PPARGC1B","PTGES2","PTPN12","PTPN9","RABGEF1","RELB","RE-PIN1","RREB1","SDHD","SLC25A11",
#                 "SLC25A19","SLC25A3","SLC25A39","SLC25A5","SLC30A6","SLC39A13","SOD2","ST5","STARD7","TANK","TARBP2",
#                 "TAX1BP3","TBC1D10B","TBRG4","TCIRG1","TERF2IP","TFRC","TIMM17A","TIMM44","TMEM60","TNFAIP3","TTC19",
#                 "TUFM","UBE2G1","UBLCP1","UQCRC1","UQCRC2","UQCRH","USP4","VDAC1","VTI1B"]
# NFATC1log2down=["CD164","CD48","CHST12","CNR2","CORO1A","EBI3","EPS15","FLI1","GCA","GNG2","IER3","IL10RA","IRF8",
#                 "LAMP1","LSP1","MARCKS","NEDD9","NUCB2","P2RY6","PKIB","POU2F2","PRKD2","RASSF5","RB1","RBM43","RNASE4",
#                 "RPS6KA3","SSBP2","TLE3","TLR6","TNFSF9","TPD52","WSB1","ZFP90"]

# NFATC1GaussianNBup = ["ACO2", "ACSL1", "DLAT", "DNAJA3", "FDXR", "GSS", "MCRS1", "NFKB2", "NFKBIE", "NUDT8", "OTUD7B", 
#                       "OXNAD1", "PPARGC1B", "PTGES2", "SARS2", "SDC1", "SEMA7A", "SLC25A39", "SLC39A13", "TARBP2", "TBRG4", "TRAF1"]
# NFATC1GaussianNBdown=["CCR5", "CDC42EP3", "CNR2", "ECE1", "GSTK1", "ICAM2", "NAB2", "PIAS3", "SORL1", "TLR6", "TNFSF9"]


# NFATC1LRup = ["ABCB4", "ACAD10", "AK2", "AP1G2", "ATOX1", "ATP5G2", "BCAT2", "DNAJA3", "DUS3L", "EXT1", "FAHD1", "FASTK", "FDXR",
#               "IDH3A", "IVNS1ABP", "MCRS1", "MFN2", "NDUFS3", "NFKBIE", "NSMAF", "OTUD7B", "OXNAD1", "PABPC4", "PPARGC1B", "PTGES2", "PTPN12", "REPIN1", 
#               "SDC1", "SEMA7A", "SERPINB8", "SLC39A13", "ST5", "STARD7", "TANK", "TARBP2", "TBRG4", "XRCC5"]
# NFATC1LRdown=[ "GSTK1", "HSPA2", "ICAM2", "NFKBIZ", "PARVG", "RASSF5", "RBM43", "SORL1", "TNFSF9"]






# NFATC1SVM = NFATC1SVMup+NFATC1SVMdown

# NFATC1NN = NFATC1NNup+NFATC1NNdown

# NFATC1log2=NFATC1log2up+NFATC1log2down



# #NFATc1 all
# #NFATC1 UP

# list111= len([i for i in NFATC1SVM if i in NFATC1NN and i in NFATC1log2])
# list011 = len([i for i in NFATC1SVM if i in NFATC1NN]) - list111
# list101 = len([i for i in NFATC1log2 if i in NFATC1NN]) - list111
# list110 = len([i for i in NFATC1log2 if i in NFATC1SVM]) - list111
# list001 = len(NFATC1NN)-list111-list011 -list101
# list010 = len(NFATC1SVM)-list111-list011 -list110
# list100 = len(NFATC1log2)-list111-list101 -list110
# allsubsets={
# '001':list001,
# '011':list011,
# '100':list100,
# '101':list101,
# '110':list110,
# '111':list111,
# '010':list010,
# }
# venn3(subsets=allsubsets,set_labels=("log2FC only","SVM","NN"),set_colors=('r','g','b'),ax=axes[1][0])
# axes[1][0].title.set_text('Venn-diagram of NFATC1 all targets')

# #NFATC1 UP
# list111= len([i for i in NFATC1SVMup if i in NFATC1NNup and i in NFATC1log2up])
# list011 = len([i for i in NFATC1SVMup if i in NFATC1NNup]) - list111
# list101 = len([i for i in NFATC1log2up if i in NFATC1NNup]) - list111
# list110 = len([i for i in NFATC1log2up if i in NFATC1SVMup]) - list111
# list001 = len(NFATC1NNup)-list111-list011 -list101
# list010 = len(NFATC1SVMup)-list111-list011 -list110
# list100 = len(NFATC1log2up)-list111-list101 -list110
# allsubsets={
# '001':list001,
# '011':list011,
# '100':list100,
# '101':list101,
# '110':list110,
# '111':list111,
# '010':list010,
# }
# venn3(subsets=allsubsets,set_labels=("log2FC only","SVM","NN"),set_colors=('r','g','b'),ax=axes[1][1])
# axes[1][1].title.set_text('Venn-diagram of NFATC1 up targets')




# # NFATC1 DOWN
# list111= len([i for i in NFATC1SVMdown if i in NFATC1NNdown and i in NFATC1log2down])
# list011 = len([i for i in NFATC1SVMdown if i in NFATC1NNdown]) - list111
# list101 = len([i for i in NFATC1log2down if i in NFATC1NNdown]) - list111
# list110 = len([i for i in NFATC1log2down if i in NFATC1SVMdown]) - list111
# list001 = len(NFATC1NNdown)-list111-list011 -list101
# list010 = len(NFATC1SVMdown)-list111-list011 -list110
# list100 = len(NFATC1log2down)-list111-list101 -list110
# allsubsets={
# '001':list001,
# '011':list011,
# '100':list100,
# '101':list101,
# '110':list110,
# '111':list111,
# '010':list010,
# }
# venn3(subsets=allsubsets,set_labels=("log2FC only","SVM","NN"),set_colors=('r','g','b'),ax=axes[1][2])
# axes[1][2].title.set_text('Venn-diagram of NFATC1 down targets')


























# # # log2 SVM NN

# # list111= len([i for i in NFATC1SVM if i in NFATC1NN and i in NFATC1log2])
# # list011 = len([i for i in NFATC1SVM if i in NFATC1NN]) - list111
# # list101 = len([i for i in NFATC1log2 if i in NFATC1NN]) - list111
# # list110 = len([i for i in NFATC1log2 if i in NFATC1SVM]) - list111
# # list001 = len(NFATC1NN)-list111-list011 -list101
# # list010 = len(NFATC1SVM)-list111-list011 -list110
# # list100 = len(NFATC1log2)-list111-list101 -list110



# # # all
# # allsubsets={
# # '001':list001,
# # '011':list011,
# # '100':list100,
# # '101':list101,
# # '110':list110,
# # '111':list111,
# # '010':list010,

# # }



# # venn3(subsets=allsubsets,set_labels=("log2FC only","SVM","NN"),set_colors=('r','g','b'))
# # plt.title("Venn-diagram of NFATc1 all targets", fontsize=18)
# # plt.show()


# # venn3(subsets={'001':2,'011':3,'100':4,'101':1,'110':4,'111':7,'010':3},set_labels=("SVM","NN","log2FC only"),set_colors=('r','g','b'))
# # plt.title("Venn-diagram of IRF8 up targets", fontsize=18)
# # plt.show()


# # venn3(subsets={'001':2,'011':3,'100':4,'101':1,'110':4,'111':7,'010':3},set_labels=("SVM","NN","log2FC only"),set_colors=('r','g','b'))
# # plt.title("Venn-diagram of IRF8 down targets", fontsize=18)
# # plt.show()



N=2
M=2


path1= "E:/archieve/cTAP/cTAP/Venn/IRF8up.png"
img1 = plt.imread(path1)

plt.subplot(N,M,1)
plt.imshow(img1,aspect='auto')
plt.title("Venn-diagram of IRF8 up targets")
plt.xticks([])
plt.yticks([])

path2= "E:/archieve/cTAP/cTAP/Venn/IRF8down.png"
img2 = plt.imread(path2)
plt.subplot(N,M,2)
plt.imshow(img2,aspect='auto')
plt.title("Venn-diagram of IRF8 down targets")
plt.xticks([])
plt.yticks([])


path3= "E:/archieve/cTAP/cTAP/Venn/NFATC1up.png"
img3 = plt.imread(path3)
plt.subplot(N,M,3)
plt.imshow(img3,aspect='auto')
plt.title("Venn-diagram of NFATC1 up targets")
plt.xticks([])
plt.yticks([])


path4= "E:/archieve/cTAP/cTAP/Venn/NFATC1down.png"
img4 = plt.imread(path4)
plt.subplot(N,M,4)
plt.imshow(img4,aspect='auto')
plt.title("Venn-diagram of NFATC1 down targets")
plt.xticks([])
plt.yticks([])


# # path5= "E:/archieve/cTAP/cTAP/VennNFATC1up.png"
# # img5 = plt.imread(path5)
# # plt.subplot(N,M,5)
# # plt.imshow(img5,aspect='auto')
# # plt.xticks([])
# # plt.yticks([])

# # path6= "E:/archieve/cTAP/cTAP/VennNFATC1down.png"
# # img6 = plt.imread(path6)
# # plt.subplot(N,M,6)
# # plt.imshow(img6,aspect='auto')
# # plt.xticks([])
# # plt.yticks([])


plt.show()
