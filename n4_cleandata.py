#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:21:45 2023

@author: meaganpatrick
"""
#import packages
import pandas as pd
import numpy as np
import os
import datetime
import glob
import re
import datetime
import calendar
import matplotlib.pyplot as plt

uncleaned=pd.read_csv('data/uncleaned/concatenated_data.csv')

#rename the columns so they are easier to work with. 
num_cols = len(uncleaned.columns)
new_col_names = [f'c{i}' for i in range(1, num_cols + 1)] ## create a list of new column names with the format "c1", "c2", "c3", etc.
uncleaned.columns = new_col_names # rename the columns of the dataframe
    #Some of the data imported in a different way than other data. 
#we will need to split them out into version 1 and version 2, and clean them separately.
#let's start where c7 is null, or not null

#Some of the data imported in a different way than other data. 
#we will need to split them out into version 1 and version 2, and clean them separately.
#let's start where c7 is null, or not null
#clean the data

uncleaned['c4_filled'] = uncleaned['c4'].fillna(' ')
cd=uncleaned[~uncleaned['c4_filled'].str.contains('Infractions')]
cd1=cd[~cd['c4_filled'].str.contains('Incidents')]
cd2=cd1[~cd1['c1'].isna()]
cd3=cd2[~cd2['c2'].isna()]
cd4=cd3[~cd3['c4_filled'].str.contains('TIER')]
#Time issue is when c3 is null
cd5=cd4[~cd4['c4_filled'].str.contains("Date")]
#Issue with columns being squished is when c11 is NA
cd5[cd5['c11'].isna()]

#fix squished issue
cd5[['col1','col2','col3','col4','col5','col6','col7','col8','col9','col10','col11','col12','col13','col14','col15','col16','col17']]=cd5['c4_filled'].str.split('(\d+)', expand=True)
cd5['col456']=cd5['col4']+cd5['col5']+cd5['col6']
cd5['col8910']=cd5['col8']+cd5['col9']+cd5['col10']
cd5['col121314']=cd5['col12']+cd5['col13']+cd5['col14']
cd5[['tier', 'rest', 'tot_infractions']] = cd5['c4_filled'].str.extract(r'^(\d+)\s+(.*?)\s+(\d+)$')
missing_c11 = cd5['c11'].isna()
cd5.loc[missing_c11, 'c12'] = cd5.loc[missing_c11, 'c5']
cd5.loc[missing_c11, 'c13'] = cd5.loc[missing_c11, 'c6']
cd5.loc[missing_c11, 'c4'] = cd5.loc[missing_c11, 'tier']
cd5.loc[missing_c11, 'c11'] = cd5.loc[missing_c11, 'tot_infractions']
cd5.loc[missing_c11, 'c10'] = cd5.loc[missing_c11, 'col15']
cd5.loc[missing_c11, 'c9'] = cd5.loc[missing_c11, 'col121314']
cd5.loc[missing_c11, 'c8'] = cd5.loc[missing_c11, 'col11']
cd5.loc[missing_c11, 'c7'] = cd5.loc[missing_c11, 'col8910']
cd5.loc[missing_c11, 'c6'] = cd5.loc[missing_c11, 'col7']
cd5.loc[missing_c11, 'c5'] = cd5.loc[missing_c11, 'col456']

#fix time issue
cd5[['column1','column2','column3']]=cd5['c2'].str.split('(\d+)', expand=True)
missing_c3 = cd5['c3'].isna()
cd5.loc[missing_c3, 'c2'] = cd5.loc[missing_c3, 'column2']
cd5.loc[missing_c3, 'c3'] = cd5.loc[missing_c3, 'column3']

cd6=cd5[['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13']]

cd7 = cd6[cd6['c1'].str.len() > 4]
cd8 = cd6[cd6['c1'].str.len() <= 4]

cd8.columns=['time','facility','tier','date','g1','g1_label','g2','g2_label','g3','g3_label','tot_infractions','tot_g_infractions','orig_shu_days']
cd7.columns=['date','time','facility','tier','g1','g1_label','g2','g2_label','g3','g3_label','tot_infractions','tot_g_infractions','orig_shu_days']
cd9=cd7[['time','facility','tier','date','g1','g1_label','g2','g2_label','g3','g3_label','tot_infractions','tot_g_infractions','orig_shu_days']]

new=pd.concat([cd9,cd8],axis=0)
new=new[~new['date'].str.contains('Infractions')]
new['facility']=new['facility'].str.strip()

new.to_csv('data/final.csv',index=False)

