import pyreadstat
import pandas as pd

files = [
    "3_LASI_W1_Individual_23-03-22.csv",
    "6_LASI_W1_CV_deathmemberfile_23-03-22.csv"
    ]


'''
Required Colums in 3_LASI_W1_Individual_23-03-22.csv
prim_key, dm005, dm028_totalmarriage, dm003, ht003, ht002, fm303s1, fm303s2, fm303s3, fm303s4, fm303s5, fm303s6, fm303s7, fm304, fm304s1, fm304s2, fm304s3, fm304s4, fm304s5, fm304s6, fm304s7

"dm005": "Age at last birthday", : Individual
"dm028_totalmarriage": "Total number of marriages", : individual 
"dm003": "Sex of the respondent", : individual
"ht003": "Ever diagnosed_diabetes", : individual
"ht002": "Ever diagnosed_hypertension", : individual
"fm303s1": "Hypertension  1 Father",
    "fm303s2": "Hypertension  2 Mother",
    "fm303s3": "Hypertension  3 Brother",
    "fm303s4": "Hypertension  4 Sister",
    "fm303s5": "Hypertension  5 Children",
    "fm303s6": "Hypertension  6 Grandchildren",
    "fm303s7": "Hypertension  7 None",

"fm304": "Family history of diabetes",
    "fm304s1": "Diabetes 1 Father",
    "fm304s2": "Diabetes 2 Mother",
    "fm304s3": "Diabetes 3 Brother",
    "fm304s4": "Diabetes 4 Sister",
    "fm304s5": "Diabetes 5 Children",
    "fm304s6": "Diabetes 6 Grandchildren",
    "fm304s7": "Diabetes 7 None",

    "dm017_villagetown": "Place of birth-village/town", : individual

Required Columns 6_LASI_W1_CV_deathmemberfile_23-03-22.csv
prim_key, residence
# "residence": "Place of residence", : deathmemberFile

'''

# Extraccting data and merging using prim_key

df1 = pd.read_csv(files[0])
# df2 = pd.read_csv(files[1])

columns = {
    "dm005": "Age at last birthday",
    "dm028_totalmarriage": "Total number of marriages",
    "dm003": "Sex of the respondent",
    "ht003": "Ever diagnosed_diabetes",
    "ht002": "Ever diagnosed_hypertension",
    "fm303s1": "Hypertension  1 Father",
    "fm303s2": "Hypertension  2 Mother",
    "fm303s3": "Hypertension  3 Brother",
    "fm303s4": "Hypertension  4 Sister",
    "fm303s5": "Hypertension  5 Children",
    "fm303s6": "Hypertension  6 Grandchildren",
    "fm303s7": "Hypertension  7 None",
    "fm304": "Family history of diabetes",
    "fm304s1": "Diabetes 1 Father",
    "fm304s2": "Diabetes 2 Mother",
    "fm304s3": "Diabetes 3 Brother",
    "fm304s4": "Diabetes 4 Sister",
    "fm304s5": "Diabetes 5 Children",
    "fm304s6": "Diabetes 6 Grandchildren",
    "fm304s7": "Diabetes 7 None",
    "dm017_villagetown": "Place of birth-village/town",
    "residence": "Place of residence",
    "we004": "Working",
    "state": "State",
    # "we014b": "Kind of job",
    # "we016": "Type of main job",
    "dm008": "Highest level of education",


}

trimed_df1 = df1[["prim_key", "dm005", "dm028_totalmarriage", "dm003", "ht003", "ht002", "fm303s1", "fm303s2", "fm303s3", "fm303s4", "fm303s5", "fm303s6", "fm303s7", "fm304", "fm304s1", "fm304s2", "fm304s3", "fm304s4", "fm304s5", "fm304s6", "fm304s7", "dm017_villagetown","we004","residence","state","dm008"]]

# change column names
trimed_df1.rename(columns=columns, inplace=True)

# save the trimmed df1
trimed_df1.to_csv("csv_data/final.csv", index=False)
