input_file = "human_gene_annotation.tsv"
output_file = "tss.bed"

with open(input_file, 'r') as f, open(output_file, 'w') as out:
    header = f.readline()  # skip header

    written = 0
    skipped = 0

    for line in f:
        cols = line.strip().split('\t')
        if len(cols) < 5:
            skipped += 1
            continue

        chrom  = "chr" + cols[1]   # e.g. 1 → chr1
        strand = "+" if cols[2] == "1" else "-"
        gene   = cols[4]

        if not gene.strip() or not chrom.strip():
            skipped += 1
            continue

        try:
            tss = int(cols[3])
        except ValueError:
            skipped += 1
            continue

        tss_end = tss + 1
        name = f"{chrom}@{tss}-{tss_end}|{gene}"
        out.write(f"{chrom}\t{tss}\t{tss_end}\t{name}\t.\t{strand}\n")
        written += 1

print(f"Done! Written: {written} entries, Skipped: {skipped}")
print(f"BED file saved to: {output_file}")
