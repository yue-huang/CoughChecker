# Usage: python3 select_diagnosis.py df_cough_2014.csv_convertNA.csv_convertRD.csv

import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def col_name_cond(col_name):
    return (col_name.startswith('D_1') or
         col_name.startswith('D_2') or
         col_name.startswith('D_3') or
         col_name.startswith('D_4') or
         col_name.startswith('D_5') or
         col_name.startswith('D_6') or
         col_name.startswith('D_7') or
         col_name.startswith('D_8') or
         col_name.startswith('D_9') or
         col_name.startswith('D_0'));


def main(data_csv_name):
    df = pd.read_csv(data_csv_name)
    df2 = pd.DataFrame()
    for colname in df.columns:
        if not col_name_cond(colname):
            print(colname)
            df2[colname] = df[colname]
    df2.to_csv(sys.argv[1] + '_selected.csv', index = False)
    print('shape of original and subsetted data is:', df.shape, df2.shape)

if __name__ == '__main__':
    main(sys.argv[1])
