# Pokemon-Showdown-Winning-vs-Losing-Team-Patterns
### Data visualization of patterns between the Winning and Losing team across 10,000 Gen 9 OU Pokemon Showdown matches.
# How does it work?
### The battle info is collected by locally storing the json associated with each battle on the Gen 9 OU Pokemon Showdown Replay page. Then the data is cleaned based on different criteria, so that outliers are removed. Relevant info is then extracted from each json and converted to text files. Data in these text files are compared to each other across several metrics and are graphed for visualization.
# What do I need to install for the code to run?
## Google Chrome
## Selenium
## Requests
## BeautifulSoup4
## FuzzyWuzzy
## Plotly
# Steps to run the code
### 1. Open the zip file containing all of the code
### 2. Enter the directory containing all of the files by running cd Pokemon-Showdown-Winning-vs-Losing-Team-Patterns on your terminal.
### 1. Run DSPSiterativejson.py. This is the webscraping process. You should see an automated Google Chrome app open up and try scrolling down as far as possible on the Gen 9 OU Pokemon Showdown replay page. All the game files' jsons are then added to a folder inside Pokemon-Showdown-Winning-vs-Losing-Team-Patterns called gen9ou-matchjson. This entire process usually takes 5-10 minutes and at the end you'll likely have at least 1000 json files of battles stored in this folder.
### 2. Run DSPSrealcleaning.py. This process removes any json files which doesn't have 6 pokemon on each team and either doesn't have at least 3 faints for the losing team or at least 10 turns in the entire battle. All the cleaned json files will be placed in a filtered directory called filteredgen9ou-matchjsons.
### 3. Run DSPSjson2extraction.py. This will extract relevant info from each json file, and convert all of the info into a txt file for each json and store them in a directory called gen9ou-stat_summary.
### 4. Run any of the other DSPS files. You will see the output graph displayed on plotly.
