import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np


#dropna - drop empty. drop_dumplicates - returns data frame without dupes. reset index. New indexes after removing dupes and empty and inserts the new index as colomn.
df_ny = pd.read_csv("C:/Users/cnilo/Documents/Node/DataKom/Examples/nodeJS-example/data-move-test/pandas/Datasets/Weather/2342202.csv").dropna().drop_duplicates().reset_index(drop = True)
#gives the first few rows to show example of df
df_ny.head()
#New Series called Area and Country.  
df_ny[["Area", "Country"]] = df_ny["NAME"].str.split(", ", 1, expand = True) #SERIES.str so we can use string methods
df_ny[["City", "Country"]] = df_ny["Country"].str.split(" ", 1, expand = True) #expand = True Returns dataframe instead of list


df_moscow = pd.read_csv("C:/Users/cnilo/Documents/Node/DataKom/Examples/nodeJS-example/data-move-test/pandas/Datasets/Weather/2342206.csv")
df_moscow = df_moscow.dropna().drop_duplicates().reset_index(drop = True)

df_moscow[["City", "Country"]] = df_moscow["NAME"].str.split(", ", expand = True)
print(df_moscow.head())
