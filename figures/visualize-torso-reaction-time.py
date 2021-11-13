#!/usr/bin/env python
"""Create figure visualization of torso joint displacements
as they relate to the subjects reaction time.
"""
import argparse
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd


# other global constants / locations.  parameterize these if we need
# flexibility to specify them on command line or move them around
figure_dir = '.'
description = """ This script creates a figure to visualize the 
relationship of torso joint movements (displacements) captured
from a kinect device vs. the subjects reaction time for individual
responses in a PsychoPy experiment.  We visualize other attributes 
such as if the response was correct or not in the figure.
"""


def create_torso_reaction_time_figure(data_file, output_file):
    """Create and save the plot of the torso joint movement datas
    relationship to the participants reaction time.  We also visualize
    accuracy in this figure as well.

    Parameters
    ----------
    data_file - The name of the input data file to load and process for
      figure visualization.  This is assumed to be a csv formatted file
      suitable to be read in by pandas read_csv() function.
    output_file - The resulting figure file name to create.
    """
    # load in data to dataframe for processing
    df = pd.read_csv(data_file)

    # reaction times can be missing if didn't respond, drop them?
    df = df.dropna()

    # using seaborn high-level df, visualize accuracy by posture, and
    # using the hue (color) to split by congruent/incongruent
    sb.scatterplot(
        x='jointTorsoDisplacement',
        y='reactionTime',
        hue='correct',
        style='correct', markers=['^', 'o'], size='correct', sizes=[100.00, 10.0],
        alpha=0.5,
        data=df);

    # clip x axis to better see bulk of data
    plt.xlim([0.0, 10.0])

    # add figure labels
    plt.xlabel('Average Joint Movement (torso joint)')
    plt.ylabel('reaction time (sec)')
    
    # save the resulting figure
    plt.savefig(output_file, transparent=True, dpi=300)


def main():
    """Main entry point for this figure visualizaiton creation
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('data',
                        help='the name of the input data file to load and create figure from')
    parser.add_argument('--output', default=None,
                        help='name of output figure, defaults to figure-torso-reaction-time.png')
    args = parser.parse_args()

    # determine output file name if not given explicitly
    output_file = args.output
    if output_file is None:
        # make full output file name, assume .png output by default
        output_file = 'figure-torso-reaction-time.png'

    # generate and save the figure for the asked for model
    create_torso_reaction_time_figure(args.data, output_file)


if __name__ == "__main__":
    main()
