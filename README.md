# travel-stackexchange

This repo contains an analysis of a travel stackexchange .xml data dump and includes the following steps:

1. Converting raw xml to a MySQL database schema
2. Data cleaning - working with xml and html
3. Data exploration - asking data questions and visualizing results
4. Model building including a sentiment analysis problem (classification)

Steps 1. and 2. are shown in the XML2MySQL.ipynb.

Files having to do with data exploration are prefixed Data Exploration - this includes the lda.html file that is too large to render inside the browser on Github. For best results, open this file in Google Chrome.

Model building files are prefixed accordingly based on their objective. So far, I only have a sentiment analysis file - more to come.

All steps have been modularized for reproducability on any of the 350 stackexchange forum data dumps. Classes are found in the .py files.

This repo demonstrates knowledge in the following areas:

* Python
* Parsing xml
* Parsing html
* Database architecture
* Querying a database using complex queries
* Working with Pandas DataFrames Objects
* Object Oriented Programming
* Visualizing results
* Model building
* Ability to ask questions

This repo is part of my journey to becoming a "full-stack" data scientist. Comments and feedback are much appreciated.

 -TJ
