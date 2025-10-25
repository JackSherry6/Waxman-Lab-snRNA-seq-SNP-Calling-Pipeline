process VARIANT_FILTERING {
    label 'process_medium'
    conda 'envs/bcftools_env.yml'
    publishDir params.outdir, mode:'copy'

    input:
    path vcf

    output:
    path("${vcf.baseName}_filtered.vcf")

    script:
    """
    bcftools view -i '
        QUAL > 20 && 
        FORMAT/DP > 5 && 
        SAF > 0 && SAR > 0 && 
        MQM > 30 && 
        MQMR > 30
    ' ${vcf} -Ov -o ${vcf.baseName}_filtered.vcf
    """
}
