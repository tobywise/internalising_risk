import pandas as pd
import numpy as np
import datetime

print "Starting"

# Settings
njobs = 1  # cores to use for parallel operations

outcome_var = 'Depressed.Ever'
id_var = 'f.eid'

col_names = [id_var, outcome_var]

# Load MHQ data
print "{0} Loading data".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# load dataframe with MHQ data
data = pd.read_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/Process_MH_Questionnaire_JRIC_220317_Output.txt",
                   sep=' ',  usecols=['ID', outcome_var])
data.columns = [id_var, outcome_var]
print "{0} Loaded data, shape = {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.shape)

print "{0} Number of cases with outcome variable = {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.shape[0])

# Create pheno file with only MRI IDs
pheno_data = data[[id_var, outcome_var]][~data[outcome_var].isnull()]
pheno_data[id_var] = pheno_data[id_var].astype(int)
pheno_data[outcome_var] = pheno_data[outcome_var].astype(int)

pheno_data.to_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/MRI_pheno_file.txt", header=False,
                  index=None, sep=' ')

pheno_data[id_var].to_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/MRI_keep_file.txt", header=False,
                  index=None, sep=' ')