# cTAP: A Machine Learning Framework for Predicting Target Genes of a Transcription Factor using a Cohort of Gene Expression Data Sets

## Abstract 
### Background
Interferon regulatory factor-8 (IRF8) and nuclear factor-activated T cells c1 (NFATc1) are two transcription factors that have an important role in osteoclast differentiation. Thanks to ChIP-seq technology, scientists can now estimate potential genome-wide target genes of IRF8 and NFATc1 (Fig. 1.). However, finding target genes that are consistently up-regulated or down-regulated across different studies is hard because it requires analysis of a large number of high-throughput expression studies from a comparable context.<br>
<br>
![image](https://user-images.githubusercontent.com/114254986/215354217-d9d4381d-3614-47b8-b0ac-235cde8c4a42.png)<br>
*Fig. 1. Osteoclast differentiation pathway diagram including IRF8, NFATc1 and functional groups of marker genes*




### Method
We have developed a machine learning based method, called, Cohort-based TF target prediction system (cTAP) to overcome this problem (Fig. 2.). This method assumes that the pathway involving the transcription factors of interest is featured with multiple “functional groups” of marker genes pertaining to the concerned biological process. It uses two notions, Gene-Present Sufficiently (GP) and Gene-Absent Insufficiently (GA), in addition to log2 fold changes of differentially expressed genes for the prediction. Target prediction is made by applying multiple machine-learning models (including SVM, logistic regression, neural netowrk, naive bayes), which learn the patterns of GP and GA from log2 fold changes and four types of Z scores from the normalized cohort’s gene expression data. The learned patterns are then associated with the putative transcription factor targets to identify genes that consistently exhibit Up/Down gene regulation patterns within the cohort. We applied this method to 11 publicly available GEO data sets related to osteoclastgenesis.<br>
  <br>

![image](https://user-images.githubusercontent.com/114254986/215354237-5a525e42-2ea3-41d0-b871-3e2380353b09.png)<br>
*Fig. 2. The overall process of cTAP. The  framework is made up of three major components, assembling “Comparison-Pairs” (CPs) designed to generate a cohort of gene expression data sets specific for osteoclast differentiation, introducing “Functional Groups” into the regulatory pathway constructed to encode gene and their relationships known for osteoclastogenesis, and training and using the learning model for TF target prediction.*


### Result
Our experiment identified a small number of Up/Down IRF8 and NFATc1 target genes as relevant to osteoclast differentiation. The machine learning models using GP and GA produced NFATc1 and IRF8 target genes different than simply using a log2 fold change alone (Fig. 3). Our literature survey revealed that all predicted target genes have known roles in bone remodeling, specifically related to the immune system and osteoclast formation and functions, suggesting confidence and validity in our method.For details please check our <a href="https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-021-08159-z">paper</a>.<br>
<br>
![image](https://user-images.githubusercontent.com/114254986/215354868-b8879bde-462f-4a9e-9ae1-0f0e461bfed7.png)<br>
*Fig. 3. ROC curve of 4 different models’ prediction results using genes in FGs and random genes (SVM, logistic regression, neural netowrk, naive bayes)*


### Conclusion
cTAP was motivated by recognizing that biologists tend to use Z score values present in data sets for the analysis. However, using cTAP effectively presupposes assembling a sizable cohort of gene expression data sets within a comparable context. As public gene expression data repositories grow, the need to use cohort-based analysis method like cTAP will become increasingly important.


## Questions
<p><em>For more information please connecting honglin.wang@uconn.edu</em></p>
<p><em>For citation please check the <a href="https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-021-08159-z">here</a></p>
