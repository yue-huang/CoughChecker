# CoughChecker
Scripts for exploring CDC data and training models to check cough-related symptoms.

## Preprocessing
Convert raw data from stata to CSV file.
```
convert_stata_to_csv.r
```
EDA.
```
EDA.py
EDA.ipynb
```
Select and modify features based on manual curation and missing data.
```
select_curate_features.py
```
Convert reasons and diagnoses.
```
convert_reason_diagnosis.py
```
Scale numerical features, convert categorical features to binary values.
```
transform.py
```

## Model fitting
Train models using logistic regression and random forests.
```
learning_and_EDA.ipynb
```

## Web app
Build a web app to check user's cough-related symptoms.
```
website
```
