# UKBioBank - Impact of genetic and environmental risk for depression on brain structure

## Requirements

Python 2.7, plus the following packages:

* Pandas
* Numpy
* Matplotlib
* Seaborn
* PyMC3
* Bambi

### Installing PyMC3

PyMC3 relies on Theano, which is near impossible to install without errors. Following this method should result in minimal unsolvable problems:

Firstly, install Theano's dependencies 

```bash
conda install mkl mkl-service libpython m2w64-toolchain
```

Then install Theano and pygpu

```bash
conda install theano pygpu
```

And finally install PyMC3 (and then Bambi, which depends on PyMC3)

```bash
pip install pymc3 bambi
```

## Running the scripts

### Producing environmental risk scores

First we use the `adversity_prediction.py` script to find environmental predictors of depression using regularised logistic regression and produce individual risk scores for each subject based on these. This can be run using the `adversity_prediction_job.sh` script.

### Creating dataframes including risk scores and GMV/FA

Next we produce dataframes that include our predictors (environmental risk scores and polygenic risk scores) and outcome variables (separate dataframes for GMV and FA even though this is a waste of space) using the `create_dataframes_for_model.py` script (run using `create_dataframes_for_model.sh`).

### Defining and running the models

Lastly we construct hierarchical regression models predicting GMV and FA based on environmental and genetic risk. This is done with the scripts `adversity_genetic_risk_model_fa.py` and `adversity_genetic_risk_model_gmv.py`, which are run using the shell scripts `risk_model_job_fa.sh` and `risk_model_job_gmv.sh`. These shouldn't take too long to run - probably about an hour or so.

These will produce a few outputs, the model results and trace (saved as pickles), along with a plot and csv summary of the parameter estimates.

### Visualising results

A very limited visualisation of the results is implemented in the jupyter notebook `model_results.ipynb`