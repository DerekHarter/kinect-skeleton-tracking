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


# final features desired, and order we desire them in
feature_names = [
    'userId',
    'utcMillisecondsSinceEpoch',
    
    'jointHeadX',
    'jointHeadY',
    'jointHeadZ',

    'jointNeckX',
    'jointNeckY',
    'jointNeckZ',

    'jointLeftShoulderX',
    'jointLeftShoulderY',
    'jointLeftShoulderZ',
    
    'jointRightShoulderX',
    'jointRightShoulderY',
    'jointRightShoulderZ',
    
    'jointTorsoX',
    'jointTorsoY',
    'jointTorsoZ',
    
    'jointLeftElbowX',
    'jointLeftElbowY',
    'jointLeftElbowZ',
    
    'jointRightElbowX',
    'jointRightElbowY',
    'jointRightElbowZ',
    
    'jointLeftHandX',
    'jointLeftHandY',
    'jointLeftHandZ',
    
    'jointRightHandX',
    'jointRightHandY',
    'jointRightHandZ',
    
    'jointLeftHipX',
    'jointLeftHipY',
    'jointLeftHipZ',
    
    'jointRightHipX',
    'jointRightHipY',
    'jointRightHipZ',
    
    'jointLeftKneeX',
    'jointLeftKneeY',
    'jointLeftKneeZ',
    
    'jointRightKneeX',
    'jointRightKneeY',
    'jointRightKneeZ',
    
    'jointLeftFootX',
    'jointLeftFootY',
    'jointLeftFootZ',
    
    'jointRightFootX',
    'jointRightFootY',
    'jointRightFootZ',
]

def compute_distance_head(row):
    """Helper function to apply to dataframe rows, will compute 
    head joint distance moved between this and next reported head 
    joint position.
    """
    distance = np.sqrt( 
        (row.jointHeadX - row.nextJointHeadX)**2.0 + 
        (row.jointHeadY - row.nextJointHeadY)**2.0 + 
        (row.jointHeadZ - row.nextJointHeadZ)**2.0
    )
    return distance

def compute_distance_torso(row):
    """Helper function to apply to dataframe rows, will compute 
    torso joint distance moved between this and next reported torso
    joint position.
    """
    distance = np.sqrt( 
        (row.jointTorsoX - row.nextJointTorsoX)**2.0 + 
        (row.jointTorsoY - row.nextJointTorsoY)**2.0 + 
        (row.jointTorsoZ - row.nextJointTorsoZ)**2.0
    )
    return distance



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
    
    # find files matching raw PsychoPy subject trial/data name
    file_pattern = "[0-9][0-9][0-9][0-9]_*_*_*_*_*"
    raw_data_pattern = data_dir + "/" + file_pattern + ".csv"
    raw_data_file_list = glob.glob(raw_data_pattern)
    raw_data_file_list.sort()
    for raw_data_file in raw_data_file_list:
        # ignore csv files of trial information
        if 'trials' in raw_data_file:
            continue

        print('processing file: ', raw_data_file)

        # raw skeleton tracking data file, process it
        # we get the subject id from the data file name
        subject_id = int(os.path.basename(raw_data_file).split('_')[0])
        print('subject id: ', subject_id)

        # load raw data into a dataframe
        subject_df = pd.read_csv(raw_data_file, names=feature_names)
        num_samples = subject_df.shape[0]
        start_time = subject_df.utcMillisecondsSinceEpoch[0]
        start_date = pd.to_datetime(start_time, unit='ms')
        end_time = subject_df.utcMillisecondsSinceEpoch[num_samples - 1]
        end_date = pd.to_datetime(end_time, unit='ms')

        # compute head and torso movement for now, create new rows with next
        # measurement, so can easily apply function to calculate distance
        # between current and next reported x,y,z position
        df_next = subject_df[['jointHeadX', 'jointHeadY', 'jointHeadZ', 'jointTorsoX', 'jointTorsoY', 'jointTorsoZ']].iloc[1:].reset_index(drop=True)
        df_next.columns = ['nextJointHeadX', 'nextJointHeadY', 'nextJointHeadZ', 'nextJointTorsoX', 'nextJointTorsoY', 'nextJointTorsoZ']
        subject_df = pd.merge(subject_df, df_next, left_index=True, right_index=True)
        subject_df['jointHeadDisplacement'] = subject_df.apply(compute_distance_head, axis=1)
        subject_df['jointTorsoDisplacement'] = subject_df.apply(compute_distance_torso, axis=1)
        
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
    parser.add_argument('--output', default='stroop-replication.csv',
                        help='name of output data file, defaults to stroop-replication.csv')
    args = parser.parse_args()

    # extract the trials and experiment data from the raw files
    skeleton_df = extract_task_switching_skeleton_data()
    save_task_switching_skeleton_data(args.output, skeleton_df)

if __name__ == "__main__":
    main()