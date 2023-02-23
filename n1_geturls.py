#import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

#create/define download directory
download_dir = "downloads/halt/"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

#extract all of the urls using an ajax call which populates each page.
#transform the response to the request into a json. then pull the fourth element
#(fourth element has the html). finally, pull any tags for urls (a href)
def extract_urls(pages):
    all_urls = []
    for num in range(pages):
        response = requests.get(f"https://doccs.ny.gov/research-and-reports?q=/research-and-reports&page={num}&_wrapper_format=drupal_ajax")
        info = response.json()
        html=info[4]['data']
        soup = BeautifulSoup(html, features='lxml')
        page_urls = [link.get("href") for link in soup.find_all("a")]
        all_urls.append(page_urls)
    return all_urls

#run function to extract urls. 
#note: as more reports are added, you may need to update the number of pages. 
urls = extract_urls(60)

#the result will be in a matrix structure, with urls in both columns and rows.
#you will need to flatten it, so that you can make it a dataframe with one column for the urls
def flatten(l):
    return [item for sublist in l for item in sublist]

urlsflat=flatten(urls)

# after flattening, put it into a dataframe.
urldf=pd.DataFrame(urlsflat, columns=['urlnames'])

# Remove all URLs which contain "research-and-reports", as these are not links for the reports,
# but for the pages awithin the website.
urldf=urldf[urldf['urlnames'].str.contains('research-and-reports')==False]

# drop any duplicates
urldf=urldf.drop_duplicates()

#print the number of report urls
print('number of report urls is:',len(urldf))

# add the base html.
urldf['fullurl']='https://doccs.ny.gov'+urldf['urlnames']
print('urlnames is the extension, full url contains the base url with doccs.ny.gov:',urldf)

urldf.to_csv('downloads/reporturls.csv')
