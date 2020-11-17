import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import glob

#dropna - drop empty. drop_dumplicates - returns data frame without dupes. reset index. New indexes after removing dupes and empty and inserts the new index as colomn.
df_ny = pd.read_csv("C:/Users/cnilo/Documents/DataKomTest/Examples/nodeJS-example/data-move-test/pandas/Datasets/Weather/2342202.csv").dropna().drop_duplicates().reset_index(drop = True)
#gives the first few rows to show example of df
df_ny.head()
#New Series called Area and Country.  
df_ny[["Area", "Country"]] = df_ny["NAME"].str.split(", ", 1, expand = True) #SERIES.str so we can use string methods
df_ny[["City", "Country"]] = df_ny["Country"].str.split(" ", 1, expand = True) #expand = True Returns dataframe instead of list


df_moscow = pd.read_csv("C:/Users/cnilo/Documents/DataKomTest/Examples/nodeJS-example/data-move-test/pandas/Datasets/Weather/2342206.csv")
df_moscow = df_moscow.dropna().drop_duplicates().reset_index(drop = True)

df_moscow[["City", "Country"]] = df_moscow["NAME"].str.split(", ", expand = True)

df_ny_x_mos = pd.concat([df_ny, df_moscow], axis=0)


dfs = []
weather_files = glob.glob("C:/Users/cnilo/Documents/DataKomTest/Examples/nodeJS-example/data-move-test/pandas/Datasets/Weather/*.csv")
for i, path in enumerate(weather_files):
    df = pd.read_csv(path).dropna().drop_duplicates().reset_index(drop = True)
    df[["Area", "Country"]] = df["NAME"].str.split(", ", expand = True)
    dfs.append(df)

#df_all = pd.concat(dfs, axis=0)

df_trondheim = pd.read_csv("C:/Users/cnilo/Documents/DataKomTest/Examples/nodeJS-example/data-move-test/pandas/Datasets/Weather/extra/trondheim.csv").dropna().drop_duplicates().reset_index(drop = True)
df_trondheim[["Area", "Country"]] = df_trondheim["NAME"].str.split(", ", expand = True)
df_trondheim["TAVG"] = (df_trondheim.TMAX + df_trondheim.TMIN) /2
df_trondheim.drop(labels=["TMAX", "TMIN"], axis=1, inplace = True)
dfs.append(df_trondheim)
df_complete = pd.concat(dfs, axis=0).reset_index(drop = True)
df_continent = pd.read_csv("C:/Users/cnilo/Documents/DataKomTest/Examples/nodeJS-example/data-move-test/pandas/Datasets/countryContinent.csv", encoding = "ISO-8859-1").dropna().drop_duplicates().reset_index(drop = True)
print(df_continent)
df_continent = df_continent[["code_2", "country", "continent"]]
print(df_continent)
df_complete_continent = df_complete.merge(df_continent, left_on="Country", right_on="code_2")
df_complete_continent.drop(labels="code_2", inplace = True, axis = 1)
df_complete_continent.rename(columns= {"Country": "Country Code", "country": "Country", "continent": "Continent"}, inplace = True)
print(df_complete_continent)
