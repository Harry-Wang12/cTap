# cTAP: A Machine Learning Framework for Predicting Target Genes of a Transcription Factor using a Cohort of Gene Expression Data Sets

# Abstract
<em>
 Identifying target genes of a transcription factor is crucial in biomedical research. Thanks to ChIP-seq technology, scientists can now estimate potential genome-wide target genes of a transcription factor. However, finding the consistently behaving Up/Down targets of a transcription factor in a given biological context is difficult because it requires analysis of a large number of high-throughput expression studies of the same or comparable context. We present a novel transcription target prediction method, called Cohort-based TF target prediction system (cTAP). This method assumes that the pathway involving the transcription factor of interest is featured with multiple functional groups of marker genes pertaining to the concerned biological process. It uses the notion of gene-presence and gene-absence in addition to log2 ratios of gene expression values for the prediction. Target prediction is made by applying multiple machine-learning models which learn the patterns of gene-presence and gene-absence from log2 ratios and four types of cohort-based gene expression Z scores from the normalized cohort’s gene expression data. The learned patterns are then associated with the putative targets of the concerned transcription factor to elicit genes exhibiting Up/Down gene regulation patterns within the cohort. We applied this method to 11 publicly available GEO data sets related to osteoclastgenesis. Our experiment uses 213 putative target genes of IRF8 identified by ChIP-Seq and produces a handful of Up/Down targets as relevant to osteoclast differentiation. The ROC curve analysis shows that the AUCs of all learned models are close to 0.9. The learned models using gene-presence and gene-absence produce target genes different from using only log2 ratios such as CASP1, BID, NOTCH1 and IRF5. Our literature survey reveals that all these predicted targets have known roles in bone remodeling, specifically related to immune and osteoclasts, suggesting confidence in our method and potential merit for a wet-lab experiment for validation.
</em>

# Work flow overview
![image](https://user-images.githubusercontent.com/114254986/215352283-b29b47a0-5327-4398-ac4f-a0fef02d91f8.png)

# Result
![image](https://user-images.githubusercontent.com/114254986/215352294-8e9175b6-738c-4138-afef-10f707424712.png)

![image](https://user-images.githubusercontent.com/114254986/215352308-174e313e-e714-4ea1-a035-343b9568bc06.png)

# Discussion

<p><em>BID</em> – Viara et al. stated that NF-B subunit RelA blocks a RANKL-induced, apoptotic JNK-BID pathway and by doing so promotes OC differentiation. Our prediction system places BID in the Up target list of IRF8 suggesting that BID may not be activated if IRF8 is suppressed. IRF8 itself plays the role of inhibiting NFATC1 for the osteoclast differentiation pathway. This discovery of the regulatory relationship between IRF8 and BID can help explain how IRF8 may have a dual role in osteoclasts by regulating apoptosis through BID and differentiation through NFATC1.</p>
<p><em>NOTCH1</em> – Regan et al. 2013  reported that Notch signaling plays context-dependent roles in the development and maintenance of many types of cells. In the skeleton, Notch signaling is responsible for proper differentiation and function of both osteoblasts and osteoclasts. Zanotti et al. 2016 pointed out that NOTCH1 has distinctive effects on inhibiting bone resorption secondary to an induction of osteoprotegerin. Our method identifies NOTCH1 in the Up target list of IRF8  suggesting a suppressive role of osteoclast differentiation, just like IRF8.</p>
<p><em>IRF5</em> – Sun et al. 2017  stated that Interferon regulatory factor (IRF5) has an important role in the differentiation of macrophages derived from mouse bone marrow. According to the SVM model IRF5 may also suppress osteoclast differentiation through the activation of IRF8. </p>
<p><em>CASP1</em> – Rocha et al. 2020 reported that CASP1 and NLRP3 deficiency increases the activity of RANKL-derived osteoclasts. When we combine both the osteoclast differentiation pathway diagram and the SVM result, CASP1 is down-regulated through IRF8 if osteoclast differentiation increases. The placement of CASP1 in the Up target of IRF8 is consistent with what has been reported by Rocha et al. 2020. </p>


# Questions
<p><em>For more information please connecting honglin.wang@uconn.edu</em></p>
<p><em>For citation please check the <a href="https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-021-08159-z">here</a></p>
