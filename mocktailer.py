"""Simulate a metagenome from single isolate sequence data"""

from parsers import *
from Bio import SeqIO
from Bio import SeqRecord
import random
import os

def subsample_reads(r1, r2, target_bases):
    """Randomly subsample paired-end reads until target_bases is reached."""
    assert os.path.exists(r1), "read_file 1 is missing"
    assert os.path.exists(r2), "read_file 2 is missing"

    r1_records = list(SeqIO.parse(r1, "fastq"))
    r2_records = list(SeqIO.parse(r2, "fastq"))
    assert len(r1_records) == len(r2_records), "R1 and R2 must have the same number of reads"
    
    indices = list(range(len(r1_records)))
    random.shuffle(indices)
    
    bases_sampled = 0
    selected_r1 = []
    selected_r2 = []

    for idx in indices:
        if bases_sampled >= target_bases:
            break
        selected_r1.append(r1_records[idx])
        selected_r2.append(r2_records[idx])
        # Add the length of both reads (assuming same length, or sum both)
        bases_sampled += len(r1_records[idx].seq) + len(r2_records[idx].seq)
    return selected_r1, selected_r2



if __name__ == '__main__':
    args = parse_args() # Get arguments
    samples = parse_config(args.config)

    # Iterate through samples
    for sample in samples:
        print(sample)

        R1 = samples[sample]["R1"]
        R2 = samples[sample]["R2"]
        print(R1)
        print(R2)
        target_bases = samples[sample]["bases_to_sample"]

        R1s, R2s = subsample_reads(r1 = R1,
                               r2 = R2,
                               target_bases = target_bases)
        
        print(R1s)