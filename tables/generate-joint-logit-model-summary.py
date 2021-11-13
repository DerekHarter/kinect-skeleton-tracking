#!/usr/bin/env python
"""Generate a LaTeX table summarizing logistic
model fit of torso joint displacement averages
vs. subject response (correct vs. incorrect) for all
collected particpants.
"""
import argparse
import pandas as pd
import numpy as np
import statsmodels.api as sm


# other global constants / locations.  parameterize these if we need
# flexibility to specify them on command line or move them around
table_dir = '.'
description = """
This script will generate a table summarizing the logistic
model fit of kinect torso joint displacement averages vs.
subject response (correct vs. incorrect) for all collected
participants.
"""


correct_map = {
    'no': 0.0,
    'yes': 1.0,
}


def generate_model_summary(data_file):
    """Generate summary dataframe of logistic regression model of
    participant joint data.

    Parameters
    ----------
    data_file - The name of the data file to open and load in for processing.
      Expected to be a csv file suitable for load by pandas read_csv.

    Returns
    -------
    model_summary_df - Returns statsmodel model summary summarizing the
      experiment subjects / participants.
    """
    # load in data to dataframe for processing
    df = pd.read_csv(data_file)

    # reaction times can be missing if didn't respond, drop them?
    df = df.dropna()

    # map to numeric value for scatterplot
    df['correctValue'] = df.correct.map(correct_map)
    
    # fit logistic regression to predict correct/incorrect
    # extract only data we need for model and add constant term
    # as required by statsmodels 
    y = df.correctValue
    X = df.jointTorsoDisplacement
    X = sm.add_constant(X)

    # fit the logistic regression statsmodel
    logit = sm.Logit(y, X)
    model = logit.fit()
    #model.summary()

    # return the resulting model
    return model


def save_table(model_summary, output_file):
    """Create and save a generated LaTeX table of this dataframe.

    Parameters
    ----------
    subject_summary_df - A dataframe of the summarized subject information.
    output_file - The name of the file to save the table into.
    """
    caption = "Summary of Logistic Regression model fit of Torso joint displacement vs. correct response."
    label = "table-joint-logit-model-summary"

    # get the table
    table_str = model_summary.summary().as_latex()

    # write out the table to indicated file
    f = open(output_file, 'w')
    f.write(table_str)
    f.close()


def main():
    """Main entry point for this figure visualizaiton creation
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('data', 
                        help='the name of the experiment (cleaned) data file to open and process')
    parser.add_argument('--output', default=None,
                        help='name of output table, defaults to table-joint-logit-model-summary.tex')
    args = parser.parse_args()

    # determine output file name if not given explicitly
    output_file = args.output
    if output_file is None:
        # make full output file name, assume .png output by default
        output_file = 'table-joint-logit-model-summary.tex'


    # generate and save the table for the asked for models
    model_summary = generate_model_summary(args.data)
    save_table(model_summary, output_file)


if __name__ == "__main__":
    main()
