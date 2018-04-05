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
fa_data = pd.read_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/FA_dataframe.txt")

# STANDARDISE THINGS
def standardise(x):
    return (x - x.mean()) / x.std()

for i in ['early_life_risk', 'adult_risk', 'PRS', 'fa']:
    fa_data[i] = standardise(fa_data[i])


# CONSTRUCT MODEL
fa_model = bambi.Model(fa_data, dropna=True)

fa_model.add('tract', categorical=['tract'])

fa_model.fit('fa ~ 1 + early_life_risk + adult_risk + early_life_risk*adult_risk + '
             'PRS + PRS*early_life_risk + PRS*adult_risk + '
          'age + sex',
          random=['early_life_risk|tract',
                  'adult_risk|tract',
                  'early_life_risk*adult_risk|tract',
                  'PRS|tract',
                  'PRS*early_life_risk|tract',
                  'PRS*adult_risk|tract'],
          data = fa_data,
          run=False)

print "{0} Constructed FA model, starting fit...".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Fit the model using ADVI
fa_results = fa_model.fit(method='advi', n=20000)

print "{0} Finished model fitting".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Save the result object
pickle.dump(fa_results, open( '/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/fa_model_results_{0}'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")), "wb" ))

# Sample from the approximate posteriors
trace = pm.sample_approx(fa_results, draws=1000)

# Save these samples
pickle.dump(fa_results, open( '/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/fa_model_results_trace{0}'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")), "wb" ))

# Plot the results
pm.traceplot(trace)
plt.savefig('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/fa_traceplot_{0}.pdf'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")))

# Get a summary of the results and save this
summary = pm.df_summary(trace)
summary.to_csv('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/fa_results_summary_{0}.csv'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")))

print "Done"