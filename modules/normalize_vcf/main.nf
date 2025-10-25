process NORMALIZE_VCF {
    label 'process_low'
    conda 'envs/bcftools_env.yml'

    input:
    path vcf
    path ref_genome

    output:
    path "${vcf.baseName}.norm.vcf.gz", emit: vcfs
    path "${vcf.baseName}.norm.vcf.gz.tbi", emit: tbis
    
    script:
    """
    bcftools norm -f $ref_genome -Ov -o ${vcf.baseName}.norm.vcf.gz $vcf
    tabix -p vcf ${vcf.baseName}.norm.vcf.gz
    """
}
