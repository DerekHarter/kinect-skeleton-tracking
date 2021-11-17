## List of all valid targets in this project:
## ----------------------------------------------
## all        : By default the top level make will
##              perform all tasks to perform
##              project workflow, from data cleaning
##              and analysis, through creating
##              figure and table results to final
##              paper generation.
##
.PHONY : all
all : data figures tables papers


## data       : Perform data cleaning and data
##              analysis.  Parse raw captured
##              data to create data sets for
##              various project high level
##              analysis tasks.
##
.PHONY : data
data :
	cd data && $(MAKE)


## figures    : Generate all figures and visualizations
##              needed for paper.
##
.PHONY : figures
figures :
	cd figures && $(MAKE)

## tables     : Generate all tables needed for paper.
##
.PHONY : tables
tables :
	cd tables && $(MAKE)

## papers     : Create the paper using results and figures
##              from the subprojects.
##
.PHONY : papers
papers :
	cd papers && $(MAKE)

## backup     : Backup raw data, use git system to add data files 
##              commit them and push them to the remore repository.
##
.PHONY : backup
backup :
	#git add data figures tables papers
	git add data
	git commit -m "Project backup target: `date`"
	git push


## clean      : DANGER: Remove all generated build products so can
##              rebuild everything from scratch.  It can take time
##              especially to regenerate model data and results, so
##              use this only when really want a complete clean rebuild
##              of all project data and results.
##
.PHONY : clean
clean  :
	#cd data && $(MAKE) clean  && cd ../tables && $(MAKE) clean && cd ../figures && $(MAKE) clean && cd ../papers && $(MAKE) clean
	cd data && $(MAKE) clean  && cd ../tables && $(MAKE) clean && cd ../figures && $(MAKE) clean && cd ../papers && $(MAKE) clean


## help       : Get all build targets supported by this build.
##
.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
