CODE_DIR = model figures
current_dir = $(notdir $(shell pwd))
parent_dir = $(notdir ${current_dir}/..)
.PHONY : clean zip
# setting up suffix rules

##<<Different commands for makefile>>

## all : runs main code and creates figure
all :
	$(MAKE) -C $(CODE_DIR)

## custom : runs the diffusion with a custom model, not the loaded data
custom :
	$(MAKE) -C model $@

## load : runs the diffusion with data model
load :
	$(MAKE) -C model $@

## Figs : runs all figures in figures
Figs :
	$(MAKE) -C figures

## fig% : runs figure%.py in figures
fig% :
	$(MAKE) -C figures $@

## zip : zips all files in the folder
zip :
	zip -r ${parent_dir}/${current_dir}_rothschild  ${parent_dir}/${current_dir}

## clean : remove auto-generated files
clean :
	$(MAKE) -C $(CODE_DIR) clean

help : makefile
	@sed -n 's/^##//p' $<
