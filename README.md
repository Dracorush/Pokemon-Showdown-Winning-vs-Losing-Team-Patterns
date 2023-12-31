# Pokemon-Showdown-Winning-vs-Losing-Team-Patterns
Data visualization of patterns between the Winning and Losing team across thousands of Gen 9 OU Pokemon Showdown matches.
## How does it work?
The battle info is collected by locally storing the json file associated with each battle on the Gen 9 OU Pokemon Showdown Replay page. Then the data is cleaned based on different criteria, so that outliers are removed. Relevant info is then extracted from each json and converted to text files. Data in these text files are compared to each other across several metrics and are graphed for visualization.
## What do I need to install for the code to run?
Google Chrome, Selenium, Requests, BeautifulSoup4, FuzzyWuzzy, Plotly, Pandas
## Steps to run the code
**1. Run DSPSiterativejson.py.** <br>
This is the webscraping process. You should see an automated Google Chrome app open up and try scrolling down as far as possible on the Gen 9 OU Pokemon Showdown replay page. All the game files' jsons are then added to a folder inside Pokemon-Showdown-Winning-vs-Losing-Team-Patterns called gen9ou-matchjson. This entire process usually takes 5-10 minutes and at the end you'll likely have at least 1000 json files of battles stored in this folder. If you want to collect more than just one iteration of json files, I recommend you run DSPSiterativejson.py every 48 hours since battles are discarded after 48 hours. <br>
**2. Run DSPSrealcleaning.py.** <br>
This process removes any json files which don't have 6 pokemon on each team and either don't have at least 3 faints for the losing team or at least 10 turns in the entire battle. All the cleaned json files will be placed in a filtered directory called filteredgen9ou-matchjsons. <br>
**3. Run DSPSjson2extraction.py.** <br>
This will extract relevant info from each json file, and write it into a txt file for each json. These txt files are stored in a directory called gen9ou-stat_summary. <br>
**4. Run any of the other DSPS files (DSPS_move_cat_counts.py, DSPS_rating_distribution.py, DSPS_stat_counts.py, DSPS_type_counts.py).** <br>
You will see each output graph displayed on Plotly.

Here is an example output graph comparing the number of status moves used by the Winning and Losing team across 10,000 games. <br>

![Status_Moves_Graph](https://github.com/Dracorush/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/assets/24494800/938f5262-4bed-40e8-bd8e-eccdce1440db)
All example output graphs can be found through these links: <br> <br>
[Rating Distribution](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/rating_distribution/rating_distribution.html) <br> <br>
[Players vs Number of Status Moves](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/move_cat/status_moves_chart.html) <br> <br>
[Players vs Number of Runswitch Moves](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/move_cat/runswitch_moves_chart.html) <br> <br>
[Players vs Number of Priority Moves](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/move_cat/priority_moves_chart.html) <br> <br>
[Players vs Number of Entry Hazard Moves](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/move_cat/entry_hazard_moves_chart.html) <br> <br>
[Players vs Number of Entry Hazard Clear Moves](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/move_cat/entry_hazard_clear_moves_chart.html) <br> <br>
[Rating Estimate vs Difference in Stat Standard Deviations](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/stat_counts/stat_counts_chart.html) <br> <br>
[Rating Estimate vs Difference in Resist Counts](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/type_counts/difference_in_type_resists_scatterplot.html) <br> <br>
[Rating Estimate vs Difference in Weakness Counts](https://dracorush.github.io/Pokemon-Showdown-Winning-vs-Losing-Team-Patterns/docs/10,000_matches_example/type_counts/difference_in_type_weaknesses_scatterplot.html)
