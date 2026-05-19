# NRF1 Transcription Factor — GO Enrichment Analysis

Identification of NRF1 transcription factor binding sites in human gene promoters, followed by Gene Ontology (GO) enrichment analysis.

---

## Pipeline Overview

```
Ensembl Annotation  →  make_bed.py  →  tss.bed
                                           │
                    hg38.chrom.sizes  →  bedtools slop  →  promoters.bed
                                           │
                         hg38.fa  →  bedtools getfasta  →  promoter_sequences.fa
                                           │
                                     find_nrf1.py  →  nrf1_genes.txt
                                           │
                                    go_enrichment.R  →  plots + CSV
```

---

## Requirements

- Python 3
- R with packages: `clusterProfiler`, `org.Hs.eg.db`, `ggplot2`
- bedtools

---

## Data Requirements (not included — too large)

| File | Source |
|------|--------|
| `hg38.fa` | [UCSC Genome Browser](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/) |
| `hg38.chrom.sizes` | [UCSC Genome Browser](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/) |
| `human_gene_annotation.tsv` | [Ensembl BioMart](https://www.ensembl.org/biomart/martview) — Human genes GRCh38, attributes: Gene ID, Chromosome, Strand, TSS, Gene name |

---

## How to Run

**1. Generate TSS BED file**
```bash
python3 make_bed.py
```

**2. Extract promoter regions (500bp upstream, 100bp downstream)**
```bash
awk 'NR==FNR{chroms[$1]=1; next} $1 in chroms' hg38.chrom.sizes tss.bed > tss_filtered.bed
bedtools slop -i tss_filtered.bed -g hg38.chrom.sizes -l 500 -r 100 -s > promoters.bed
```

**3. Extract promoter sequences**
```bash
bedtools getfasta -fi hg38.fa -bed promoters.bed -name -s -fo promoter_sequences.fa
```

**4. Find NRF1 motif (GCGCNNNGCGC)**
```bash
python3 find_nrf1.py
```

**5. GO Enrichment Analysis**
```bash
Rscript go_enrichment.R
```

---

## Results

- **329,638** TSS entries extracted
- **4,868** genes with NRF1 motif hits
- **289** enriched GO Biological Process terms

| Output | Description |
|--------|-------------|
| `nrf1_genes.txt` | Genes containing NRF1 motif in promoter |
| `go_results.csv` | Full GO enrichment results table |
| `go_dotplot.png` | Dotplot of top 20 GO terms |
| `go_barplot.png` | Barplot of top 20 GO terms |
| `go_cnetplot.png` | Gene-concept network plot |

---

## NRF1 Motif

```
GCGC[ACGT]{2}GCGC
```

NRF1 (Nuclear Respiratory Factor 1) is a transcription factor that regulates genes involved in mitochondrial biogenesis and oxidative phosphorylation.