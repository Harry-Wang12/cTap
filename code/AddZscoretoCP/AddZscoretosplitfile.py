
import os

import time
import CohortNormalizationAndGenerateZ
import UpdatecomparisonWithZ
import GenerateAndCombineCohort





if __name__ == "__main__":
    Totalbigfilename = "./CohortTotalTable_"
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    Totalbigfilename += now + ".txt"


    log2ratiodir = "./rawratio"
    log2ratiowithZdir = "./datamaterial"
    Zoutputpath="./Z_"


    loadresult = GenerateAndCombineCohort.generatfromdir(log2ratiodir)
    GenerateAndCombineCohort.writetable(loadresult["cohorts"], loadresult["genelist"],Totalbigfilename)

    if not os.path.exists(log2ratiowithZdir):
        os.mkdir(log2ratiowithZdir)


    CohortNormalizationAndGenerateZ.generateZscore(Totalbigfilename,Zoutputpath)
    matrixZfile = Zoutputpath +  "sample_Z.txt"
    genomeZfile = Zoutputpath +  "genome_Z.txt"

    UpdatecomparisonWithZ.AddcohortToComparsionPair(log2ratiodir,log2ratiowithZdir,matrixZfile,genomeZfile)