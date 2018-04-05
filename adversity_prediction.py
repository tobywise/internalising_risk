import pandas as pd
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import numpy as np
from scipy import stats
import datetime
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
sns.set(style='white')
import matplotlib.pyplot as plt

print "Starting"

# Settings
njobs = 1  # cores to use for parallel operations

# Load necessary variables
with open("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/early_life.txt") as f:
    early_life_vars = f.read().splitlines()

with open("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/adult.txt") as f:
    adult_vars = f.read().splitlines()

outcome_var = 'Depressed.Ever'
mri_var = 'f.25091.2.0'
id_var = 'f.eid'

col_names = early_life_vars + adult_vars + [mri_var] + [id_var]

# Load MHQ data
print "{0} Loading data".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# load dataframe with MHQ data
data = pd.read_csv("/mnt/lustre/groups/ukbiobank/KCL_Data/Phenotypes/Full_Dataset_August_2017/Final_full_pheno_061117.txt",
                   sep='\t', dtype=np.float64, usecols=col_names)
print "{0} Loaded data, shape = {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.shape)

# Load phenotype data (e.g. depressed or not)
print "{0} Loading phenotype data".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
p_data = pd.read_csv("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/Process_MH_Questionnaire_JRIC_220317_Output.txt",
                   sep=' ', dtype=np.float64, usecols=['ID', outcome_var])
p_data.columns = [id_var, outcome_var]
print "{0} Loaded data, shape = {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.shape)

print "Merging phenotype data"
data = pd.merge(data, p_data, on='f.eid')


# select MHQ cases with valid outcome values (i.e. not no answer/don't know)
data = data[~data[outcome_var].isnull()]
data = data[data[outcome_var] >= 0]
data = data[np.all(data[early_life_vars + adult_vars] >= 0, axis=1)]

print "{0} Number of cases with outcome variable = {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.shape[0])

# split data into training//test sets - test = MRI data (10k)
mri_ids = data[id_var][~data[mri_var].isnull()].values

# Separate predictors and outcome
outcome_data = data[outcome_var]
print "Histogram of outcome values"
print np.histogram(outcome_data)
mhq_data = data[early_life_vars + adult_vars]

# split data into training//test sets - test = MRI data (10k)
y_train = outcome_data[~data[id_var].isin(mri_ids)]
X_train = mhq_data[~data[id_var].isin(mri_ids)]

y_test = outcome_data[data[id_var].isin(mri_ids)]
X_test = mhq_data[data[id_var].isin(mri_ids)]

print "Number of non-MRI cases = {0}".format(len(X_train))
print "Number of MRI cases = {0}".format(len(X_test))

##############################
# PREDICTING BINARY OUTCOMES #
##############################

# LOGISTIC REGRESSION WITH L1 PENALTY
print "{0} Setting up regression".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Parameter to optimise with CV = alpha (L1)
tuned_parameters = {'C': stats.expon(scale=1)}

# Set up parameter search using random search with 5-fold CV, scoring = accuracy
logistic_regression = RandomizedSearchCV(linear_model.LogisticRegression(), param_distributions=tuned_parameters, n_iter=1000,
                           cv=5, n_jobs=njobs, scoring='accuracy', random_state=1)

print "{0} Running parameter search".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
logistic_regression.fit(X_train, y_train)

print "{0} Parameter search done".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print "Optimal C value = {0}".format(logistic_regression.best_params_['C'])


# Train model with optimal alpha
logistic_regression_test = linear_model.LogisticRegression(C=logistic_regression.best_params_['C'])
logistic_regression_test.fit(X_train, y_train)

# Predict test set values
y_pred = logistic_regression_test.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print "Accuracy on test set = {0}".format(accuracy)

# Get coefficients
coefs = logistic_regression_test.coef_
print "Coefficients = {0}".format(coefs)

print early_life_vars + adult_vars
print coefs[0]
plt.bar(range(0, len(coefs[0])), coefs[0], color=['#009B8B'] * len(early_life_vars) + ['#FAA200'] * len(adult_vars))
plt.xticks(range(0, len(coefs[0])), early_life_vars + adult_vars, rotation='vertical')
plt.xlabel("Variable")
plt.ylabel("Regression coefficient")
plt.tight_layout()

plt.savefig("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/coefs.png")


##################################
# PREDICTING CONTINUOUS OUTCOMES #
##################################

# LINEAR REGRESSION WITH L1 PENALTY (LASSO)

# # Parameter to optimise with CV = alpha (L1)
# tuned_parameters = {'alpha': stats.expon(scale=1)}
#
# # Set up parameter search using random search with 5-fold CV, scoring = MSE
# lasso = RandomizedSearchCV(linear_model.Lasso(), param_distributions=tuned_parameters, n_iter=1000,
#                            cv=5, n_jobs=njobs, scoring='accuracy', random_state=1)


# print "Running parameter search"
# lasso.fit(X_train, y_train)
#
# print "Parameter search done"
# print "Optimal alpha value = {0}".format(lasso.best_params_['alpha'])
#
#
# # Train model with optimal alpha
# lasso_test = linear_model.Lasso(alpha = lasso.best_params_['alpha'])
# lasso_test.fit(X_train, y_train)
#
# # Predict test set values
# y_pred = lasso_test.predict(X_test)
# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)
# print "MSE on test set = {0}".format(mse)
# print "R-squared in test set = {0}".format(r2)
#
# # Get coefficients
# print dir(lasso_test)
# coefs = lasso_test.coef_
# print "Coefficients = {0}".format(coefs)

print "{0} Regression done!".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#################################

# Create adversity risk scores
mri_data = mhq_data[data['f.eid'].isin(mri_ids)]
mri_data['early_life_risk'] = np.sum(X_test[early_life_vars].values * coefs[0][:len(early_life_vars)], axis=1)
mri_data['adult_risk'] = np.sum(X_test[adult_vars].values * coefs[0][len(early_life_vars):], axis=1)


# plot distributions of risk scores
plt.figure(figsize=(5, 4))
sns.set_palette(sns.color_palette(['#009B8B', '#FAA200']))
a = sns.kdeplot(mri_data['early_life_risk'], shade=True, label='Early life')
b = sns.kdeplot(mri_data['adult_risk'], shade=True, label='Adult')
legend = plt.legend(title='Risk scores')
plt.xlabel("Risk estimate")
# legend.get_title().set_fontsize('10')
a.axes.get_yaxis().set_visible(False)
plt.savefig("/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/risk_distribution.png")

mri_data['f.eid'] = data[data['f.eid'].isin(mri_ids)]['f.eid']
mri_data.to_csv('/mnt/lustre/groups/ukbiobank/Edinburgh_Data/usr/toby/adversity/imaging_adversity_risk_df.txt')

print '{0} Saved risk data'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
