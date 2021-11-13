DATA_DIR := ../data
FIGURE_DIR := .
SRC_DIR := .

# figures to generate

figures = figure-torso-reaction-time \
	figure-torso-response

figure_results := $(patsubst %, $(FIGURE_DIR)/%.png, $(figures))


## List of all valid targets in this sub project:
## ----------------------------------------------
## all        : By default run all figure generation tasks
##              if the figures are out of date.
##
.PHONY : all
all : $(figure_results)


response_joint_files = \
	response-joint-displacements
response_joint_data := $(patsubst %, $(DATA_DIR)/%.csv, $(response_joint_files))

## figure-torso-reaction-time.png
##            : Scatter plot of torso joint movement
##              as it relates to reaction time.
##
$(FIGURE_DIR)/figure-torso-reaction-time.png: $(SRC_DIR)/visualize-torso-reaction-time.py $(response_joint_data)
	python $^ --output $@


## figure-torso-response.png
##            : Scatter plot of torso joint movement
##              as it relates to reaction time.
##
$(FIGURE_DIR)/figure-torso-response.png: $(SRC_DIR)/visualize-torso-response.py $(response_joint_data)
	python $^ --output $@


## clean      : DANGER: Remove all generated figures.  Figure generation is relatively
##              quick, so actually removing and redoing all figures is not that big a deal
##              if needed.
##
.PHONY : clean
clean  :
	rm -rf $(figure_results) *~

## help       : Get all build targets supported by this build.
##
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
