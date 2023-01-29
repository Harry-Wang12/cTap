

import os
import time
import CalculateFunctionalGroupScore
from multiprocessing import Process
import CrossValidation
from CalculateModel import CalculateModel
import shutil
import GenerateAndCombineCohort
import CohortNormalizationAndGenerateZ
import UpdatecomparisonWithZ


def calcualtescore(CModle,inputdir,outputfile,evaluateresultfile,Blocks):
    print("start "+ inputdir)
    ComparisonParirlist = CrossValidation.loadsamplefile(inputdir)
    SamplesScore = {}
    for CP in ComparisonParirlist:
        SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)

    CalculateFunctionalGroupScore.evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)

    with open(outputfile, "w") as file:
        line = "result"
        for Samplename, score in SamplesScore.items():
            # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
            line += "\t" + Samplename + "\t" + Samplename + "_pval"
            # line += "\t" + Samplename
        line += "\n"
        # line = ""
        for block in Blocks:
            line += block["name"]
            for Samplename, score in SamplesScore.items():
                # line += "\t" + str(score[block["name"]]["score"])
                line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
                    score[block["name"]]["pval"])
            line += "\n"

        file.write(line)

def calcualtescoreraw(totaldir,CModle, Method, outputfile, evaluateresultfile, Blocks,BM,BG,WM,WG,TM,TG):
    inputdir = "./new_datamaterial"
    ComparisonParirlist = CrossValidation.loadsamplefile(inputdir)
    outputdir = totaldir + "/revised" + "_" +str(BM) + "_" + str(WM)+ "_" + str(TM)+ "_" + str(BG) + "_" + str(WG)+ "_" + str(TG)+ "_"+str(Method)+"/"
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    print("write: " + outputdir)
    if Method == 3:
        for CP in ComparisonParirlist:
            CPR = CModle.preprocess_3(sample=CP,  BG=BG,  WP=WG,T= T)
            CPR.writerevisedresult(outputdir + "/")
    elif Method == 4:
        for CP in ComparisonParirlist:
            CPR = CModle.preprocess_4(sample=CP, BM=BM, BG=BG, WM=WM, WG=WG,TM = TM,TG = TG)
            CPR.writerevisedresult(outputdir + "/")
    elif Method == 0:
        for CP in ComparisonParirlist:
            CPR = CModle.preprocess_0(sample=CP)
            CPR.writerevisedresult(outputdir + "/")

    #################################################################################################################################################
    print("start " + outputdir)
    ComparisonParirlist = CrossValidation.loadsamplefile(outputdir)
    SamplesScore = {}
    for CP in ComparisonParirlist:
        SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)

    CalculateFunctionalGroupScore.evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)

    with open(outputfile, "w") as file:
        line = "result"
        for Samplename, score in SamplesScore.items():
            # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
            line += "\t" + Samplename + "\t" + Samplename + "_pval"
            # line += "\t" + Samplename
        line += "\n"
        # line = ""
        for block in Blocks:
            line += block["name"]
            for Samplename, score in SamplesScore.items():
                # line += "\t" + str(score[block["name"]]["score"])
                line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
                    score[block["name"]]["pval"])
            line += "\n"

        file.write(line)
    # shutil.rmtree(outputdir)




    ########################################################################################################################################
def calcualtescorerawrank(totaldir, CModle, Method, Blocks, BM, BG, WM, WG, T,blockinformation):
    inputdir = "./datamaterial/replacedDir_percentage_5_5_2_mean"
    ComparisonParirlist = CrossValidation.loadsamplefile(inputdir)
    outputdir = totaldir + "/revised" + "_" + str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG) + "_" + str(
        T) + "_" + str(Method) + "/"
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

    # print("write: " + outputdir)
    if Method == 3:
        for CP in ComparisonParirlist:
            CPR = CModle.preprocess_3(sample=CP, BG=BG, WP=WG, T=T)
            CPR.writerevisedresult(outputdir + "/")
    elif Method == 4:
        for CP in ComparisonParirlist:
            CPR = CModle.preprocess_4(sample=CP, BM=BM, BG=BG, WM=WM, WG=WG)
            CPR.writerevisedresult(outputdir + "/")
    elif Method == 0:
        for CP in ComparisonParirlist:
            CPR = CModle.preprocess_0(sample=CP)
            CPR.writerevisedresult(outputdir + "/")


    # print("start " + outputdir)
    ComparisonParirlist = CrossValidation.loadsamplefile(outputdir)
    SamplesScore = {}
    for CP in ComparisonParirlist:
        SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)

    Totalscore = CalculateFunctionalGroupScore.evaluateresultValue(blockinformation,SamplesScore,Blocks)

    # CalculateFunctionalGroupScore.evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)

    # with open(outputfile, "w") as file:
    #     line = "result"
    #     for Samplename, score in SamplesScore.items():
    #         # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
    #         line += "\t" + Samplename + "\t" + Samplename + "_pval"
    #         # line += "\t" + Samplename
    #     line += "\n"
    #     # line = ""
    #     for block in Blocks:
    #         line += block["name"]
    #         for Samplename, score in SamplesScore.items():
    #             # line += "\t" + str(score[block["name"]]["score"])
    #             line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
    #                 score[block["name"]]["pval"])
    #         line += "\n"
    #
    #     file.write(line)
    shutil.rmtree(outputdir)
    return Totalscore




    ########################################################################################################################################

if __name__ == '__main__':

    #######################################################################################################################################
    # # # #generate big table
    # unparseddir = "./journalresult/rawratio"
    # parseddir = "./journalresult/rawratio_done"
    # if not os.path.exists(parseddir):
    #     os.mkdir(parseddir)
    
    # # Totalbigfilename  = CohortTotalTable + time +.txt
    
    # Totalbigfilename = "./journalresult/CohortTotalTable.txt"
    # # now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # # Totalbigfilename += now + ".txt"
    
    # GenerateOrCombine = "Generate" # "Combine"
    # #
    # if GenerateOrCombine == "Generate":
    #     loadresult = GenerateAndCombineCohort.generatfromdir(unparseddir)
    #     GenerateAndCombineCohort.writetable(loadresult["cohorts"], loadresult["genelist"],Totalbigfilename)
    #     GenerateAndCombineCohort.MoveUnparsedToParsed(unparseddir,parseddir)
    
    
    
    # #
    # # # ########################################################################################################################################
    # # # trimed QN and get Z
    # Totalbigfilename = "./journalresult/CohortTotalTable.txt"
    # inputpath = Totalbigfilename #get from outside
    # outputpath = "./journalresult/CohortTotalTable_normalized.txt" #get from outside
    #
    
    # Cutmethod = "percentage" #"Zscore"
    # B_t = 5 #3
    # B_b = 5 #3
    #
    # # BZ_t = 3
    # # BZ_b = 3
    # method1_type = "mean" #"median"
    # method = 2 #2
    #
    # CohortNormalizationAndGenerateZ.TrimedNormalization(inputpath, outputpath, Cutmethod, B_t, B_b, method, method1_type)
    
    # Zoutputpath="./journalresult/Z_"
    # CohortNormalizationAndGenerateZ.generateZscore(outputpath,Zoutputpath)
    # # # # ########################################################################################################################################
    # # # generate new data material
    # outputdir = "./journalresult/Zratio/"
    # if not os.path.exists(outputdir):
    #     os.mkdir(outputdir)
    # matrixZfile = Zoutputpath +  "sample_Z.txt"
    # genomeZfile = Zoutputpath +  "genome_Z.txt"
    # UpdatecomparisonWithZ.AddcohortToComparsionPair(parseddir,outputdir,matrixZfile,genomeZfile)
    
    # #
    # now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    # dirpath = "./result_"+now
    # print(dirpath)
    # os.makedirs(dirpath)

    ################################################################################################################tuning############################################
    '''
    ###########################################################################################
    # Delete by mistake
    # Add when new cohor come
    #
    #############################################################################################
    '''
    # only step 5
    #
    # Blocks = CalculateFunctionalGroupScore.loadblockinformation("./testblock")
    # CModle = CalculateModel(Block=Blocks)
    # # Blocks = CalculateFunctionalGroupScore.loadblockinformation("./OCblocks_potential")
    # # reviseddir ="./revised7-20"
    # B_t=5
    # B_b=5
    # method = 2
    # method1_type="mean"
    # inputdir = "./datamaterial/replacedDir_percentage" + "_" + str(B_t) + "_" + str(B_b) + "_" + str(method) + "_" + str(method1_type)
    # Method = 4
    # outresultdir = "./result_2020_07_20/"
    # outputfile = outresultdir +"5_5_2_replacedDir_percentage_Score_" + str(Method) + "_" + str(0.5) + "_" + str(0.5) + "_" + str(0.5) + "_" + str(1.5) + ".txt"
    # CalculateFunctionalGroupScore.CalculateScore(inputdir, outputfile, outresultdir, Method, Blocks, T=0.5, mi=0.5,power=0.5, B=1.5)
    # # CalculateFunctionalGroupScore.CalculateScorebatch(inputdir, outresultdir, Blocks, Method)

    # targetgenelist = CrossValidation.loadtargetgene("./targetgene.txt")
    #
    # CModle = CalculateModel(Block=targetgenelist)
    # ComparisonParirlist = CrossValidation.loadsamplefile(inputdir)
    # CrossValidation.writerevisedCPlist(ComparisonParirlist,CModle,reviseddir)
    # Method = 4
    # # outresultdir = "./result_2020_07_21/"
    # outresultdir = "./result/"
    # l = []
    # Cutmethod = "percentage"
    # # for B_t in [5,10,15]:
    # for B_t in [5]:
    #     B_b = B_t
    #     # for method in [1,2]:
    #     for method in [2]:
    #         if method == 1:
    #             for method1_type in ["mean","median"]:
    #                 inputdir  = "./datamaterial/replacedDir_percentage"+"_"+str(B_t)+"_"+str(B_b)+"_"+str(method)+"_"+str(method1_type)
    #                 # for Method in [0, 1, 2, 3, 4]:
    # #                 Method =2
    #                 p = Process(target=CalculateFunctionalGroupScore.CalculateScorebatch,args=(inputdir, outresultdir, Blocks, Method))
    #                 p.start()
    #                 l.append(p)
    #                 # CalculateFunctionalGroupScore.CalculateScorebatch(inputdir, outresultdir, Blocks,Method)
    # #             #
    # #             #     # Method = 3 # 0,1,2,3
    # #             #     # for T in ["False",0.25,0.5,0.75,1,2]:
    # #             #     #     for mi in ["False",2,3]:
    # #             #     #         for power in ["False",0.25,0.5,0.75]:
    # #             #     #             for B in ["False",1,2,3]:
    # #             #     #                 for W in ["False",1.5,2,2.5]:
    # #             #     #                     outputfile = outresultdir+inputdir+"_Score_"+str(Method)+"_"+str(T)+"_"+str(mi)+"_"+str(power)+"_"+str(B)+"_"+str(W)+".txt"
    # #             #     #                     print(outputfile)
    # #             #     #                     CalculateFunctionalGroupScore.CalculateScore(inputdir, outputfile,outresultdir, Method, Blocks, T=T, mi=mi, power=power,B=B, W=W)
    # #             #     Method = 4
    # #             #     # BM = 2, BG = 1, WM = 1.5, WG = 2
    # #             #     for BM in [0.5,1,1.5,2,2.5]:
    # #             #         for BG in [0.5,1,1.5,2,2.5]:
    # #             #             for WM in [0.5,1,1.5,2,2.5]:
    # #             #                 for WG in [0.5,1,1.5,2,2.5]:
    # #             #                     outputfile = outresultdir + inputdir + "_Score_" + str(Method) + "_" + str(BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG) + ".txt"
    # #             #                     print(outputfile)
    # #             #                     CalculateFunctionalGroupScore.CalculateScore(inputdir, outputfile,outresultdir, Method, Blocks, T=BM, mi=BG, power=WM,B=WG, W="False")
    #         else:
    #             method1_type = "mean"
    #             inputdir = "./datamaterial/replacedDir_percentage" + "_" + str(B_t) + "_" + str(B_b) + "_" + str(method) + "_" + str(method1_type)
    #             # CalculateFunctionalGroupScore.CalculateScorebatch(inputdir, outresultdir, Blocks, Method)
    #             # CalculateFunctionalGroupScore.CalculateScorebatch(inputdir, outresultdir, Blocks)
    #             # Method = 3  # 0,1,2,3
    #             # Method = 2
    #             p = Process(target=CalculateFunctionalGroupScore.CalculateScorebatch,args=(inputdir, outresultdir, Blocks,Method))
    #             p.start()
    #             l.append(p)
    # #             # CalculateFunctionalGroupScore.CalculateScorebatch(inputdir, outresultdir, Blocks)
    # #             # # for T in ["False", 0.25, 0.5, 0.75, 1, 2]:
    # #             # #     for mi in ["False", 2, 3]:
    # #             # #         for power in ["False", 0.25, 0.5, 0.75]:
    # #             # #             for B in ["False", 1, 2, 3]:
    # #             # #                 for W in ["False", 1.5, 2, 2.5]:
    # #             # #                     outputfile = outresultdir+inputdir+"_Score_"+str(Method)+"_"+str(T)+"_"+str(mi)+"_"+str(power)+"_"+str(B)+"_"+str(W)+".txt"
    # #             # #                     print(outputfile)
    # #             # #                     CalculateFunctionalGroupScore.CalculateScore(inputdir, outputfile,outresultdir, Method, Blocks, T=T, mi=mi, power=power,B=B, W=W)
    # #             # Method = 4
    # #             # # BM = 2, BG = 1, WM = 1.5, WG = 2
    # #             # for BM in [0.5, 1, 1.5, 2, 2.5]:
    # #             #     for BG in [0.5, 1, 1.5, 2, 2.5]:
    # #             #         for WM in [0.5, 1, 1.5, 2, 2.5]:
    # #             #             for WG in [0.5, 1, 1.5, 2, 2.5]:
    # #             #                 outputfile = outresultdir + inputdir + "_Score_" + str(Method) + "_" + str(
    # #             #                     BM) + "_" + str(BG) + "_" + str(WM) + "_" + str(WG) + ".txt"
    # #             #                 print(outputfile)
    # #             #                 CalculateFunctionalGroupScore.CalculateScore(inputdir, outputfile, outresultdir,
    # #             #                                                              Method, Blocks, T=BM, mi=BG, power=WM,
    # #             #                                                              B=WG, W="False")
    # #             #
    # #             #
    # #             #
    # #             #
    # #             #
    # #             #
    # #
    # for p in l :
    #     p.join()
    #
#######################################################################################################################################
#     maxscore =0
#     Bestcase=[]
#     totaldir = "E:/reviseddata8_9_method4_v3"
#     if not os.path.exists(totaldir):
#         os.mkdir(totaldir)
#     # for Method in [3]:
#     #     if Method ==3:
#     Method = 4;
#     # if not os.path.exists(totaldir):
#     #     os.mkdir(totaldir)
#     # l=[]
#
#     # for BM in [0.5, 1,1.5]:
#     for BM in [1]:
#     # for BM in [2]:
#
#
#         # for WM in [0.26,0.275,0.28,0.29]:
#         # for WM in [0.25,0.275,0.5]:
#         for WM in [0.5,1,1.5]:
#             # for TM in [0.1,0.15,0.2]:
#             for TM in [0.5,1,1.5]:
#
#                 # for BG in [ 0.51,0.55, 0.6,0.61]:
#                 # for BG in [0.5, 1,1.5]:
#                 for BG in [0.5]:
#                     for WG in [0.5,1,1.5]:
#                         for TG in [0.5,1,1.5]:
#                             inputdir = totaldir+"/revised" + "_" + str(BM) + "_" + str(WM)+ "_" + str(TM)+ "_" + str(BG) + "_" + str(WG)+ "_" + str(TG)+"/"
#                             outputfile =  totaldir + "/Score_revised" + "_" + str(BM) + "_" + str(WM)+ "_" + str(TM)+ "_" + str(BG) + "_" + str(WG)+ "_" + str(TG) + ".txt"
#                             evaluateresultfile =  totaldir + "/Effectevaluateresult_revised" +  "_" + str(BM) + "_" + str(WM)+ "_" + str(TM)+ "_" + str(BG) + "_" + str(WG)+ "_" + str(TG) + ".txt"
#                             calcualtescoreraw(totaldir,CModle, Method, outputfile, evaluateresultfile, Blocks,BM,BG,WM,WG,TM,TG)
#     Method =0
#     inputdir = totaldir + "/revised_method_0/"
#     outputfile = totaldir + "/Score_revised_method_0.txt"
#     evaluateresultfile = totaldir + "/Effectevaluateresult_revised_method_0.txt"
#     calcualtescoreraw(totaldir, CModle, Method, outputfile, evaluateresultfile, Blocks, 0, 0, 0, 0, 0,0)
#     # os.system("shutdown -s -t  60 ")
# ###############################################################################################################################
#     outputdir = "./MachineLearningPart/8/RevisedCPprime"
#
#     print("start " + outputdir)
#     ComparisonParirlist = CrossValidation.loadsamplefile(outputdir)
#     SamplesScore = {}
#     for CP in ComparisonParirlist:
#         SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)
#     evaluateresultfile = "./MachineLearningPart/output_test_evaluate.txt"
#     CalculateFunctionalGroupScore.evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
#     outputfile = "./MachineLearningPart/output_test_socre.txt"
#     with open(outputfile, "w") as file:
#         line = "result"
#         for Samplename, score in SamplesScore.items():
#             # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
#             line += "\t" + Samplename + "\t" + Samplename + "_pval"
#             # line += "\t" + Samplename
#         line += "\n"
#         # line = ""
#         for block in Blocks:
#             line += block["name"]
#             for Samplename, score in SamplesScore.items():
#                 # line += "\t" + str(score[block["name"]]["score"])
#                 line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
#                     score[block["name"]]["pval"])
#             line += "\n"
#
#         file.write(line)

    # outputdir = "./paper_material/datamaterial"

    # print("start " + outputdir)
    # ComparisonParirlist = CrossValidation.loadsamplefile(outputdir)
    # SamplesScore = {}
    # for CP in ComparisonParirlist:
    #     SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)
    # evaluateresultfile = "./paper_material/baseline_test_evaluate.txt"
    # CalculateFunctionalGroupScore.evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
    # outputfile = "./paper_material/baseline_test_socre.txt"
    # with open(outputfile, "w") as file:
    #     line = "result"
    #     for Samplename, score in SamplesScore.items():
    #         # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
    #         line += "\t" + Samplename + "\t" + Samplename + "_pval"
    #         # line += "\t" + Samplename
    #     line += "\n"
    #     # line = ""
    #     for block in Blocks:
    #         line += block["name"]
    #         for Samplename, score in SamplesScore.items():
    #             # line += "\t" + str(score[block["name"]]["score"])
    #             line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
    #                 score[block["name"]]["pval"])
    #         line += "\n"

    #     file.write(line)
########################################################################################################################################################


    # p = Process(target=calcualtescoreraw,args=(totaldir,CModle, Method, outputfile, evaluateresultfile, Blocks,0,BG,0,WG,T))
                        # p.start()
                        # l.append(p)


    # for p in l :
    #     p.join()
    #######################################################################
    # base line
    #########################################################################


    # p = Process(target=calcualtescore, args=(CModle,inputdir,outputfile,evaluateresultfile,Blocks))
    # p.start()
    # l.append(p)
    # inputdir =  totaldir + "/parsedDir/"
    # outputfile =  totaldir + "/Score_parsedDir.txt"
    # evaluateresultfile =  totaldir + "/Effectevaluateresult_parsedDir.txt"
    # calcualtescore(CModle, inputdir, outputfile, evaluateresultfile, Blocks)
    # # p = Process(target=calcualtescore, args=(CModle, inputdir, outputfile, evaluateresultfile, Blocks))
    # # p.start()
    # # l.append(p)
    # inputdir =  totaldir + "/parsedDir_revised/"
    # outputfile =  totaldir + "/Score_parsedDir_revised.txt"
    # evaluateresultfile =  totaldir + "/Effectevaluateresult_parsedDir_revised.txt"
    # calcualtescore(CModle, inputdir, outputfile, evaluateresultfile, Blocks)
    # p = Process(target=calcualtescore, args=(CModle, inputdir, outputfile, evaluateresultfile, Blocks))
    # p.start()
    # l.append(p)
    #

################################################################################################################################################
    #
    #
    # #
    # for inputdirpath in ["Baseline","LRrevised","NBrevised","NNrevised","SVMrevised","revised_0.5_0.25_0.2_0.5_1.25_0.1_4"]:
    #
    #     print(inputdirpath)
    #     inputdir = "./paperresult/"+inputdirpath
    #     ComparisonParirlist = CrossValidation.loadsamplefile(inputdir)
    #     SamplesScore = {}
    #     for CP in ComparisonParirlist:
    #         SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)
    #     evaluateresultfile = "./paperresult/"+inputdirpath+"_combine.txt"
    #     CalculateFunctionalGroupScore.evaluateresult("./effectSign.txt", SamplesScore, Blocks, evaluateresultfile)
    #     outputfile = "./paperresult/"+inputdirpath+"_Score.txt"
    #     with open(outputfile, "w") as file:
    #         line = "result"
    #         for Samplename, score in SamplesScore.items():
    #             # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
    #             # line += "\t" + Samplename + "\t" + Samplename + "_pval"
    #             line += "\t" + Samplename
    #         line += "\n"
    #         # line = ""
    #         for block in Blocks:
    #             line += block["name"]
    #             for Samplename, score in SamplesScore.items():
    #                 line += "\t" + str(score[block["name"]]["score"])
    #                 # line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
    #                 #     score[block["name"]]["pval"])
    #             line += "\n"
    #
    #         file.write(line)
    #
####################################################################################################################################################################
    # Blocks = CalculateFunctionalGroupScore.loadblockinformation("./testblock")
    # CModle = CalculateModel(Block=Blocks)
    # inputdir = "./parsedDir_new"
    # ComparisonParirlist = CrossValidation.loadsamplefile(inputdir)
    # SamplesScore = {}
    # for CP in ComparisonParirlist:
    #     SamplesScore[CP.getname()] = CModle.calculateScoreMatraix(sample=CP)
    # outputfile = "IRF8_baseline_6functional_groups_Score.txt"
    # with open(outputfile, "w") as file:
    #     line = "result"
    #     for Samplename, score in SamplesScore.items():
    #         # line += "\t" + block["name"]+"_socre\t"+ block["name"]+"_pvalue"
    #         # line += "\t" + Samplename + "\t" + Samplename + "_pval"
    #         line += "\t" + Samplename
    #     line += "\n"
    #     # line = ""
    #     for block in Blocks:
    #         line += block["name"]
    #         for Samplename, score in SamplesScore.items():
    #             line += "\t" + str(score[block["name"]]["score"])
    #             # line += "\t" + str(score[block["name"]]["score"]) + "\t" + str(
    #             #     score[block["name"]]["pval"])
    #         line += "\n"
    #
    #     file.write(line)