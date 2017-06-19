# FSND P3 - Log Analysis
Log Analysis Project using python and PostgreSQL

![](https://github.com/Dongs7/img/blob/master/p3.png)

## Requirements
* Python 2.7.12
* Vagrant
* Oracle Virtual Box
* Flask
* psycopg2
* Twitter Bootstrap 

## File/Folder Description
[template] - folder contains html files
[static]   - folder contains static files (css files)
newsdb.py  - connect to DB and fetch results from the
             DB. Create a new text file from the results
news.py    - Start the localhost server

## How to run this program
Run this program by typing the following command in the terminal:

$ python news.py

1. The program will generate the text output file first. This step might take a few seconds since it needs to fetch the results from the DB. Then, 'result.txt' will be created in the folder.

2. After the first step, the program will start the server so the results from the DB can be displayed in the browser.
Use 'localhost:8000'
