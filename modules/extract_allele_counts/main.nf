
process EXTRACT_ALLELE_COUNTS{
    label 'process_low'
    conda 'envs/bcftools_env.yml'
    publishDir params.outdir, mode:'copy'

    input:
    tuple val(group_name), path(merged_vcf)

    output:
    path("${group_name}.txt")

    script:
    """
    #!/usr/bin/env bash

    # Get sample names as space-separated string
    samples=\$(bcftools query -l "$merged_vcf")

    # Start header
    header="CHROM\tPOS\tREF\tALT"

    # Loop over samples and add per-sample columns
    for s in \$samples; do
        header="\$header\tGT_\$s\tAD_\$s\tAF_\$s\tDP_\$s"
    done

    # Write header to output file
    echo -e "\$header" > "${group_name}.txt"

    # Append data
    bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%GT\t%AD\t%AF\t%DP]\n' "$merged_vcf" >> "${group_name}.txt"
    """
}
//bcftools query -f '%CHROM\t%POS\t%REF\t%ALT[\t%GT\t%AD\t%AF\t%DP]\n' $merged_vcf > ${group_name}.txt

