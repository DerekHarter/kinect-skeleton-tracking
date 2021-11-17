#!/usr/bin/env python
import os
import os.path
import sys
import argparse
import glob
import pandas as pd
import numpy as np


# other global constants / locations.  parameterize these if we need
# flexibility to specify them on command line or move them around
data_dir = '.'
psychopy_response_file = 'task-switching-replication.csv'

description = """
One time use script.  Initial 13 subjects were recorded using millisecond
time stamps.  But C++ actually allows for microsecond resolution and we 
switched after discovering.  This script will take a csv file as input
with a millisecond time stamp, rename the feature and convert to
microseconds (by multiplying by 1000) and save file back out. 
"""


def fix_utc_timestamps(data_file):
    """
    Load the indicated csv data file into a data frame, 
    rename the utcMillisecondsSinceEpoch feature to
    utcMicrosecondsSinceEpoch.  Convert all timestamps for 
    this column/feature to microseconds (16 digit time stamp).
    Then return the resulting modified dataframe.
    """
    # get the dataframe
    df = pd.read_csv(data_file)

    # rename the feature
    feature_map = {
        'utcMillisecondsSinceEpoch': 'utcMicrosecondsSinceEpoch',
    }
    df = df.rename(columns=feature_map)

    # make the new feature column into microseconds by multiplying by
    # 1000, this will increase the time stamp to 16 digits as expected
    # for a microseconds since epoch time stamp, though of course we have
    # lost the actual last 3 digits since they were not recorded in original
    # experiment
    df['utcMicrosecondsSinceEpoch'] = df.utcMicrosecondsSinceEpoch * 1000

    # return resulting dataframe
    return df


def save_fixed_timestamps(output_file, df):
    """
    Save the given dataframe back to indicated file.
    """
    df.to_csv(output_file, index=False)
    
    
def main():
    """Main entry point for this script
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input', default='input.csv',
                        help='name of  data file to process, defaults to input.csv')
    args = parser.parse_args()

    # extract the trials and experiment data from the raw files
    df = fix_utc_timestamps(args.input)
    save_fixed_timestamps(args.input, df)


if __name__ == "__main__":
    main()
