# Pokemon-Showdown-Winning-vs-Losing-Team-Patterns
### Data visualization of patterns between the Winning and Losing team across thousands of Gen 9 OU Pokemon Showdown matches.
## How does it work?
The battle info is collected by locally storing the json file associated with each battle on the Gen 9 OU Pokemon Showdown Replay page. Then the data is cleaned based on different criteria, so that outliers are removed. Relevant info is then extracted from each json and converted to text files. Data in these text files are compared to each other across several metrics and are graphed for visualization.
## What do I need to install for the code to run?
Google Chrome
Selenium
Requests
BeautifulSoup4
FuzzyWuzzy
Plotly
Pandas
## Steps to run the code
#### 1. Open the zip file containing all of the code.
#### 2. Enter the directory containing Pokemon-Showdown-Winning-vs-Losing-Team-Patterns-main on your terminal using the cd command. Then enter this directory by running cd Pokemon-Showdown-Winning-vs-Losing-Team-Patterns on your terminal.
#### 3. Run DSPSiterativejson.py. 
This is the webscraping process. You should see an automated Google Chrome app open up and try scrolling down as far as possible on the Gen 9 OU Pokemon Showdown replay page. All the game files' jsons are then added to a folder inside Pokemon-Showdown-Winning-vs-Losing-Team-Patterns called gen9ou-matchjson. This entire process usually takes 5-10 minutes and at the end you'll likely have at least 1000 json files of battles stored in this folder. If you want to collect more than just one iteration of json files, I recommend you run DSPSiterativejson.py every 48 hours since battles are discarded after 48 hours.
#### 4. Run DSPSrealcleaning.py. 
This process removes any json files which don't have 6 pokemon on each team and either don't have at least 3 faints for the losing team or at least 10 turns in the entire battle. All the cleaned json files will be placed in a filtered directory called filteredgen9ou-matchjsons.
## 5. Run DSPSjson2extraction.py. 
This will extract relevant info from each json file, and write it into a txt file for each json. These txt files are stored in a directory called gen9ou-stat_summary.
## 6. Run any of the other DSPS files (DSPS_move_cat_counts.py, DSPS_rating_distribution.py, DSPS_stat_counts.py, DSPS_type_counts.py).
You will see the output graph displayed on Plotly.
