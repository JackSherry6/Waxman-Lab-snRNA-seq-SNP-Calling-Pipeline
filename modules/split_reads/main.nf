
process SPLIT_READS {
    label 'process_medium'
    conda 'envs/gatk_env.yml'

    input:
    tuple path(bam), path(bai)
    path ref_fa
    path ref_fai
    path ref_dict

    output:
    tuple path("${bam.baseName}_split.bam"), path("${bam.baseName}_split.bam.bai")

    script:
    """
    gatk SplitNCigarReads \
        -R ${ref_fa} \
        -I ${bam} \
        -O ${bam.baseName}_split.bam

    samtools index ${bam.baseName}_split.bam
    """

}
