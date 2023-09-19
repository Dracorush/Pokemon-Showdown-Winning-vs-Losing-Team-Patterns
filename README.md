# Pokemon-Showdown-Winning-vs-Losing-Team-Patterns
### Data visualization of patterns between the Winning and Losing team across 10,000 Gen 9 OU Pokemon Showdown matches.
# How does it work?
### The battle info is collected by locally storing the json associated with each battle on the Gen 9 OU Pokemon Showdown Replay page. By running  Then the data is cleaned based on different criteria, so that only relevant info is extracted from each json and converted to text files. Data in these text files are compared to each other across several metrics and are graphed for visualization.
# What do I need to install for the code to run?
## fuzzywuzzy
## plotly
# Steps to run the code
### 1. Run DSPSiterativejson.py
### 2. DSPSrealcleaning.py
### 3. Run DSPSjson2extraction.py
### 4. Run any of the other DSPS files
