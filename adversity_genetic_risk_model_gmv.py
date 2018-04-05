import matplotlib
matplotlib.use('Agg')
import pandas as pd
import bambi
import datetime
import seaborn as sns
sns.set(style='white')
import matplotlib.pyplot as plt
import pickle
import pymc3 as pm

# LOAD DATA
gmv_data = pd.read_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/GMV_dataframe.txt")

# STANDARDISE THINGS
def standardise(x):
    return (x - x.mean()) / x.std()

for i in ['early_life_risk', 'adult_risk', 'PRS', 'volume']:
    gmv_data[i] = standardise(gmv_data[i])

# CONSTRUCT MODEL
gmv_model = bambi.Model(gmv_data, dropna=True)

gmv_model.add('region', categorical=['region'])

gmv_model.fit('volume ~ 1 + early_life_risk + adult_risk + early_life_risk*adult_risk + '
             'PRS + PRS*early_life_risk + PRS*adult_risk + '
          'age + sex',
          random=['early_life_risk|region',
                  'adult_risk|region',
                  'early_life_risk*adult_risk|region',
                  'PRS|region',
                  'PRS*early_life_risk|region',
                  'PRS*adult_risk|region'],
          data = gmv_data,
          run=False)

print "{0} Constructed GMV model, starting fit...".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Fit the model using ADVI
gmv_results = gmv_model.fit(method='advi', n=20000)

print "{0} Finished model fitting".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Save the result object
pickle.dump(gmv_results, open( '/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/gmv_model_results_{0}'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")), "wb" ))

# Sample from the approximate posteriors
trace = pm.sample_approx(gmv_results, draws=1000)

# Save these samples
pickle.dump(gmv_results, open( '/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/gmv_model_results_trace{0}'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")), "wb" ))

# Plot the results
pm.traceplot(trace)
plt.savefig('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/gmv_traceplot_{0}.pdf'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")))

# Get a summary of the results and save this
summary = pm.df_summary(trace)
summary.to_csv('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/gmv_results_summary_{0}.csv'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")))

print "Done"