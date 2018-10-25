# NP_EulerDiffusion
Solving differential equations numerically is possible using many open source programs, however this doesn't always let you manipulate your domain and boundary conditions as efficiently as you'd require. For this project, we wanted to investigate the distribution of nanoparticles in complicated vasculature data. In the first part, we developped all the machinery of the diffusion of these simulations in the directory model. The first stage of the code is a simple euler method [main.py, diffusion.py, various_model.py]. Future development will hopefully use meshes and may have another module that does the diffusion using external software. All data is stored in the directory data and figures are generated from figures.

## Prerequisites
You will need a version of python 2.7.15 (although most of the code runs on other versions of python very well. You will also need the following modules
  - numpy
  - TBC
## Running
### Structure

### Simulation run
A couple of scripts (makefiles) are available to help run everything smoothly from the home directory. Running from command line, you can simply type (from the home directory)
```python
make 
```
```bash
example code
```
## Authors
*  *Jeremy Rothschild* -[jbRothschild](https://github.come/jbRothschild)

## Acknowledgements
