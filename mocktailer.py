"""Simulate a metagenome from single isolate sequence data"""

from parsers import *
from Bio import SeqIO
from Bio import SeqRecord
import random
import os
import gzip

# Functions to deal with reads
def subsample_reads(r1, r2, target_bases):
    """Randomly subsample paired-end reads until target_bases is reached."""
    assert os.path.exists(r1), "read_file 1 is missing"
    assert os.path.exists(r2), "read_file 2 is missing"

    with gzip.open(r1, "rt") as r1_handle, gzip.open(r2,"rt") as r2_handle:
        r1_records = list(SeqIO.parse(r1_handle, "fastq"))
        r2_records = list(SeqIO.parse(r2_handle, "fastq"))
    
    assert len(r1_records) == len(r2_records), "R1 and R2 must have the same number of reads"
    
    indices = list(range(len(r1_records)))
    random.shuffle(indices)
    
    bases_sampled = 0
    selected_r1 = []
    selected_r2 = []

    for idx in indices: # This assumes the order of the reads are identical in the input
        if bases_sampled >= target_bases:
            break
        selected_r1.append(r1_records[idx])
        selected_r2.append(r2_records[idx])
        
        # Update bases sampled
        bases_sampled += len(r1_records[idx].seq) + len(r2_records[idx].seq)
    
    num_reads = len(selected_r1)
    return selected_r1, selected_r2, bases_sampled, num_reads

def write_reads(r1_list, r2_list, out_r1, out_r2):
    """Write paired-end reads to gzipped FASTQ files."""

    with gzip.open(out_r1, "wt") as r1_out, gzip.open(out_r2, "wt") as r2_out:
        SeqIO.write(r1_list, r1_out, "fastq")
        SeqIO.write(r2_list, r2_out, "fastq")

def write_log(log_info, total_bases, log_out):
    with open(log_out, "w") as f:
        for sample, sampled_bases, num_reads in log_info:
            abund = float(sampled_bases)/float(total_bases)
            f.write(f"{sample}: 2x{num_reads} reads subsampled for a total of {sampled_bases} bases for an estimated abundance of {abund}\n")


if __name__ == '__main__':
    args = parse_args() # Get arguments
    total_bases, samples = parse_config(args.config)
    out_prefix = args.out_prefix
    log_out = args.log_name

    # Iterate through samples
    all_R1s = []
    all_R2s = []
    log_info = []

    for sample in samples:

        R1 = samples[sample]["R1"]
        R2 = samples[sample]["R2"]
        abund = samples[sample]["abundance"]

        target_bases = samples[sample]["bases_to_sample"]

        R1s, R2s, bases_sampled, num_reads = subsample_reads(r1 = R1,
                               r2 = R2,
                               target_bases = target_bases)

        # Could implement this as as option for the tool
        # write_reads(r1_list = R1s,
        #             r2_list = R2s,
        #             out_r1 = f"{sample}_R1_sub.fq.gz",
        #             out_r2 = f"{sample}_R2_sub.fq.gz")
        
        # gather info
        log_info.append([sample,bases_sampled, num_reads])
        all_R1s.extend(R1s)
        all_R2s.extend(R2s)

    # Write all the reads collected
    write_reads(r1_list=all_R1s,
                r2_list=all_R2s,
                out_r1 = f"{out_prefix}_R1.fq.gz",
                out_r2 = f"{out_prefix}_R2.fq.gz")
    
    # write log
    write_log(log_info,
              total_bases=total_bases,
              log_out=log_out)