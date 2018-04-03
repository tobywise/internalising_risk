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

gmv_results = gmv_model.fit(method='advi', n=50000)

pickle.dump(gmv_results, open( '/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/gmv_model_results_{0}'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")), "wb" ))

trace = pm.sample_approx(gmv_results, draws=1000)

pm.traceplot(trace)
plt.savefig('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/traceplot_test_{0}.pdf'.format(
    datetime.datetime.now().strftime("%Y_%m_%d")))

# print "{0} GMV model fit".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# print gmv_results[:].summary()
# print gmv_results[:].summary(ranefs=True)
#
# gmv_results[:].plot()
# plt.savefig('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/gmv_model_results_{0}.pdf'.format(
#     datetime.datetime.now().strftime("%Y_%m_%d")))
# gmv_results[:].plot(transformed=True)
# plt.savefig('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/gmv_model_results_{0}.pdf'.format(
#     datetime.datetime.now().strftime("%Y_%m_%d")))
#
# print "{0} Saved fit result figure".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
# pickle.dump(gmv_results, open( '/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/gmv_model_results_{0}'.format(
#     datetime.datetime.now().strftime("%Y_%m_%d")), "wb" ))
#
# print "{0} Saved bambi model object".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))