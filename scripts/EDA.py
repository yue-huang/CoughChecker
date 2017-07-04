# Usage: EDA.
# Use the code snippet in each section.

import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read in CDC file
df = pd.read_csv('namcs2014_stata.csv')
df.shape  # 45710x1105
len(df[df.RFV1 == 14400])

# Select patients with cough symptom
df_cough = df[(df['RFV1'] == 14400) | (df['RFV2'] == 14400) | (
    df['RFV3'] == 14400) | (df['RFV4'] == 14400) | (df['RFV5'] == 14400)]
df_cough.shape  # 1907x1105
df_cough.to_csv('df_cough_2014.csv', index=False)

# Check which reason the cough symptom lies in
objects = ('No cough', 'Reason1', 'Reason2', 'Reason3', 'Reason4', 'Reason5')
y_pos = np.arange(len(objects))
numbers = [len(df) - len(df_cough), len(df[df.RFV1 == 14400]), len(df[df.RFV2 == 14400]),
           len(df[df.RFV3 == 14400]), len(df[df.RFV4 == 14400]), len(df[df.RFV5 == 14400])]
# alpha: 0.0 transparent through 1.0 opaque
plt.bar(y_pos, numbers, align='center', log=True, alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Number of patients')
plt.title('Statistics of cough')
plt.savefig('stats_of_cough.png')

plt.close("all")

# Check how many unique reasons for patients to come to clinic
df_cough = pd.read_csv('df_cough_2014.csv')

symptoms = df_cough.RFV1.append(
    [df_cough.RFV2, df_cough.RFV3, df_cough.RFV4, df_cough.RFV5])  # 9535
# 3696, 299 unique symptoms (-9 (NA) has 3561, 14400 (cough) has 1907, >30000 (not symptoms nor diseases) has 371).
symptoms_meaningful = symptoms[(symptoms != -9)
                               & (symptoms != 14400) & (symptoms < 30000)]
symptoms.plot.hist(bins=500)
plt.xticks(range(10000, 32000, 2000), rotation=45, fontsize=5)
plt.savefig('stats_reason_meaningful_500.png')

# Check how many reasons each patient has to come to clinic
symptom_num = []
for index, row in df_cough.iterrows():
    if row.RFV2 == -9:
        n = 0
    elif row.RFV3 == -9:
        n = 1
    elif row.RFV4 == -9:
        n = 2
    elif row.RFV5 == -9:
        n = 3
    else:
        n = 4
    symptom_num.append(n)

plt.hist(symptom_num)
plt.xticks(range(5))
plt.title('Number of reasons besides cough')

# Check how many unique diagnoses that patients have
diagnoses = df_cough.DIAG1.append(
    [df_cough.DIAG2, df_cough.DIAG3, df_cough.DIAG4, df_cough.DIAG5])
diagnosesR = df_cough.DIAG1R.append(
    [df_cough.DIAG2R, df_cough.DIAG3R, df_cough.DIAG4R, df_cough.DIAG5R])
# 4184, 669 unique diagnoses (-9 has 5092, >200000 (other factors and NAs) has 259)
diagnosesR_meaningful = diagnosesR[(diagnosesR != -9) & (diagnosesR < 200000)]
diagnosesR_meaningful.plot.hist(bins=200)
plt.xticks(range(100000, 210000, 10000), rotation=45, fontsize=7)
plt.title('statistics of diagnoses')
plt.savefig('stats_diagnosis_meaningful_200.png')

# Get summary statistics of diagnoses
df = pd.read_csv('df_cough_2014.csv_convertNA.csv_convertRD.csv')
diagnosis_names = []
for colname in df.columns:
    if colname.startswith('D_'):
        diagnosis_names.append(colname)
diagnosis_sum = df[diagnosis_names].sum(axis=0)
diagnosis_sum.to_csv('stats_diagnosis.csv')
