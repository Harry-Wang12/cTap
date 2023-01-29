# cTAP: A Machine Learning Framework for Predicting Target Genes of a Transcription Factor using a Cohort of Gene Expression Data Sets

## Background
Interferon regulatory factor-8 (IRF8) and nuclear factor-activated T cells c1 (NFATc1) are two transcription factors that have an important role in osteoclast differentiation. Thanks to ChIP-seq technology, scientists can now estimate potential genome-wide target genes of IRF8 and NFATc1. However, finding target genes that are consistently up-regulated or down-regulated across different studies is hard because it requires analysis of a large number of high-throughput expression studies from a comparable context.

## Method
We have developed a machine learning based method, called, Cohort-based TF target prediction system (cTAP) to overcome this problem. This method assumes that the pathway involving the transcription factors of interest is featured with multiple “functional groups” of marker genes pertaining to the concerned biological process. It uses two notions, Gene-Present Sufficiently (GP) and Gene-Absent Insufficiently (GA), in addition to log2 fold changes of differentially expressed genes for the prediction. Target prediction is made by applying multiple machine-learning models, which learn the patterns of GP and GA from log2 fold changes and four types of Z scores from the normalized cohort’s gene expression data. The learned patterns are then associated with the putative transcription factor targets to identify genes that consistently exhibit Up/Down gene regulation patterns within the cohort. We applied this method to 11 publicly available GEO data sets related to osteoclastgenesis.

## Result
Our experiment identified a small number of Up/Down IRF8 and NFATc1 target genes as relevant to osteoclast differentiation. The machine learning models using GP and GA produced NFATc1 and IRF8 target genes different than simply using a log2 fold change alone. Our literature survey revealed that all predicted target genes have known roles in bone remodeling, specifically related to the immune system and osteoclast formation and functions, suggesting confidence and validity in our method.

## Conclusion
cTAP was motivated by recognizing that biologists tend to use Z score values present in data sets for the analysis. However, using cTAP effectively presupposes assembling a sizable cohort of gene expression data sets within a comparable context. As public gene expression data repositories grow, the need to use cohort-based analysis method like cTAP will become increasingly important.

## Work flow overview
![image](https://user-images.githubusercontent.com/114254986/215352283-b29b47a0-5327-4398-ac4f-a0fef02d91f8.png)

## Result
![image](https://user-images.githubusercontent.com/114254986/215352294-8e9175b6-738c-4138-afef-10f707424712.png)

![image](https://user-images.githubusercontent.com/114254986/215352308-174e313e-e714-4ea1-a035-343b9568bc06.png)

## Discussion

<p><em>BID</em> – Viara et al. stated that NF-B subunit RelA blocks a RANKL-induced, apoptotic JNK-BID pathway and by doing so promotes OC differentiation. Our prediction system places BID in the Up target list of IRF8 suggesting that BID may not be activated if IRF8 is suppressed. IRF8 itself plays the role of inhibiting NFATC1 for the osteoclast differentiation pathway. This discovery of the regulatory relationship between IRF8 and BID can help explain how IRF8 may have a dual role in osteoclasts by regulating apoptosis through BID and differentiation through NFATC1.</p>
<p><em>NOTCH1</em> – Regan et al. 2013  reported that Notch signaling plays context-dependent roles in the development and maintenance of many types of cells. In the skeleton, Notch signaling is responsible for proper differentiation and function of both osteoblasts and osteoclasts. Zanotti et al. 2016 pointed out that NOTCH1 has distinctive effects on inhibiting bone resorption secondary to an induction of osteoprotegerin. Our method identifies NOTCH1 in the Up target list of IRF8  suggesting a suppressive role of osteoclast differentiation, just like IRF8.</p>
<p><em>IRF5</em> – Sun et al. 2017  stated that Interferon regulatory factor (IRF5) has an important role in the differentiation of macrophages derived from mouse bone marrow. According to the SVM model IRF5 may also suppress osteoclast differentiation through the activation of IRF8. </p>
<p><em>CASP1</em> – Rocha et al. 2020 reported that CASP1 and NLRP3 deficiency increases the activity of RANKL-derived osteoclasts. When we combine both the osteoclast differentiation pathway diagram and the SVM result, CASP1 is down-regulated through IRF8 if osteoclast differentiation increases. The placement of CASP1 in the Up target of IRF8 is consistent with what has been reported by Rocha et al. 2020. </p>


## Questions
<p><em>For more information please connecting honglin.wang@uconn.edu</em></p>
<p><em>For citation please check the <a href="https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-021-08159-z">here</a></p>
