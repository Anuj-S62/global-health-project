import pandas as pd
import matplotlib as plt
import seaborn as sns
import numpy as np

file = "csv_data/final.csv"

# pre-processing


'''
# dataset

# prim_key,
# Age at last birthday,
# Total number of marriages,
# Sex of the respondent,
# Ever diagnosed_diabetes,
# Ever diagnosed_hypertension,
# Hypertension  1 Father,
# Hypertension  2 Mother,
# Hypertension  3 Brother,
# Hypertension  4 Sister,
# Hypertension  5 Children,
# Hypertension  6 Grandchildren,
# Hypertension  7 None,
# Family history of diabetes,
# Diabetes 1 Father,
# Diabetes 2 Mother,
# Diabetes 3 Brother,
# Diabetes 4 Sister,
# Diabetes 5 Children,
# Diabetes 6 Grandchildren,
# Diabetes 7 None,
# Place of birth-village/town
# Working
# 101000100040101,70,1.0,1,2.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,7,0.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0
# 101000100040102,68,1.0,2,1.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,1,1.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0

1: male
2: female

1: yes
2: no
'''

df = pd.read_csv(file)
print(len(df))

def preprocess():
    # drop all the rows with missing values and reset the index
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    # if family history does not contains integer values, drop the row

    if df["Family history of diabetes"].dtype != np.int64:
        df.drop(df[df["Family history of diabetes"].str.isnumeric() == False].index, inplace=True)
        df.reset_index(drop=True, inplace=True)
    

preprocess()

# ave
print(len(df))  
df.to_csv("csv_data/final3.csv", index=False)

def find_number_of_diabetes():
    # find the number of people with diabetes based on gender: 1: male and 2: female

    # Sex of the respondent with value 2.0
    gender = df["Sex of the respondent"]
    diabetes_status = df["Ever diagnosed_diabetes"]
    working_status = df["Working"]

    print(gender.value_counts())
    total_males = gender.value_counts()[1]
    total_females = gender.value_counts()[2]
    # no of males having Ever diagnosed_diabetes = 1 
    
    print(total_males)
    print(total_females)
    males_with_diabetes = 0
    females_with_diabetes = 0
    males_with_diabetes_and_working = 0
    females_with_diabetes_and_working = 0

    for i in range(len(diabetes_status)):
        if gender[i] == 1 and diabetes_status[i] == 1:
            males_with_diabetes += 1
            if working_status[i] == 1:
                males_with_diabetes_and_working += 1
        elif gender[i]==2 and diabetes_status[i] == 1:
            females_with_diabetes += 1
            if working_status[i] == 1:
                females_with_diabetes_and_working += 1

    
    print("Number of males with diabetes : " + str(males_with_diabetes))
    print("Percentage : " + str((males_with_diabetes/total_males)*100)) 
    print("Number of females with diabetes : " + str(females_with_diabetes))
    print("Percentage : " + str((females_with_diabetes/total_females)*100)) 

    
    print("Number of males with diabetes and working : " + str(males_with_diabetes_and_working))
    print("Percentage of males working given that they have diabetes: " + str((males_with_diabetes_and_working/males_with_diabetes)*100))
    print("Percentage of males with diabetes working: " + str((males_with_diabetes_and_working/total_males)*100))
    
    print("Number of females with diabetes and working : " + str(females_with_diabetes_and_working))
    print("Percentage of females working given that they have diabetes: " + str((females_with_diabetes_and_working/females_with_diabetes)*100))
    print("Percentage of females with diabetes working: " + str((females_with_diabetes_and_working/total_females)*100))


find_number_of_diabetes()

