
process MARK_DUPLICATES {
    label 'process_medium'
    conda 'envs/picard_env.yml'

    input:
    tuple path(bam), path(bai)

    output:
    tuple path("${bam.baseName}.marked.bam"), path("${bam.baseName}.marked.bam.bai")

    script:
    """
    mkdir -p tmp
    picard MarkDuplicates \
        I=${bam} \
        O=${bam.baseName}.marked.bam \
        M=tmp/marked_dup_metrics.txt \
        CREATE_INDEX=true \
        VALIDATION_STRINGENCY=SILENT \
        TMP_DIR=tmp \
        READ_NAME_REGEX=null

    cp ${bai} ${bam.baseName}.marked.bam.bai
    """
}
