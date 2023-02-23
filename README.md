# halt_incident_reports
HALT Incident Reports April 2022-January 2023

This project was created by Meagan Patrick in February of 2022. It scrapes the NY Department of Corrections website for all URLs to research reports. It then isolates HALT incident reports, downloads them, and scrapes them into a dataframe for descriptive statistical analysis. 

-------------

About HALT: https://www.nysenate.gov/newsroom/press-releases/senate-passes-halt-solitary-confinement-act

-------------

HOW TO USE:

This project relies on four preparatory python files, and then does QA and initial descriptive statistics in a Jupyter notebook. The files have been labeled in the order that they should be run:

1. n1_geturls.py

This code iterates through the DOC website's ajax call to load html for each of the pages on the DOC reports webpage, extracting all URL values. It removes any URLs not to website pages rather than reports, and adds the base URL, and downloading a csv of all report links to downloads/reporturls.csv. 

2. n2_downloadfiles.py

This code takes the reporturls.csv, filters out the Halt Incident Report URLs, and downloads them from the website. It check that the number of reports is adequate, given that a report is issued each month since April 2022. To download the reports, it avoids restrictions on scraping by simulating cookies, browser headings, and including a buffer time of five seconds between downloads. It downloads all files to the downloads/halt/ folder and names them by month (ie: halt-incident-list-november-2022.pdf)

3. n3_scrapefiles.py

This code uses Tabula to scrape the Halt Incident Reports for each month into its own dataframe for the month. It creates a dictionary holding all dataframes. It then concatenate the dataframes together to create a single dataframe 'uncleaned'. All dataframes are downloaded as csvs in /data/uncleaned, including the concatenated dataframe (concatenate_data.csv), as well as dataframes for each month (ie: december_2022.csv). 

4. n4_cleandata.py

This program cleans the data that was scraped from the PDFs came in very messy. Not all of the columns came in the right order, column names were imported as rows, and some of the columns came in as one column. It outputs 'data/final.csv.'

5. n5_qa_describedata_.ipynb

This Jupyter Notebook compares the original uncleaned dataframes and the final cleaned dataframe, ensuring no rows were dropped. It also compares the number of facilities in the final dataframe to a separate list of facilities from the DOC website (sourced here: https://doccs.ny.gov/system/files/documents/2022/09/facility-map-11-1-22.pdf). 

Describing the data, there are 7 records which do not have a facility coded for them. It downloads these records into a csv ('data/uncodedfacilityrecords.csv'). It also downloads a summary statistics chart (stats.csv). It looks at the number of unique "guilty" codes used, and downloads them in a csv 'unique_guilty_values.csv'. 

It then creates new boolean columns in the 'final' dataframe for each of the "guilty" values, with the intention of a potential future Bayesian analysis once more information is known, and the data can be normalized. This dataframe is downloaded as 'finalwithbooleans.csv'.

Finally, it uses histograms to describe the shape of the data, and looks at top values. 
