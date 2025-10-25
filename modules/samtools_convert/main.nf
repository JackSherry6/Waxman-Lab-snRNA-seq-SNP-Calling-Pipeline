
process SAMTOOLS_CONVERT {
    label 'process_medium'
    conda 'envs/samtools_env.yml'

    input: 
    tuple path(cram), path(crai)

    output:
    tuple path("${cram.baseName}.bam"), path("${cram.baseName}.bam.bai")

    script:
    """
    samtools view -b -o ${cram.baseName}.bam ${cram}
    samtools index ${cram.baseName}.bam
    """
}

