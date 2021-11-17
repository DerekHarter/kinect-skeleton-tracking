#!/usr/bin/env python
"""Extract task switching skeleton tracking summary data for data analysis from
raw subject trial files
"""
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
description = """
This script extracts all task switching skeleton tracking subject
trials into a single summary file for data analysis.  The result is a tidy
data file, in csv format, with 1 skeleton join position data per
line, and normalized feature/column names.
"""


def extract_task_switching_skeleton_data():
    """
    Extract skeleton tracking data points and summarize them.  Collect
    summary by subject and date/time stamp into a single resulting
    data frame to be returned.

    Returns
    -------
    df - Returns a pandas dataframe of the extracted and cleaned
         task switching skeleton tracking summary data.
    """
    # will hold result to return
    initDf = True
    df = None
    
     # find files matching raw kinect tracker participant trial/data name
    file_pattern = "[0-9][0-9][0-9][0-9]_*-joint-positions-displacements"
    raw_data_pattern = data_dir + "/" + file_pattern + ".csv"
    raw_data_file_list = glob.glob(raw_data_pattern)
    raw_data_file_list.sort()
    for raw_data_file in raw_data_file_list:
        print('kinect joint data file: ', raw_data_file)

        # raw skeleton tracking data file, process it
        # we get the subject id from the data file name
        subject_id = int(os.path.basename(raw_data_file).split('_')[0])
        print('Processing participant: %04d' % subject_id)

        # load raw data into a dataframe
        #subject_df = pd.read_csv(raw_data_file, names=feature_names)
        subject_df = pd.read_csv(raw_data_file)
        num_samples = subject_df.shape[0]
        start_time = subject_df.utcMicrosecondsSinceEpoch[0]
        start_date = pd.to_datetime(start_time, unit='us')
        end_time = subject_df.utcMicrosecondsSinceEpoch[num_samples - 1]
        end_date = pd.to_datetime(end_time, unit='us')

        # now extract data to add to summary report
        minHeadDisplacement = subject_df.jointHeadDisplacement.min()
        maxHeadDisplacement = subject_df.jointHeadDisplacement.max()
        meanHeadDisplacement = subject_df.jointHeadDisplacement.mean()
        minTorsoDisplacement = subject_df.jointTorsoDisplacement.min()
        maxTorsoDisplacement = subject_df.jointTorsoDisplacement.max()
        meanTorsoDisplacement = subject_df.jointTorsoDisplacement.mean()
        
        subject_dict = {
            'subjectId': [subject_id],
            'samples': [num_samples],
            'startTime': [start_time],
            'startDate': [start_date],
            'endTime': [end_time],
            'endDate': [end_date],
            'minHeadDisplacement': [minHeadDisplacement],
            'maxHeadDisplacement': [maxHeadDisplacement],
            'meanHeadDisplacement': [meanHeadDisplacement],
            'minTorsoDisplacement': [minTorsoDisplacement],
            'maxTorsoDisplacement': [maxTorsoDisplacement],
            'meanTorsoDisplacement': [meanTorsoDisplacement],
        }

        if initDf:
            df = pd.DataFrame(subject_dict);
            initDf = False
        else:
            df = pd.concat([df, pd.DataFrame(subject_dict)], ignore_index=True)
            
    # return the cleaned and tidy dataframe
    # convert to America/Chicago time zone to get accurate date reports
    df.startDate = df.startDate.dt.tz_localize('UTC').dt.tz_convert('America/Chicago')
    df.endDate = df.endDate.dt.tz_localize('UTC').dt.tz_convert('America/Chicago')
    
    return df


def save_task_switching_skeleton_data(data_file_name, skeleton_df):
    """Save extracted data fame to output file as a csv formatted
    data file.

    Parameters
    ----------
    data_file_name - Name to save extracted data file to
    task_switching_replication_df - A pandas dataframe of the data to save
    """
    skeleton_df.to_csv(data_file_name, index=False)


def main():
    """Main entry point for this figure visualizaiton creation
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--output', default='task-switching-skeleton-summary.csv',
                        help='name of output data file, defaults to task-switching-skeleton-summary.csv')
    args = parser.parse_args()

    # extract the trials and experiment data from the raw files
    skeleton_df = extract_task_switching_skeleton_data()
    save_task_switching_skeleton_data(args.output, skeleton_df)

if __name__ == "__main__":
    main()
