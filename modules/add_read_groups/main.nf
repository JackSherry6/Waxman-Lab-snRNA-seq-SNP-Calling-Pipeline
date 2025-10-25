
process ADD_READ_GROUPS {
    label 'process_low'
    conda 'envs/gatk_env.yml'

    input:
    tuple path(bam), path(bai)

    output:
    tuple path("${bam.baseName}_rg.bam"), path("${bam.baseName}_rg.bam.bai")

    script:
    """
    gatk AddOrReplaceReadGroups \
        -I ${bam} \
        -O ${bam.baseName}_rg.bam \
        -RGID 1 \
        -RGLB lib1 \
        -RGPL illumina \
        -RGPU unit1 \
        -RGSM ${bam.baseName} 

    cp ${bai} ${bam.baseName}_rg.bam.bai
    """
}
