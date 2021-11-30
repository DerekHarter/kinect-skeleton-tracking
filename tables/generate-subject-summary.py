#!/usr/bin/env python
"""Generate a LaTeX table summarizing all participants
run so far, with information about the date run
and mean displacement observed for some joints for the
participants.
"""
import argparse
import pandas as pd


# other global constants / locations.  parameterize these if we need
# flexibility to specify them on command line or move them around
table_dir = '.'
description = """
This script will generate a table summarizing all participants
run so far, with information about the date and condition
when run, and average accuracy and reaction time.
"""

def generate_subject_summary_df(data_file):
    """Generate summary dataframe of experimental subjects

    Parameters
    ----------
    data_file - The name of the data file to open and load in for processing.
      Expected to be a csv file suitable for load by pandas read_csv.

    Returns
    -------
    subject_summary_df - Returns a pandas dataframe summarizing the
      experiment subjects / participants.
    """
    # load input data frame
    df = pd.read_csv(data_file)

    # drop some features from summary data file, only display useful
    # features in the table
    drop_columns = [
        'startTime',
        'endTime',
        'endDate',
        'minHeadDisplacement',
        'maxHeadDisplacement',
        'meanHeadDisplacement',
        'minTorsoDisplacement',
        'maxTorsoDisplacement',
        'meanTorsoDisplacement',
    ]
    df = df.drop(drop_columns, axis=1)

    # format datetime for table
    df['startDate'] = pd.to_datetime(df['startDate']).dt.strftime('%Y-%m-%d %H:%M')

    # change the rates to cm / seconds
    df['rateHeadDisplacement'] = df.rateHeadDisplacement / 10.0
    df['rateTorsoDisplacement'] = df.rateTorsoDisplacement / 10.0
    
    # rearrange column order a bit
    df = df[ ['subjectId', 'startDate', 'samples', 'rateHeadDisplacement', 'rateTorsoDisplacement'] ]
    
    # return the resulting dataframe
    return df


def save_table(subject_summary_df, output_file):
    """Create and save a generated LaTeX table of this dataframe.

    Parameters
    ----------
    subject_summary_df - A dataframe of the summarized subject information.
    output_file - The name of the file to save the table into.
    """
    caption = "Summary of experiment participants results.  Number of samples, and the head and torso displacement rates (cm / sec) during experiment are shown."
    label = "table-subject-summary"
    header = [
        'part',
        'date',
        'samples',
        'head',
        'torso',
    ]
    subject_summary_df.to_latex(output_file,
                                index=False,
                                #header=True,
                                bold_rows=False,
                                float_format="%0.4f",
                                caption=caption,
                                label=label,
                                header=header,
                                longtable=False)


def main():
    """Main entry point for this figure visualizaiton creation
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('data', 
                        help='the name of the experiment (cleaned) data file to open and process')
    parser.add_argument('--output', default=None,
                        help='name of output table, defaults to table-subject-summary.tex')
    args = parser.parse_args()

    # determine output file name if not given explicitly
    output_file = args.output
    if output_file is None:
        # make full output file name, assume .png output by default
        output_file = 'table-subject-summary.tex'


    # generate and save the table for the asked for models
    subject_summary_df = generate_subject_summary_df(args.data)
    save_table(subject_summary_df, output_file)


if __name__ == "__main__":
    main()
