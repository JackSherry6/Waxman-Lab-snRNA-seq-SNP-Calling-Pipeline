
process MERGE_VCFS{
    label 'process_low'
    conda 'envs/bcftools_env.yml'
    publishDir params.outdir, mode:'copy'

    input:
    tuple val(sample), path(vcfs)
    path(tbis)

    output:
    tuple val("$sample"), path("${sample}_merged.vcf")

    script:
    """
    bcftools merge --force-samples ${vcfs.join(' ')} -o ${sample}_merged.vcf
    """
}

