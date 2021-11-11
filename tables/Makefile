DATA_DIR := ../data
TABLE_DIR := .
SRC_DIR := .

# tables to generate
tables = table-subject-summary

table_results := $(patsubst %, $(TABLE_DIR)/%.tex, $(tables))


## List of all valid targets in this sub project:
## ----------------------------------------------
## all        : By default run all table generation tasks
##              if the tables are out of date.
##
.PHONY : all
all : $(table_results)



task_switching_replication_files = \
	task-switching-skeleton-summary
task_switching_replication_data := $(patsubst %, $(DATA_DIR)/%.csv, $(task_switching_replication_files))

## table-subject-summary.tex
##            : Generate a table summarizing subjects
##              run so far, their date and condition, and
##              their average accuracy and reaction time
##
$(TABLE_DIR)/table-subject-summary.tex: $(SRC_DIR)/generate-subject-summary.py $(task_switching_replication_data)
	python $^ --output $@


## clean      : DANGER: Remove all generated tables.  Table generation is relatively
##              quick, so actually removing and redoing all tables is not that big a deal
##              if needed.
##
.PHONY : clean
clean  :
	rm -rf $(table_results) *~

## help       : Get all build targets supported by this build.
##
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
