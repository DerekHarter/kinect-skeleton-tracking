#!/usr/bin/env python
"""Extract joint displacement data/calculations for subject responses.
This script uses data files of subject response data from PsychoPy
experiments, and kinect joint position tracking informaiton.
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
psychopy_response_file = 'task-switching-replication.csv'

description = """
This script extracts and calculates joint movements or displacements for
subject responses.  This script uses data files of subject response data
from PsychoPy experiments, and corresponding kinect joint position tracking
information of joint positions of the subject while performing the 
experiment.  For each subject response, we use the utc time stamp to
determine which kinect joint position measurements were recorded from
the point when the cue became visible to the subject, to when they
made their response.  We calculate the movement of each joint from
one measurement to the next using the euclidian distance of the 3D
measured joint position point.  We then average the movement/displacement 
over all observed measurements for each joint of interest, and create a
new dataframe/file with the displacement measurements and needed response 
features of interest.
"""


def get_joint_df(participant):
    """
    Get the kinect joint experiment data for the given participant.
    If we need to we will cache the load of these data files as they can
    be a bit large.

    Parameters
    ----------
    participant - The participant identifier, used to determine which
       data file name to open with the corresponding kinect joint data.
    """
    # try and find the file for this participant
    file_pattern = data_dir + "/" + "%04d_task-switching-replication_*.csv" % participant
    file_list = glob.glob(file_pattern)
    if len(file_list) != 1:
        print("Error: did not find exptected file or got multiple files for pattern: <", file_pattern, ">")

    # load the file into a df if we found it
    data_file = file_list[0]
    print("kinect joint data file: ", data_file)
    #joint_df = pd.read_csv(data_file, names=feature_names)
    joint_df = pd.read_csv(data_file)

    # convert utc time stamp to seconds so we have same units as in the
    # subject response data
    joint_df['utcTime'] = joint_df.utcMillisecondsSinceEpoch / 1000.0
    
    return joint_df


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


        
def extract_response_joint_displacements():
    """
    Extract average joint displacements for each subject response.
    We expect 1 input file in the data directory with the PsychoPy
    task switching response data for all subjects.  In same data 
    directory there are also data files for each subjects experiments
    with the raw kinect joint position measurements.  Both files have
    utc time stamps with < ms accuracy from time synchronized machines.
    We use the utc time stamp of when the subject response was made, along
    with the reaction time measurement, to extract all kinect joint
    measurements from cue onset to when response is made from the kinect
    joint data for the subject.  From this we can calculate displacements
    of joints for each measurement, and overall average or sums of the
    displacements as needed.

    Returns
    -------
    df - Returns basically the original response df from the subject 
         PsychoPy response data, but with joint displacement measurements
         calculated for each response.
    """
    # First load the PsychoPy subject response data into a dataframe.
    # We will process each response from this file to get joint displacement
    # for it from the captured kinect joint sensor information
    data_file = data_dir + "/" + psychopy_response_file
    response_df = pd.read_csv(data_file)

    # add columns with initially 0 values to hold computed displacments
    response_df['jointHeadDisplacement'] = 0.0
    response_df['jointTorsoDisplacement'] = 0.0
    
    # iterate over each row, which contains a single subject response,
    # and determine average joint displacement for the response
    current_participant = 0
    for index, response in response_df.iterrows():
        #print(response.participant, response.utcTime, response.reactionTime)
        if response.participant != current_participant:
            current_participant = response.participant
            print('Processing participant: %04d' % current_participant)
            joint_df = get_joint_df(current_participant)

        # extract joint displacements for this response, we subtract
        # 1.0 seconds for delay from when cue is shown to when prompt
        # is given, and of course subtract the reactionTime as that is the
        # time from when prompt shows till when they make their response.
        response_time = response.utcTime

        # if reaction time is 0 or NaN it means they didn't respond before timeout
        # use a full 1.5 seconds as the (non)reaction time in that case
        if pd.isnull(response.reactionTime):
            start_time = response_time - 2.5
        # otherwise use their actual reaction time to determine start of trial cue
        else: 
            start_time = response_time - response.reactionTime - 1.0

        # find all rows in joint dataframe with time between start and when response given
        mask = (joint_df.utcTime >= start_time) & (joint_df.utcTime <= response_time)
        displacement_df = joint_df[mask]
        displacement_df = displacement_df.reset_index(drop=True)

        # add in columns but displaced in time by 1 so that we can easily calculate
        # movement
        next_df = displacement_df[['jointHeadX', 'jointHeadY', 'jointHeadZ', 'jointTorsoX', 'jointTorsoY', 'jointTorsoZ']].iloc[1:].reset_index(drop=True)
        next_df.columns = ['nextJointHeadX', 'nextJointHeadY', 'nextJointHeadZ', 'nextJointTorsoX', 'nextJointTorsoY', 'nextJointTorsoZ']
        displacement_df = pd.merge(displacement_df, next_df, left_index=True, right_index=True)

        # at this point the displacement dataframe has columns of the current and next joint
        # position in each row, so calculate distance that the joint moved now
        if len(displacement_df) == 0:
            print('    Error: no kinect data found: participant: ', response.participant, ' utcTime: ', response.utcTime)

        else:
            displacement_df['jointHeadDisplacement'] = displacement_df.apply(compute_distance_head, axis=1)
            displacement_df['jointTorsoDisplacement'] = displacement_df.apply(compute_distance_torso, axis=1)

            # now add the computed joint movement / displacements into the response_df
            mask = (response_df.utcTime == response_time)
            response_df.loc[mask, ['jointHeadDisplacement'] ] = displacement_df.jointHeadDisplacement.mean()
            response_df.loc[mask, ['jointTorsoDisplacement'] ] = displacement_df.jointTorsoDisplacement.mean()
    
    return response_df


def save_response_joint_displacements(data_file_name, displacement_df):
    """Save extracted data fame to output file as a csv formatted
    data file.

    Parameters
    ----------
    data_file_name - Name to save extracted data file to
    displacement_df - A pandas dataframe of the data to save
    """
    displacement_df.to_csv(data_file_name, index=False)


def main():
    """Main entry point for this figure visualizaiton creation
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--output', default='response-joint-displacements.csv',
                        help='name of output data file, defaults to response-joint-displacements.csv')
    args = parser.parse_args()

    # extract the trials and experiment data from the raw files
    displacement_df = extract_response_joint_displacements()
    save_response_joint_displacements(args.output, displacement_df)


if __name__ == "__main__":
    main()
