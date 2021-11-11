DATA_DIR := .
RAW_DATA_DIR := .
SRC_DIR := .


# raw data sources
task_switching_skeleton_raw_trials = $(wildcard ${RAW_DATA_DIR}/[0-9][0-9][0-9][0-9]_*_*_*_*_*.csv)

# extracted / cleaned targets
target_data_files = ${DATA_DIR}/task-switching-skeleton-summary.csv


## List of all valid targets in this sub project:                                             
## ----------------------------------------------                                             
## all        : By default run all data cleaning
##              and extraction tasks.
##                                                                                            
.PHONY : all                                                                                  
all : $(target_data_files)                                                                       


## task-switching-skeleton.csv
##            : Create extracted and cleaned data from all
##              subject trials of task switching replication
##              skeleton tracking data
##
${DATA_DIR}/task-switching-skeleton-summary.csv : ${SRC_DIR}/extract-task-switching-skeleton-summary.py ${task_switching_skeleton_raw_trials}
	python $< --output $@                                                                 


## clean      : DANGER: Remove all extracted / cleaned data files
##
.PHONY : clean
clean  :
	rm -rf $(target_data_files) *~

## help       : Get all build targets supported by this build.
##
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
