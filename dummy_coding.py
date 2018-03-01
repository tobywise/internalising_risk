import pandas as pd
import argparse

def dummy_code(data, vars, sep=' '):

    df = pd.read_csv(data, sep=sep)

    for v in vars:
        if v not in df.columns:
            raise AttributeError("Column {0} not present in data file".format(v))

    dummies = {}

    if not isinstance(vars, list):
        vars = [vars]

    for v in vars:
        print "Recoding {0}".format(v)
        for n, i in enumerate(df[v].unique()):
            if n == 0:
                dummies[v + '_dummy_{0}'.format(n)] = 0
            else:
                dummies[v + '_dummy_{0}'.format(n)] = (df[v] == i).astype(int)

    dummies = pd.DataFrame(dummies)

    dummy_df = pd.concat([df, dummies], axis=1)
    dummy_df = dummy_df[[i for i in dummy_df.columns if not i in vars]]

    dummy_df.to_csv(data.split('.')[0] + '_dummy_coded.txt', index=False, sep=sep)

    print "Finished"


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="File to do dummy coding with")
    parser.add_argument('vars', help="Names of columns to dummy code, can be given as a list of names separated with commas,"
                                     "e.g. var1,var2,var3")
    parser.add_argument('--sep', help="File separator, default = space", dest='sep')
    parser.set_defaults(sep=' ')
    args = parser.parse_args()

    args.vars = args.vars.split(',')

    dummy_code(args.file, args.vars, args.sep)