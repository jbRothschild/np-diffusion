CODE_DIR = model figures
current_dir = $(notdir $(shell pwd))
parent_dir = $(notdir ${current_dir}/..)
.PHONY : clean zip custom sim data Figs fig%
# setting up suffix rules

##<<Different commands for makefile>>git

## all : runs main code and creates figure
all :
	$(MAKE) -C $(CODE_DIR)

## homogen : scores our different models according to some homogenous score
homogen :
	$(MAKE) -C model $@

## sim : runs the diffusion with
sim :
	echo $(param)
	$(MAKE) -C model $@ ARGS1=$(model) ARGS2=${param}

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
