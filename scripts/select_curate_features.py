# Preprocessing: Select and modify features based on manual curation and missing data.
# Usage: python3 select_curate_features.py df_cough_2014.csv cols-type-2014.csv

# Preprocessing steps:
# Subset the columns based on column name
# Edit rows manually


import sys
import csv
import pandas as pd
import numpy as np


def subset_cols(df, colType):
    colRetain = colType.name
    df = df[(df.columns).intersection(colRetain)]
    return df


def manual_editing(df):
    if 'USETOBAC' in df.columns:
        df.replace({'USETOBAC': {-8: np.nan}}, inplace=True)
        df.replace({'USETOBAC': {-9: np.nan}}, inplace=True)
    if 'RFV1' in df.columns:
        df.replace({'RFV1': {-9: np.nan}}, inplace=True)
    if 'RFV2' in df.columns:
        df.replace({'RFV2': {-9: np.nan}}, inplace=True)
    if 'RFV3' in df.columns:
        df.replace({'RFV3': {-9: np.nan}}, inplace=True)
    if 'RFV4' in df.columns:
        df.replace({'RFV4': {-9: np.nan}}, inplace=True)
    if 'RFV5' in df.columns:
        df.replace({'RFV5': {-9: np.nan}}, inplace=True)
    if 'MAJOR' in df.columns:
        df.replace({'MAJOR': {-9: 9}}, inplace=True)
        df.replace({'MAJOR': {4: 9}}, inplace=True)
        df.replace({'MAJOR': {6: 9}}, inplace=True)
    if ('DIAG1R' in df.columns) and ('PRDIAG1' in df.columns):
        df.loc[df.PRDIAG1 == 1, 'DIAG1R'] = np.nan
        df.replace({'DIAG1R': {-9: np.nan}}, inplace=True)
        df.loc[df.DIAG1R > 200000, 'DIAG1R'] = np.nan
    if ('DIAG2R' in df.columns) and ('PRDIAG2' in df.columns):
        df.loc[df.PRDIAG2 == 1, 'DIAG2R'] = np.nan
        df.replace({'DIAG2R': {-9: np.nan}}, inplace=True)
        df.loc[df.DIAG2R > 200000, 'DIAG2R'] = np.nan
    if ('DIAG3R' in df.columns) and ('PRDIAG3' in df.columns):
        df.loc[df.PRDIAG3 == 1, 'DIAG3R'] = np.nan
        df.replace({'DIAG3R': {-9: np.nan}}, inplace=True)
        df.loc[df.DIAG3R > 200000, 'DIAG3R'] = np.nan
    if ('DIAG4R' in df.columns) and ('PRDIAG4' in df.columns):
        df.loc[df.PRDIAG4 == 1, 'DIAG4R'] = np.nan
        df.replace({'DIAG4R': {-9: np.nan}}, inplace=True)
        df.loc[df.DIAG4R > 200000, 'DIAG4R'] = np.nan
    if ('DIAG5R' in df.columns) and ('PRDIAG5' in df.columns):
        df.loc[df.PRDIAG5 == 1, 'DIAG5R'] = np.nan
        df.replace({'DIAG5R': {-9: np.nan}}, inplace=True)
        df.loc[df.DIAG5R > 200000, 'DIAG5R'] = np.nan
    if 'ASTH_SEV' in df.columns:
        df.replace({'ASTH_SEV': {-9: np.nan}}, inplace=True)
        df.replace({'ASTH_SEV': {-7: np.nan}}, inplace=True)
        df.replace({'ASTH_SEV': {5: np.nan}}, inplace=True)
        df.replace({'ASTH_SEV': {6: np.nan}}, inplace=True)
    if 'NOCHRON' in df.columns:
        df.replace({'NOCHRON': {0: 2}}, inplace=True)
    if 'TOTCHRON' in df.columns:
        df.replace({'TOTCHRON': {-9: np.nan}}, inplace=True)
    if 'HTIN' in df.columns:
        df.replace({'HTIN': {-9: np.nan}}, inplace=True)
    if 'WTLB' in df.columns:
        df.replace({'WTLB': {-9: np.nan}}, inplace=True)
    if 'BMI' in df.columns:
        df.loc[df.BMI < 0, 'BMI'] = np.nan
    if 'TEMPF' in df.columns:
        df.replace({'TEMPF': {-9: np.nan}}, inplace=True)
    if 'BPSYS' in df.columns:
        df.replace({'BPSYS': {-9: np.nan}}, inplace=True)
    if 'BPDIAS' in df.columns:
        df.replace({'BPDIAS': {-9: np.nan}}, inplace=True)
        df.replace({'BPDIAS': {998: np.nan}}, inplace=True)
    if ('DIABTYP1' in df.columns) and ('DIABTYP2' in df.columns) and ('DIABTYP0' in df.columns):
        df['DIABTYP'] = df['DIABTYP1'] + df['DIABTYP2'] + df['DIABTYP0']
        df.loc[df.DIABTYP > 0, 'DIABTYP'] = 1
        df = df.drop(['DIABTYP1', 'DIABTYP2', 'DIABTYP0'], axis=1)
    df = df.drop(['PRDIAG1', 'PRDIAG2', 'PRDIAG3',
                  'PRDIAG4', 'PRDIAG5'], axis=1)
    return df


def main(data_csv_name, coltype_csv_name):
    stats = {}
    df = pd.read_csv(data_csv_name, low_memory=False)
    colType = pd.read_csv(coltype_csv_name, sep=',')
    stats['initial'] = [df.shape[0], df.shape[1]]

    df = subset_cols(df, colType)
    stats['subset_cols'] = [df.shape[0], df.shape[1]]

    df = manual_editing(df)
    stats['manual_editing'] = [df.shape[0], df.shape[1]]

    with open('stats_convertNA.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['procedure', 'row_num', 'col_num'])
        for key, value in stats.items():
            print(key, value)
            writer.writerow([key] + value)

    df.to_csv(sys.argv[1] + '_convertNA.csv', index=False)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
