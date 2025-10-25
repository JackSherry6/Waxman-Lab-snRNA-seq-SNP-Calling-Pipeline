
process VARIANT_CALLING {
    label 'process_medium'
    conda 'envs/freebayes_env.yml'

    input:
    tuple path(bam), path(bai)
    path(ref_fa)
    path(ref_index)

    output:
    path("${bam.baseName}.vcf")

    script:
    """
    freebayes \
        -f ${ref_fa} \
        ${bam} > ${bam.baseName}.vcf
    """

}
