import argparse
import os
import yaml

#import sys


# Parse arguments
def file_exists(filepath):
    if not os.path.isfile(filepath):
        raise argparse.ArgumentTypeError(f"File '{filepath}' does not exist.")
    return filepath

def parse_args():
    parser = argparse.ArgumentParser(description="Argument parser for assembly mapping script.")
    
    parser.add_argument("-c",
                        "--config",
                        type=file_exists,
                        required=True,
                        help="Path to the mapping file.")
    parser.add_argument("-o",
                        "--out_prefix",
                        type=str,
                        required=True,
                        help="Prefix for subsampled reads.")
    parser.add_argument("-l",
                        "--log_name",
                        type=str,
                        default="mocktailer.log",
                        help="Path to write log to.")
    
    
    return parser.parse_args()

# Parse config-file
def parse_config(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    total_bases = config.get("total_bases")
    if total_bases is None:
        raise ValueError("Missing 'total_bases' in config.")

    samples = config.get("samples")
    if not samples:
        raise ValueError("No samples defined in config.")

    sample_dict= {}
    for name, info in samples.items():
        abundance = info.get("abundance")
        R1 = info.get("R1")
        R2 = info.get("R2")

        sample_dict[name] = {
            "R1": R1,
            "R2": R2,
            "abundance": abundance,
            "bases_to_sample": int(total_bases * abundance)
        }

    return total_bases, sample_dict

