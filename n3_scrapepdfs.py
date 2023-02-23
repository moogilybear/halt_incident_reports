#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:20:45 2023

@author: meaganpatrick
"""
#import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
##for calculating the number of months since the reports started being outputted 
import datetime
##for reading the file names in the folder
import glob
##for reading the pdfs
import tabula
import pdfquery
import re
import datetime
import calendar
import matplotlib.pyplot as plt

#define download directory 
download_dir = "downloads/halt/"

# Now that all of the pdf reports are downloaded, 
# Use glob to get a list of PDF files in the folder, with their extensions.
pdf_files = glob.glob(download_dir+'*.pdf')

# Create a DataFrame with the PDF file names
pdf_df = pd.DataFrame({'filename': pdf_files})

#check to make sure they are correct.
print(pdf_df)

# now, we want to scrape each of the pdfs, and store each pdf into a dataframe
# for each month. to do that, we will create an empty dictionary to store the month dataframes
dfs = {}

# loop through each file name in the directory and read the tables from the PDF
for filename in os.listdir(download_dir):
    
    # read the tables from the PDF and concatenate all tables into one dataframe
    filepath = os.path.join(download_dir,filename)  # add path to filename
    tables = tabula.read_pdf(filepath, multiple_tables=True, guess=False, pages="all")
    df = pd.concat(tables, ignore_index=True)

    # drop any rows that contain all NaN values
    df.dropna(how='all', inplace=True)

    # get the last two words of the filename and use them as the dataframe name
    df_name = filename.split('-')[-2:]
    df_name = '_'.join(df_name).replace('.pdf', '')
    
    # add the dataframe to the dictionary with the appropriate name
    dfs[df_name] = df
    
#you can take a look at dataframes by entering their month_year, like such:
#april_2022=dfs['april_2022']

#Concatenate the dataframes so that they are one large table. This table will need to be cleaned.
uncleaned=pd.concat(dfs, ignore_index=True)

# iterate over the items in the dictionary and save each dataframe as a csv
# create the directory if it doesn't exist
if not os.path.exists('data/uncleaned'):
    os.makedirs('data/uncleaned')

for filename, dataframe in dfs.items():
    dataframe.to_csv(f'data/uncleaned/{filename}.csv', index=False)

uncleaned.to_csv('data/uncleaned/concatenated_data.csv', index=False)