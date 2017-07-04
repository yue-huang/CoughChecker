# Transformation: Scale numerical features, convert categorical features to binary values.
# Usage: python3 transform.py df_cough_2014.csv_convertNA.csv_convertRD_DIAG1R.csv cols-type-2014.csv


import pandas as pd
import sys
from random import sample
import csv


def separate_cols(df, outcome_col, colType):
    '''
    Separate outcome, numerical/ordinal, categorical and the rest columns.
    '''
    y = df[outcome_col]
    x = df.drop(outcome_col, axis=1)
    x_numerical_ordinal = pd.DataFrame()
    x_categorical = pd.DataFrame()
    x_extra = pd.DataFrame()
    for col in x.columns:
        if col in colType.name.values:
            type = colType[(colType.name == col)].type.iloc[0]
            if type == 'n' or type == 'o':
                x_numerical_ordinal[col] = x[col]
            elif type == 'c':
                x_categorical[col] = x[col]
        else:
            x_extra[col] = x[col]
    return y, x_numerical_ordinal, x_categorical, x_extra


def impute_NA(df, colType):
    '''
    Impute NA to median or mode.
    '''
    for col in df.columns:
        if df[col].isnull().any():
            if col in colType.name.values:
                type = colType[(colType.name == col)].type.iloc[0]
                if type == 'n' or type == 'o':
                    df[col].fillna(value=df[col].median(), inplace=True)
                elif type == 'c':
                    df[col].fillna(value=df[col].mode().iloc[0], inplace=True)
    return df


def transform(y, x_numerical_ordinal, x_categorical, x_extra):
    '''
    Scale numerical features, and convert categorical features to binary values.
    '''
    for col in x_numerical_ordinal.columns:
        min = x_numerical_ordinal[col].min()
        max = x_numerical_ordinal[col].max()
        if min == max:
            x_numerical_ordinal.drop(col, axis=1, inplace=True)
        else:
            x_numerical_ordinal[col] = (
                x_numerical_ordinal[col] - min) / (max - min)

    x_categorical = pd.get_dummies(
        x_categorical, columns=x_categorical.columns, drop_first=True)

    stats['x_numerical_ordinal_transformed'] = [
        x_numerical_ordinal.shape[0], x_numerical_ordinal.shape[1]]
    stats['x_categorical_transformed'] = [
        x_categorical.shape[0], x_categorical.shape[1]]

    df_transformed = pd.concat(
        [y, x_numerical_ordinal, x_categorical, x_extra], axis=1)
    return (df_transformed)


def main(data_csv_name, coltype_csv_name):
    print("Reading in files...")
    df = pd.read_csv(data_csv_name, sep=',')
    colType = pd.read_csv(coltype_csv_name, sep=',')
    stats['initial'] = [df.shape[0], df.shape[1]]

    print('Imputing NA to median or mode...')
    df = impute_NA(df, colType)

    print('Separating outcome, numerical/ordinal and categorical columns...')
    outcome_col_name = 'DIAG1R'
    y, x_numerical_ordinal, x_categorical, x_extra = separate_cols(
        df, outcome_col_name, colType)
    stats['x_numerical_ordinal'] = [
        x_numerical_ordinal.shape[0], x_numerical_ordinal.shape[1]]
    stats['x_categorical'] = [x_categorical.shape[0], x_categorical.shape[1]]
    stats['x_extra'] = [x_extra.shape[0], x_extra.shape[1]]

    print('Transforming columns...')
    df_transformed = transform(y, x_numerical_ordinal, x_categorical, x_extra)
    stats['transformed'] = [df_transformed.shape[0], df_transformed.shape[1]]
    df_transformed.to_csv(sys.argv[1] + '_transformed.csv', index=False)

    print('writing files...')
    with open('stats_transformation.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['procedure', 'row_num', 'col_num'])
        for key, value in stats.items():
            print(key, value)
            writer.writerow([key] + value)


if __name__ == '__main__':
    stats = {}
    main(sys.argv[1], sys.argv[2])
