# The "5th base"

https://www.illumina.com/science/genomics-research/articles/5-base-solution.html

The 5-base genome measures the four standard bases plus methylated cytosine as a fifth base.

![5-base](./pic/5-base.png)

## Illumina 5-base conversion chemistry

![chemistry](./pic/chemistry.png)

## Sequencing coverage recommendations for different applications

![application](./pic/application.png)

**500M paired-end reads for germline VC + Methylation:**

*   48 samples/NovaSeq X 25B
*   18 samples/NovaSeq X 10B or NovaSeq 6000 S4 
*   3 samples/NovaSeq X 1.5B

## 生信分析

![pipeline](./pic/pipeline.png)

https://help.dragen.illumina.com/product-guide/dragen-v4.4/dragen-methylation-pipeline/dragen-5base-pipeline

Methylation (5mC), Germline and Somatic variants (SNVs, Indels, CNVs, SVs(future 4.5 release of DRAGEN))

### 参数设置:
**--methylation-conversion=illumina**

### 默认分析:
Methylation is primarily identified by reference C>T mismatches on the + strand, or G>A mismatches on the – strand.
目前5-base data is only compatible with **--methylation-protocol=directional**

### Small Variant Calling:
**--enable-variant-caller=true**

### CNV Calling:

        Germline CNV Calling (depth-based): Supported for WGS; not supported for WES
        Germline CNV Calling ASCN: Not supported
        Multisample Germline CNV Calling: Not supported
        Somatic CNV Calling ASCN: Supported for WGS; not supported for WES
        Somatic CNV Calling WES: Not supported
        Cytogenetics Modality: Not supported
        CNV with SV Support: Supported

### 分析时间:
1–4 hours(30× Germline–100×/30× T/N.)

### 不同类型的胞嘧啶甲基化
| 类型 | 序列模式 | 主要分布 | 生物学意义 |
| :--- | :--- | :--- | :--- |
| **CpG** | 5'-**C G**-3' | 哺乳动物基因组 | **主要的甲基化类型**，与基因沉默、基因组印迹、X染色体失空等密切相关。 |
| **CHG** | 5'-C **H G**-3' (H=A/T/C) | 植物基因组 | 在植物中与CpG甲基化共同维持转录转座子沉默。在哺乳动物某些细胞中有非典型存在。 |
| **CHH** | 5'-C **H H**-3' (H=A/T/C) | 植物基因组 | 在植物中通常甲基化水平较低，需要被持续建立，常用于防御病毒和转座子。 |


### 6-base genome:5-hydroxymethylcytosine (5hmC) 

在很长一段时间里，科学家认为DNA甲基化（5mC）是一个相对稳定的、最终的沉默标记。然而，在2009年，两个里程碑式的研究发现，5mC可以在TET家族酶的作用下被氧化成5hmC。

### 常规甲基化生物信息分析

[nf-core/methylseq is a bioinformatics analysis pipeline used for Methylation (Bisulfite) sequencing data. It pre-processes raw data from FastQ inputs, aligns the reads and performs extensive quality-control on the results.](https://github.com/nf-core/methylseq)

| Step | Bismark workflow | bwa-meth workflow |
| :--- | :--- | :--- |
| Generate Reference Genome Index *(optional)* | Bismark | bwa-meth |
| Merge re-sequenced FastQ files | cat | cat |
| Raw data QC | FastQC | FastQC |
| Adapter sequence trimming | Trim Galore! | Trim Galore! |
| Align Reads | Bismark (bowtie2/hisat2) | bwa-meth |
| Deduplicate Alignments | Bismark | Picard MarkDuplicates |
| Extract methylation calls | Bismark | MethylDackel |
| Sample report | Bismark | - |
| Summary Report | Bismark | - |
| Alignment QC | Qualimap *(optional)* | Qualimap *(optional)* |
| Sample complexity | Preseq *(optional)* | Preseq *(optional)* |
| Project Report | MultiQC | MultiQC |

#### Bismark

![bismark](./pic/Bismark_alignment_modes.png)

#### bwa-meth
[bwa-meth:fast and accurate alignment of BS-Seq reads using bwa-mem and a 3-letter genome](https://github.com/brentp/bwa-meth)

[Pedersen B S, Eyring K, De S, et al. Fast and accurate alignment of long bisulfite-seq reads[J]. arXiv preprint arXiv:1401.1129, 2014.](https://arxiv.org/pdf/1401.1129)

### ENCODE (Encyclopedia of DNA Elements)

广泛的资源，包含大量的DNA元件（如组蛋白修饰、DNA敏感性、转录因子结合位点等）图谱。