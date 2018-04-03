import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import re
import datetime
import seaborn as sns
sns.set(style='white')
import matplotlib.pyplot as plt
import pickle

# create separate dataframes for GMV and FA
fields = pd.read_csv("/mnt/lustre/groups/ukbiobank/KCL_Data/Phenotypes/Full_Dataset_August_2017/Final_field_finder_071117", sep='\t', header=None)
fields.columns = ['row', 'ukbb_field', 'description']

# define lists of columns used for selecting relevant data
risk_columns = ['adult_risk', 'early_life_risk']

# extract GMV columns based on field description
gmv_desc = fields.description[fields.description.str.contains('Volume.of')].tolist()
gmv_desc = [c for c in gmv_desc if not 'peripheral' in c and not 'ventricular' in c and not 'brain.grey' in c
               and not re.match('.+(grey|white).matter.[2n].+', c)]
gmv_columns = fields.ukbb_field[fields.description.isin(gmv_desc)].tolist()

# extract FA columns
fa_columns = fields.ukbb_field[fields.description.str.contains('Mean.FA')].tolist()

# id, age and sex columns
id_column = 'f.eid'
age_column = 'f.21003.2.0'
sex_column = 'f.31.0.0'

# load MHQ data
col_names = gmv_columns + fa_columns + [id_column, age_column, sex_column]

print "{0} Loading data".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# load dataframe with MHQ data
data = pd.read_csv("/mnt/lustre/groups/ukbiobank/KCL_Data/Phenotypes/Full_Dataset_August_2017/Final_full_pheno_061117.txt",
                   sep='\t', dtype=np.float64, usecols=col_names)
print "{0} Loaded data, shape = {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.shape)

# load risk data
risk_data = pd.read_csv('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/imaging_adversity_genetic_risk_df.txt',
                   dtype=np.float64, usecols=[id_column] + risk_columns)
print "{0} Loaded adversity risk scores, shape = {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), risk_data.shape)

prs_data = pd.read_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/prsice_test.best", sep='\t',
                       usecols=['IID', 'PRS'])
prs_data.columns = ['f.eid', 'PRS']
print "{0} Loaded PRS scores, shape = {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prs_data.shape)

# merge MRI and risk data
merged_data = pd.merge(data, risk_data, on=id_column)
merged_data = pd.merge(merged_data, prs_data, on=id_column)

# create separate dataframes for GMV and FA
gmv = merged_data[gmv_columns + risk_columns + [id_column, age_column, sex_column] + ['PRS']]
fa = merged_data[fa_columns + risk_columns + [id_column, age_column, sex_column] + ['PRS']]

# convert to long
gmv_long = pd.melt(gmv, id_vars=[id_column, age_column, sex_column] + risk_columns + ['PRS'])
fa_long = pd.melt(fa, id_vars=[id_column, age_column, sex_column] + risk_columns + ['PRS'])

gmv_long.columns = ['id', 'age', 'sex', 'adult_risk', 'early_life_risk', 'PRS', 'region', 'volume']
fa_long.columns = ['id', 'age', 'sex', 'adult_risk', 'early_life_risk', 'PRS', 'tract', 'fa']

print "{0} Created GMV/FA dataframes".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print "Number of subjects in GMV dataframe = {0}".format(len(gmv_long.id.unique()))
print "Number of subjects in FA dataframe = {0}".format(len(fa_long.id.unique()))

gmv_long.to_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/GMV_dataframe.txt", index=False)
fa_long.to_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/FA_dataframe.txt", index=False)

print "Saved dataframes"

# Plot GMV distributions

plt.figure(figsize=(22, 7))
sns.lvplot(data=gmv_long, x='region', y='volume', scale="linear")
plt.tight_layout()
plt.xticks(rotation=90)
plt.gcf().subplots_adjust(bottom=0.2)
plt.xlabel("Region", fontweight="bold")
plt.ylabel("Volume", fontweight="bold")
plt.savefig("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/GMV_distributions.pdf")
plt.clf()
plt.cla()
plt.close()

plt.figure(figsize=(22, 7))
sns.lvplot(data=fa_long, x='tract', y='fa', scale="linear")
plt.tight_layout()
plt.xticks(rotation=90)
plt.gcf().subplots_adjust(bottom=0.2)
plt.xlabel("Tract", fontweight="bold")
plt.ylabel("FA", fontweight="bold")
plt.savefig("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/FA_distributions.pdf")
plt.clf()
plt.cla()
plt.close()

print "Plotted data distributions"