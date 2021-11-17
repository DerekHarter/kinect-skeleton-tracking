#!/usr/bin/env python
"""Calculate joint displacements for kinect data.  Original data files
contain the x,y,z position of 15 skeleton joints.  We calculate the 
displacement (or movement) of each joint.  We calculate the euclidian 
distance moved between each successive measurement of the joint, and 
add this to the original data file.
"""
import os
import os.path
import sys
import argparse
import glob
import pandas as pd
import numpy as np

# disable SettingWithCopyWarning
# NOTE: this may not be safe, not 100% sure why still receive this warning
#   when using the suggested iloc[] accessor for assignment
#pd.options.mode.chained_assignment = None # default = 'warn'

# other global constants / locations.  parameterize these if we need
# flexibility to specify them on command line or move them around
data_dir = '.'

description = """
This script calculate joint displacements for kinect data.  Original
data files contain the x,y,z position of 15 skeleton joints.  We
calculate the displacement (or movement) of each joint.  We calculate
the euclidian distance moved between each successive measurement of
the joint, and add this to the original data file.
"""

joint_list = [
    'jointHead',
    'jointNeck',
    'jointLeftShoulder',
    'jointRightShoulder',
    'jointLeftElbow',
    'jointRightElbow',
    'jointLeftHand',
    'jointRightHand',
    'jointTorso',
    'jointLeftHip',
    'jointRightHip',
    'jointLeftKnee',
    'jointRightKnee',
    'jointLeftFoot',
    'jointRightFoot'
]


def process_participant_joint_data(raw_kinect_file):
    """Find all participant raw kinect joint data files and process them
    to calculate joint displacements between each recorded joint position.

    Parameters
    ----------
    raw_kinect_file - The name of the data file with original raw kinect
       joint position recordings.
    """
    # get raw joint data into data frame to process
    print('kinect joint data file: ', raw_kinect_file)
    joint_df = pd.read_csv(raw_kinect_file)

    # look out for if we got multiple users tracked, this causes problems because
    # we assume all joints for all users are not mixed together
    num_users = len(joint_df.userId.unique())
    if num_users != 1:
        print('   Error: multiple user ids detected: ', joint_df.userId.unique())
        #sys.exit(0)
        # lets try just dropping the additional user ids?
        mask = (joint_df.userId == 1)
        joint_df = joint_df[mask]

    num_samples, num_features = joint_df.shape
        
    # add columns for displacment results
    for joint in joint_list:
        name = "%sDisplacement" % joint
        joint_df[name] = np.NAN
        
    # process pairs of rows, starting at row 1 to process row 0/1
    for sample_idx in range(1, num_samples):
        # extract previous and current rows as series
        prev = joint_df.iloc[sample_idx - 1]
        curr = joint_df.iloc[sample_idx]

        # calculate all displacements
        displacement_dict = calculate_displacements(prev, curr)

        # add displacement measurements to this samples position data
        joint_df.loc[sample_idx, list(displacement_dict.keys())] = list(displacement_dict.values())
        
        # slow operation, show progress
        if sample_idx % 1000 == 0:
            print('     Processing sample %05d / %05d' % (sample_idx, num_samples),
                  end='')
            print('\b'*36, end='')
            sys.stdout.flush()

    # refresh display line so don't overwrite lines
    print('\n')

    # return the new dataframe with displacements calculated for joints
    return joint_df
        
        
def calculate_displacements(prev, curr):
    """
    Given two samples (Pandas series) with all 15 joints x,y,z values,
    calculate all displacements (euclidian distance) between the previous
    and the current joint position samples.

    Parameters
    ----------
    prev, curr - Expected to be Pandas series (e.g. rows of a data frame)
      where each sample contains expected features like jointHeadX, jointHeadY,
      and jointHeadZ for the x,y,z positions of the head joint.

    Returns
    ------
    displacement_dict - A dictionary of joints and the calculated
       displacement (movement) of that joint between the previous
       and the current position sample.
    """
    displacement_dict = {}
    for joint in joint_list:
        # calculate the distance this joint moved
        displacement = calculate_euclidian_distance(prev, curr, joint)

        # recored distance moved in dictionary for return
        jointDisplacement = '%sDisplacement' % joint
        displacement_dict[jointDisplacement] = displacement

    return displacement_dict


def calculate_euclidian_distance(prev, curr, joint):
    """Calculate the euclidian distance between the previous sampled joint 
    position and the current joint position for the indicated joint.

    Parameters
    ----------
    prev, curr - Pandas series containing sampled kinect positions for all joints.
    joint - Name of the joint, presumed that jointNameX, jointNameY, jointNameZ are
      feature names of the joint x,y,z position in the prev and curr samples

    Returns
    -------
    displacement - The calculated euclidian distance displacement between the previous
      and current positions of the joint
    """
    jointX = '%sX' % joint
    jointY = '%sY' % joint
    jointZ = '%sZ' % joint
    
    prevX = prev[jointX]
    prevY = prev[jointY]
    prevZ = prev[jointZ]
    currX = curr[jointX]
    currY = curr[jointY]
    currZ = curr[jointZ]

    # euclidian distance between prev and current x,y,z point
    displacement = np.sqrt( (prevX - currX)**2.0 + (prevY - currY)**2.0 + (prevZ - currZ)**2.0 )

    return displacement


def save_joint_displacements(data_file_name, joint_df):
    """Save new dataframe with calculated joint displacements
    to touput file as a csv formated data file.

    Parameters
    ----------
    data_file_name - name to save extracted data file to
    joint_df - a pandas dataframe of joint position data along with the newly
      calculated joint displacements for all of the sampled positions.
    """
    joint_df.to_csv(data_file_name, index=False)

    
def main():
    """Main entry point for this figure visualizaiton creation
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--output', default='joint-displacements.csv',
                        help='name of output data file, defaults to joint-displacements.csv')
    parser.add_argument('--input', default='raw-kinect-joints.csv',
                        help='name of output data file, defaults to raw-kinect-joints.csv')
    args = parser.parse_args()

    # extract the trials and experiment data from the raw files
    joint_df = process_participant_joint_data(args.input)
    save_joint_displacements(args.output, joint_df)
    
if __name__ == "__main__":
    main()

    
