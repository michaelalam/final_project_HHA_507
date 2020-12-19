# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:36:20 2020

@author: Michael Lam
"""

import pandas as pd
import plotly.express as px

def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2

df_hospital_2  = load_hospitals()

def get_all_hospitals(name: str):
    for hospital_name in df_hospital_2['hospital_name']:
        if(name.lower() in hospital_name.lower()):
            print(hospital_name)
            
def get_sum_by_group(df, group_name: str, quantity_name: str):
    costs = df.groupby(group_name)[quantity_name].sum().reset_index()
    costs[quantity_name] = costs[quantity_name].astype('float64')
    return costs
    