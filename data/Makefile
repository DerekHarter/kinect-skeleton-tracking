DATA_DIR := .
RAW_DATA_DIR := .
SRC_DIR := .


# raw data sources
joint_position_raw_trials = $(wildcard ${RAW_DATA_DIR}/[0-9][0-9][0-9][0-9]_*-joint-positions.csv)

# displacement data files
displacement_data_files = $(patsubst %-joint-positions.csv,%-joint-positions-displacements.csv,${joint_position_raw_trials})

# extracted / cleaned targets
summary_data_files = ${DATA_DIR}/task-switching-skeleton-summary.csv ${DATA_DIR}/response-joint-displacements.csv  
target_data_files = ${summary_data_files} ${displacement_data_files}


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
${DATA_DIR}/task-switching-skeleton-summary.csv : ${SRC_DIR}/extract-task-switching-skeleton-summary.py ${displacement_data_files}
	python $< --output $@                                                                 


## response-joint-displacements.csv
##            : Extract joint displacement (or movements) from kinect
##              joint position information for each subject response made
##              in a PsychoPy experiment file.
##
${DATA_DIR}/response-joint-displacements.csv : ${SRC_DIR}/extract-response-joint-displacements.py ${displacement_data_files} task-switching-replication.csv
	python $< --output $@                                                                 


## XXXX_joint-displacements_YYYY_Mon_DD_HHMM.csv
##            : Extract joint displacement (or movements) from kinect
##              joint position information for each subject response made
##              in a PsychoPy experiment file.
##
${DATA_DIR}/%-joint-positions-displacements.csv : ${SRC_DIR}/calculate-joint-displacements.py ${DATA_DIR}/%-joint-positions.csv
	python $< --output $@ --input $(word 2,$^)


## clean      : DANGER: Remove all extracted / cleaned data files
##              Currently only removing the summary csv files, don't delete the individual
##              joint displacements as they take quite a bit of time to regenerate and
##              shouldn't need to be regenerated after initial creation.
.PHONY : clean
clean  :
	rm -rf $(summary_data_files) *~

## help       : Get all build targets supported by this build.
##
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
