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

fa_results = fa_model.fit(method='advi', n=50000)

pickle.dump(fa_results, open( '/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/fa_model_results_{0}'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")), "wb" ))

trace = pm.sample_approx(fa_results, draws=1000)

pm.traceplot(trace)
plt.savefig('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/FA_traceplot_test_{0}.pdf'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")))