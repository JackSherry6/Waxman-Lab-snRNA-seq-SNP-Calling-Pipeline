include {SAMTOOLS_CONVERT} from './modules/samtools_convert'
include {ADD_READ_GROUPS} from './modules/add_read_groups'
include {MARK_DUPLICATES} from './modules/mark_duplicates'
include {SPLIT_READS} from './modules/split_reads'
include {VARIANT_CALLING} from './modules/variant_calling'
include {VARIANT_FILTERING} from './modules/variant_filtering'
include {NORMALIZE_VCF} from "./modules/normalize_vcf"
include {MERGE_VCFS} from "./modules/merge_vcfs"
include {EXTRACT_ALLELE_COUNTS} from "./modules/extract_allele_counts"

workflow {

    Channel
    .fromPath("${params.samples}/*.cram")
    .map { cram ->
        def crai = file("${cram}.crai")   // assume .crai has the same base name
        [cram, crai]
    }
    .set {sample_pairs}

    SAMTOOLS_CONVERT(sample_pairs)

    ADD_READ_GROUPS(SAMTOOLS_CONVERT.out)

    MARK_DUPLICATES(ADD_READ_GROUPS.out)

    SPLIT_READS(MARK_DUPLICATES.out, params.ref_genome, params.ref_index, params.ref_dict)

    VARIANT_CALLING(SPLIT_READS.out, params.ref_genome, params.ref_index)

    VARIANT_FILTERING(VARIANT_CALLING.out)

    NORMALIZE_VCF(VARIANT_FILTERING.out, params.ref_genome)

    def sample_groups = [:]
    new File(params.group_labels).eachLine { line ->
        if (line.startsWith('SampleID')) return
        def (sample, group) = line.split(',')
        sample_groups[sample] = group
    }

    merge_ch = NORMALIZE_VCF.out.vcfs
        .map { vcf_file ->
            def filename = vcf_file.getName()
            def matcher = filename =~ /_(M\d+)_/
            def sample_id = matcher ? matcher[0][1] : null
            def group = sample_groups[sample_id]
            [group, vcf_file]
        }
        .filter { it[0] != null && it[1] != null }
        .groupTuple()

    MERGE_VCFS(merge_ch, NORMALIZE_VCF.out.tbis.collect())

    EXTRACT_ALLELE_COUNTS(MERGE_VCFS.out)

}

    