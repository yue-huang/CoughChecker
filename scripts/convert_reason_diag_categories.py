# Usage: python3 convert_reason_diagnosis.py df_cough_2014.csv_convertNA.csv ICD9CM_categories.csv

import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def convert_reasons (df):
    df.RFV1 = df.RFV1.astype(float)
    df1 = pd.get_dummies(df['RFV1'], prefix = 'R')
    df2 = pd.get_dummies(df['RFV2'], prefix = 'R')
    df3 = pd.get_dummies(df['RFV3'], prefix = 'R')
    df4 = pd.get_dummies(df['RFV4'], prefix = 'R')
    df5 = pd.get_dummies(df['RFV5'], prefix = 'R')
    df_reasons = pd.concat([df1,df2,df3,df4,df5],axis = 1)
    df_reasons = df_reasons.groupby(df_reasons.columns,axis=1).sum()
    df = pd.concat([df,df_reasons], axis = 1)
    df.drop(['RFV1','RFV2','RFV3','RFV4','RFV5'],axis = 1, inplace = True)
    return df

def convert_diagnoses (df, icd):
    colnames = ['DIAG1R', 'DIAG2R','DIAG3R', 'DIAG4R','DIAG5R']
    #df_diag = df[colnames].fillna(0)
    for colname in colnames:
        #df_diag[colname] = df_diag[colname].astype(float)
        for index, value in df[colname].iteritems():
            if value is not np.nan:
                for index2, row in icd.iterrows():
                    if row.iloc[1]<= value <row.iloc[2]:
                        df.loc[index,colname] = row.iloc[0]
                        break
                        #df_diag.loc[(df_diag[colname]>row.iloc[1]) & (df_diag[colname]<row.iloc[2]),colname] = row.iloc[0]
    #df_diag = df_diag.replace(0, np.nan)
    #df = pd.concat([df.drop(colnames, axis = 1), df_diag], axis = 1)
    df1 = pd.get_dummies(df['DIAG1R'], prefix = 'D')
    df2 = pd.get_dummies(df['DIAG2R'], prefix = 'D')
    df3 = pd.get_dummies(df['DIAG3R'], prefix = 'D')
    df4 = pd.get_dummies(df['DIAG4R'], prefix = 'D')
    df5 = pd.get_dummies(df['DIAG5R'], prefix = 'D')
    df_diagnoses = pd.concat([df1,df2,df3,df4,df5],axis = 1)
    df_diagnoses = df_diagnoses.groupby(df_diagnoses.columns,axis=1).sum()
    df = pd.concat([df,df_diagnoses], axis = 1)
    df.drop(colnames,axis = 1, inplace = True)
    return df

def main(data_csv_name, icd_csv_name):
    stats = {}
    df = pd.read_csv(data_csv_name)
    icd = pd.read_csv(icd_csv_name, header = None)
    stats['initial'] = [df.shape[0], df.shape[1]]

    df = convert_reasons(df)
    stats['convert_reasons'] = [df.shape[0], df.shape[1]]

    df = convert_diagnoses(df, icd)
    stats['convert_diagnoses'] = [df.shape[0], df.shape[1]]

    df.to_csv(sys.argv[1] + '_convertRD.csv', index = False)

    with open('stats_convert_reasons_diagnoses.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['procedure','row_num','col_num'])
        for key, value in stats.items():
            print(key, value)
            writer.writerow([key] + value)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
