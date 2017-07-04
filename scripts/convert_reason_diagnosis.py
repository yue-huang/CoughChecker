# Usage: python3 convert_reason_diagnosis.py df_cough_2014.csv_convertNA.csv

import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def remove_irrelevant_reasons(df, reasons):
    for reason in reasons:
        df.loc[df[reason] == 10460, reason] = np.nan
        df.loc[(df[reason] >= 10600) & (df[reason] <= 10660), reason] = np.nan
        #df.loc[(df[reason] >= 10750) & (df[reason] <= 10960), reason] = np.nan
        df.loc[df[reason] == 11355, reason] = np.nan
        df.loc[df[reason] == 13552, reason] = np.nan
        df.loc[df[reason] == 14450, reason] = np.nan
        df.loc[df[reason] >= 20000, reason] = np.nan
        #df.loc[(df[reason] >= 26000) & (df[reason] <= 26490), reason] = np.nan
        #df.loc[df[reason] >= 31000, reason] = np.nan
    return df


def convert_reasons(df):
    '''
    One hot encode five reasons into binary reasons.
    '''
    reasons = ['RFV1', 'RFV2', 'RFV3', 'RFV4', 'RFV5']
    df.RFV1 = df.RFV1.astype(float)
    df = remove_irrelevant_reasons(df, reasons)

    # One hot encoding
    df1 = pd.get_dummies(df['RFV1'], prefix='R')
    df2 = pd.get_dummies(df['RFV2'], prefix='R')
    df3 = pd.get_dummies(df['RFV3'], prefix='R')
    df4 = pd.get_dummies(df['RFV4'], prefix='R')
    df5 = pd.get_dummies(df['RFV5'], prefix='R')
    df_reasons = pd.concat([df1, df2, df3, df4, df5], axis=1)
    df_reasons = df_reasons.groupby(df_reasons.columns, axis=1).sum()
    df = pd.concat([df, df_reasons], axis=1)
    df.drop(['RFV1', 'RFV2', 'RFV3', 'RFV4', 'RFV5'], axis=1, inplace=True)

    # Combine redundant features
    if ('DIABTYP' in df.columns) and ('R_22050.0' in df.columns):
        df['DIAB'] = df['DIABTYP'] + df['R_22050.0']
        df.loc[df.DIAB > 0, 'DIAB'] = 1
        df = df.drop(['DIABTYP', 'R_22050.0'], axis=1)
    if ('DEPRN' in df.columns) and ('R_11100.0' in df.columns):
        df['DEPR'] = df['DEPRN'] + df['R_11100.0']
        df.loc[df.DEPR > 0, 'DEPR'] = 1
        df = df.drop(['DEPRN', 'R_11100.0'], axis=1)
    if ('R_14000.0' in df.columns) and ('R_14103.0' in df.columns):
        df['R_nasal_congestion'] = df['R_14000.0'] + df['R_14103.0']
        df.loc[df.R_nasal_congestion > 0, 'R_nasal_congestion'] = 1
        df = df.drop(['R_14000.0', 'R_14103.0'], axis=1)
    return df


def convert_diagnoses_all(df):
    # Original version to convert all five diagnoses. Didn't use.
    colnames = ['DIAG1R', 'DIAG2R', 'DIAG3R', 'DIAG4R', 'DIAG5R']
    for colname in colnames:
        for index, value in df[colname].iteritems():
            if pd.notnull(value) and (type(value) is np.float64):
                while True:
                    if int((value - 100000) / 100) == 465:
                        df.loc[index, colname] = 'acute_upper_respiratory_infection'
                        break
                    elif int((value - 100000) / 100) == 466:
                        df.loc[index, colname] = 'acute_bronchitis'
                        break
                    elif int((value - 100000) / 100) == 462:
                        df.loc[index, colname] = 'acute_pharyngitis'
                        break
                    elif int((value - 100000) / 100) == 401:
                        df.loc[index, colname] = 'hypertension_ACE'
                        break
                    elif int((value - 100000) / 100) == 460:
                        df.loc[index, colname] = 'common_cold'
                        break
                    elif int((value - 100000) / 100) == 487:
                        df.loc[index, colname] = 'influenza'
                        break
                    elif int((value - 100000) / 100) == 488:
                        df.loc[index, colname] = 'influenza'
                        break
                    elif int((value - 100000) / 100) == 33:
                        df.loc[index, colname] = 'whooping_cough'
                        break
                    elif int((value - 100000) / 100) == 477:
                        df.loc[index, colname] = 'allergic_rhinitis'
                        break
                    elif int((value - 100000) / 100) == 493:
                        df.loc[index, colname] = 'asthma'
                        break
                    elif int((value - 100000) / 100) == 490:
                        df.loc[index, colname] = 'bronchitis'
                        break
                    elif int((value - 100000) / 100) == 491:
                        df.loc[index, colname] = 'chronic_bronchitis'
                        break
                    elif int((value - 100000) / 100) == 492:
                        df.loc[index, colname] = 'emphysema'
                        break
                    elif value - 100000 == 53011:
                        df.loc[index, colname] = 'GERD'
                        break
                    elif value - 100000 == 53081:
                        df.loc[index, colname] = 'GERD'
                        break
                    elif value - 100000 == 78491:
                        df.loc[index, colname] = 'postnasal_drip'
                        break
                    elif int((value - 100000) / 100) == 461:
                        df.loc[index, colname] = 'acute_sinusitis'
                        break
                    elif int((value - 100000) / 100) == 473:
                        df.loc[index, colname] = 'chronic_sinusitis'
                        break
                    elif int((value - 100000) / 100) == 464:
                        df.loc[index, colname] = 'acute_laryngitis'
                        break
                    elif int((value - 100000) / 100) == 476:
                        df.loc[index, colname] = 'chronic_laryngitis'
                        break
                    elif int((value - 100000) / 10) == 2770:
                        df.loc[index, colname] = 'cystic_fibrosis'
                        break
                    elif int((value - 100000) / 100) == 162:
                        df.loc[index, colname] = 'lung_cancer'
                        break
                    elif int((value - 100000) / 100) == 231:
                        df.loc[index, colname] = 'lung_cancer'
                        break
                    elif int((value - 100000) / 10) == 1970:
                        df.loc[index, colname] = 'lung_cancer'
                        break
                    break
    df1 = pd.get_dummies(df['DIAG1R'], prefix='D')
    df2 = pd.get_dummies(df['DIAG2R'], prefix='D')
    df3 = pd.get_dummies(df['DIAG3R'], prefix='D')
    df4 = pd.get_dummies(df['DIAG4R'], prefix='D')
    df5 = pd.get_dummies(df['DIAG5R'], prefix='D')
    df_diagnoses = pd.concat([df1, df2, df3, df4, df5], axis=1)
    df_diagnoses = df_diagnoses.groupby(df_diagnoses.columns, axis=1).sum()
    df = pd.concat([df, df_diagnoses], axis=1)
    df.drop(colnames, axis=1, inplace=True)
    return df


def convert_diagnoses(df):
    '''
    Convert primary diagnoses into categories and one hot encode into binary diagnoses.
    '''
    colnames = ['DIAG1R']
    rest_colnames = ['DIAG2R', 'DIAG3R', 'DIAG4R', 'DIAG5R']

    # Only retain patients that have primary diagnoses
    df.dropna(subset=colnames, inplace=True)

    print('Number of samples beforing dropping:', df.shape[0])

    # Convert diagnoses into categories
    for colname in colnames:
        for index, value in df[colname].iteritems():
            if pd.notnull(value) and (type(value) is np.float64):
                while True:
                    if int((value - 100000) / 100) == 465:
                        df.loc[index, colname] = 1
                        break
                    elif int((value - 100000) / 100) == 466:
                        df.loc[index, colname] = 1
                        break
                    elif int((value - 100000) / 100) == 462:
                        df.loc[index, colname] = 1
                        break
                    # elif int((value-100000)/100) == 401: df.loc[index,colname] = 4;break
                    elif int((value - 100000) / 100) == 460:
                        df.loc[index, colname] = 1
                        break
                    elif int((value - 100000) / 100) == 487:
                        df.loc[index, colname] = 6
                        break
                    elif int((value - 100000) / 100) == 488:
                        df.loc[index, colname] = 6
                        break
                    elif int((value - 100000) / 100) == 33:
                        df.loc[index, colname] = 7
                        break
                    elif int((value - 100000) / 100) == 477:
                        df.loc[index, colname] = 8
                        break
                    elif int((value - 100000) / 100) == 493:
                        df.loc[index, colname] = 9
                        break
                    elif int((value - 100000) / 100) == 491:
                        df.loc[index, colname] = 11
                        break
                    elif int((value - 100000) / 100) == 492:
                        df.loc[index, colname] = 11
                        break
                    elif value - 100000 == 53011:
                        df.loc[index, colname] = 13
                        break
                    elif value - 100000 == 53081:
                        df.loc[index, colname] = 13
                        break
                    elif value - 100000 == 78491:
                        df.loc[index, colname] = 14
                        break
                    elif int((value - 100000) / 100) == 461:
                        df.loc[index, colname] = 1
                        break
                    elif int((value - 100000) / 100) == 473:
                        df.loc[index, colname] = 1
                        break
                    elif int((value - 100000) / 100) == 464:
                        df.loc[index, colname] = 1
                        break
                    elif int((value - 100000) / 100) == 476:
                        df.loc[index, colname] = 1
                        break
                    elif int((value - 100000) / 10) == 2770:
                        df.loc[index, colname] = 19
                        break
                    elif int((value - 100000) / 100) == 162:
                        df.loc[index, colname] = 20
                        break
                    elif int((value - 100000) / 100) == 231:
                        df.loc[index, colname] = 20
                        break
                    elif int((value - 100000) / 10) == 1970:
                        df.loc[index, colname] = 20
                        break
                    elif int((value - 100000) / 100) == 11:
                        df.loc[index, colname] = 21
                        break
                    elif int((value - 100000) / 10) == 4151:
                        df.loc[index, colname] = 22
                        break
                    elif int((value - 100000) / 10) == 4162:
                        df.loc[index, colname] = 22
                        break
                    elif int((value - 100000) / 100) == 428:
                        df.loc[index, colname] = 23
                        break
                    elif 480 <= int((value - 100000) / 100) <= 486:
                        df.loc[index, colname] = 24
                        break
                    break

    # Create a dictionary of disease categories
    disease_dict = {0: ['no_disease', 'no_disease'],
                    1: ['upper_respiratory_infection', 'mild'],
                    2: ['acute_bronchitis', 'mild'],
                    3: ['acute_pharyngitis', 'mild'],
                    4: ['hypertension_ACE', 'mild'],
                    5: ['common_cold', 'mild'],
                    6: ['influenza', 'severe'],
                    7: ['whooping_cough', 'severe'],
                    8: ['allergic_rhinitis', 'mild'],
                    9: ['asthma', 'severe'],
                    11: ['COPD', 'severe'],
                    13: ['GERD', 'mild'],
                    14: ['postnasal_drip', 'mild'],
                    15: ['sinusitis', 'mild'],
                    17: ['laryngitis', 'mild'],
                    19: ['cystic_fibrosis', 'severe'],
                    20: ['lung_cancer', 'severe'],
                    21: ['pulmonary_tuberculosis', 'severe'],
                    22: ['pulmonary_embolism', 'severe'],
                    23: ['heart_failure', 'severe'],
                    24: ['pneumonia', 'severe']}

    # Subset the data with diseases of interest
    df = df[df.DIAG1R <= 24]
    print("Number of samples after dropping other categories:", df.shape[0])

    # Convert disease categories into mild/severe binary labels
    stats = df.DIAG1R.value_counts()
    print('Before combination:\n', stats)

    # Create lists for summary statistics
    combined_mild = []
    combined_mild_number = []
    combined_severe = []
    combined_severe_number = []
    for index, value in stats.iteritems():
        if disease_dict[index][1] == 'mild':
            df.loc[df.DIAG1R == index, 'DIAG1R'] = 0
            combined_mild.append(disease_dict[index][0])
            combined_mild_number.append(value)
        elif disease_dict[index][1] == 'severe':
            df.loc[df.DIAG1R == index, 'DIAG1R'] = 1
            combined_severe.append(disease_dict[index][0])
            combined_severe_number.append(value)
    print('After combination:\n', df.DIAG1R.value_counts())
    print('Combined mild diseases, numbers and frequencies numbers are:')
    print(combined_mild, combined_mild_number, [
          number / sum(combined_mild_number) for number in combined_mild_number])
    print('Combined severe diseases and numbers are:')
    print(combined_severe, combined_severe_number, [
          number / sum(combined_severe_number) for number in combined_severe_number])

    # Only retain primary/first diagnoses
    df = df.drop(rest_colnames, axis=1)

    return df


def main(data_csv_name):
    stats = {}
    df = pd.read_csv(data_csv_name)
    stats['initial'] = [df.shape[0], df.shape[1]]

    df = convert_reasons(df)
    stats['convert_reasons'] = [df.shape[0], df.shape[1]]

    df = convert_diagnoses(df)
    stats['convert_diagnoses'] = [df.shape[0], df.shape[1]]

    df.to_csv(sys.argv[1] + '_convertRD_DIAG1R.csv', index=False)

    with open('stats_convert_reasons_diagnoses_DIAG1R.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['procedure', 'row_num', 'col_num'])
        for key, value in stats.items():
            print(key, value)
            writer.writerow([key] + value)


if __name__ == '__main__':
    main(sys.argv[1])
