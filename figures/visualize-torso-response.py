#!/usr/bin/env python
"""Create figure visualization of torso joint displacements
as they relate to the subjects response for trials, correct
or incorrect.
"""
import argparse
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import numpy as np


# other global constants / locations.  parameterize these if we need
# flexibility to specify them on command line or move them around
figure_dir = '.'
description = """ This script creates a figure to visualize the 
relationship of torso joint movements (displacements) captured
from a kinect device vs. the participants response, e.g. if they
made a correct response or an incorrect response.
"""


correct_map = {
    'no': 0.0,
    'yes': 1.0,
}


def create_torso_response_figure(data_file, output_file):
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

    # map to numeric value for scatterplot
    df['correctValue'] = df.correct.map(correct_map)

    # and the y_jitter doesn't seem to be implemented as of now for
    # lmplot, so add our own jitter
    num_samples, num_features = df.shape
    jitter = df.correctValue + (np.random.randn(num_samples) * 0.03)
    df['correctValueJitter'] = jitter.copy()

    # using seaborn high-level df, visualize the joint movements
    # as they relate to the participant response
    sb.scatterplot(x='jointTorsoDisplacement', 
                   y='correctValueJitter',
                   y_jitter=0.1,
                   alpha=0.25,
                   data=df);

    # clip x axis to better see bulk of data
    plt.xlim([0.0, 10.0])

    # add in labels and fix up y axis ticks/labels
    plt.xlabel('Average Joint Movement (torso joint)')
    plt.ylabel('response correct')
    plt.yticks(ticks=[0.0, 1.0], labels=['no', 'yes'])

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
                        help='name of output figure, defaults to figure-torso-response.png')
    args = parser.parse_args()

    # determine output file name if not given explicitly
    output_file = args.output
    if output_file is None:
        # make full output file name, assume .png output by default
        output_file = 'figure-torso-response.png'

    # generate and save the figure for the asked for model
    create_torso_response_figure(args.data, output_file)


if __name__ == "__main__":
    main()
