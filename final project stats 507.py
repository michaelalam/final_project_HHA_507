# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:42:51 2020

@author: Michael Lam
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 14:48:54 2020
@author: hantswilliams
TO RUN: 
    streamlit run week13_streamlit.py
"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2



def get_all_hospitals(name: str):
    for hospital_name in df_hospital_2['hospital_name']:
        if(name.lower() in hospital_name.lower()):
            print(hospital_name)
            
def get_sum_by_group(df, group_name: str, quantity_name: str):
    costs = df.groupby(group_name)[quantity_name].sum().reset_index()
    costs[quantity_name] = costs[quantity_name].astype('float64')
    return costs
    

st.title('Medicare —Hey this is a comparison between Stony Brook University Hospital and Mount Sinai Hospital - NY')



    
    
# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)
  

st.write('Hello, *World!* :sunglasses:') 
  
# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()







hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']


#Bar Chart
st.subheader('Hospital Type - NY')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('The majority of hospitals in NY are acute care, followed by psychiatric')


st.subheader('With a PIE Chart:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)



st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)


#Timeliness of Care
st.subheader('NY Hospitals - Timelieness of Care')
bar2 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national\
        average as it relates to timeliness of care')



#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('Drill Down into INPATIENT data')


inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured: ' )
st.header( str(total_inpatient_count) )



##Common D/C 

common_discharges = inpatient_ny.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.header('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)




#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.title('COSTS')

bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)



#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)



# hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
# hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
# filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
# st.dataframe(filtered)

# lets you type in the name of a hospital and returns a list of that hospital
# You can use upper or lower case
# print(get_all_hospitals(""))

# prints all the columns you have access to in the dataframe
# you can access the information in the columns like df['column_name'] e.g. df_hospital_2['hospital_name']
# print(df_hospital_2.columns)

# prints all the hospital names

#for hospital_name in df_hospital_2['hospital_name']:
#    print(hospital_name)


###to serach for the hospitals 
##for hospital_name in sorted(df_hospital_2['hospital_name']):
##if("sinai" in lower(hospital_name)):
### print(hospital_name)

#for hospital_name in sorted(df_hospital_2['hospital_name']):
#    if("sinai" in lower(hospital_name)):
#        print(hospital_name)




#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']



#This section here lets you plot a bar graph based on the group_name, quality_name and dataframe you provide
#The parameters are:
#data_frame = whatever dataframe you're using
#group_name = The column name you want to group by
#quantity_name = The column name you want to take the sum of
#where clase (on the sum_by_group line) = whatever you want to filter by

data_frame = inpatient_ny
group_name = "provider_name"
quantity_name = "average_covered_charges"
sum_by_group = get_sum_by_group(data_frame.dropna(), group_name, quantity_name)

# This parts plots the data above to your website
bar_avg_payments = px.bar(sum_by_group, x = group_name, y = quantity_name)
st.header("average cover charges vs payments")
st.plotly_chart(bar_avg_payments)




#data_frame = inpatient_ny
#group_name = "provider_name"
#quantity_name = "average_total_payments"
#sum_by_group = get_sum_by_group(data_frame.where(data_frame["hospital_name"]).dropna(), group_name, quantity_name)

# This parts plots the data above to your website
#bar_avg_payments = px.bar(sum_by_group, x = group_name, y = quantity_name)
#st.header("average cover charges vs payments")
#st.plotly_chart(bar_avg_payments)


# WE WANT TO USE "MOUNT SINAI HOSPITAL" AND "SUNY/STONY BROOK UNIVERSITY HOSPITAL"

 
costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


stony_brook_costs_sum = costs_sum.where(costs_sum["provider_name"] == "UNIVERSITY HOSPITAL ( STONY BROOK )").dropna()
mount_sinai_costs_sum = costs_sum.where(costs_sum["provider_name"] == "MOUNT SINAI HOSPITAL").dropna()

st.header("Hospitals")
st.subheader("Stony Brook and Mount Sinai")
st.dataframe(stony_brook_costs_sum)
st.dataframe(mount_sinai_costs_sum)

st.subheader("New York")
st.dataframe(costs_sum)

for col_name, series in stony_brook_costs_sum.items():
    st.markdown(f"**{col_name}: {series.values}**" )
    
for col_name, series in mount_sinai_costs_sum.items():
    st.markdown(f"**{col_name}: {series.values}**" )
    
stony_sinai_differences = []
stony_sinai_differences.append("Differences")
stony_np = stony_brook_costs_sum.to_numpy()
sinai_np = mount_sinai_costs_sum.to_numpy()
for i in range(1, 4):
    stony_sinai_differences.append(stony_np[0][i] - sinai_np[0][i])

st.header("Stony Brook Minus Mount Sinai Payments")
st.subheader("Mount Sinai compared to Stony Brook University Hospital makes more more revenue in medicare and total payments. Delta represents the difference between the total payments and medicare payments.")
st.markdown(f"Average Total Payments: **{stony_sinai_differences[1]}**")
st.markdown(f"Average Medicare Payments: **{stony_sinai_differences[2]}**")
st.markdown(f"Delta: **{stony_sinai_differences[3]}**")



stony_brook_inpatients = df_inpatient_2.where(df_inpatient_2["provider_name"] == "UNIVERSITY HOSPITAL ( STONY BROOK )").dropna().groupby("provider_name")["total_discharges"].sum().reset_index()
mount_sinai_inpatients = df_inpatient_2.where(df_inpatient_2["provider_name"] == "MOUNT SINAI HOSPITAL").dropna().groupby("provider_name")["total_discharges"].sum().reset_index()
st.header("Discharge Information")
st.subheader("Stony Brook and Mount Sinai Discharges")
st.dataframe(stony_brook_inpatients)
st.dataframe(mount_sinai_inpatients)

for col_name, series in stony_brook_inpatients.items():
    st.markdown(f"**{col_name}: {series.values}**" )
    
for col_name, series in mount_sinai_inpatients.items():
    st.markdown(f"**{col_name}: {series.values}**" )
