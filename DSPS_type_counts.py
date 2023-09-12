# Code for graphing the differences in concatenated weakness counts
import os
import math
import plotly.graph_objects as go

# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize empty lists to store rating estimates and the difference in weakness counts
rating_estimates = []
difference_in_weakness_counts = []

# Function to calculate average rating
def calculate_average(initial, final):
    return (initial + final) / 2

# Initialize counters for different rating brackets
bracket_counts = {
    "1000-1200": {"positive": 0, "negative": 0},
    "1201-1400": {"positive": 0, "negative": 0},
    "1401-1600": {"positive": 0, "negative": 0},
    "1601-1800": {"positive": 0, "negative": 0},
    "1801-2000": {"positive": 0, "negative": 0}
}

# Iterate over the file names
for file_name in os.listdir(directory):
    if file_name.startswith("stat_summary_gen9ou-") and file_name.endswith(".txt"):
        # Extract the unique number from the file name
        file_number = file_name.split("-")[1].split(".")[0]
        
        # Construct the full file path
        file_path = os.path.join(directory, file_name)

        # Read the contents of the single text file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Initialize empty lists for weakness counts
        winning_team_weakness_counts = []
        losing_team_weakness_counts = []

        # Loop through the lines and extract weakness counts
        for i, line in enumerate(lines):
            if "Winning Team Weakness Counts (List):" in line:
                winning_team_weakness_counts = list(map(int, lines[i + 1].strip('[]\n').split(', ')))
            elif "Losing Team Weakness Counts (List):" in line:
                losing_team_weakness_counts = list(map(int, lines[i + 1].strip('[]\n').split(', ')))
            if winning_team_weakness_counts and losing_team_weakness_counts:
                break
        
        # Check if the lists are non-empty before concatenation
        if winning_team_weakness_counts:
            winning_team_concatenated = int("".join(map(str, winning_team_weakness_counts)))
        else:
            winning_team_concatenated = 0

        if losing_team_weakness_counts:
            losing_team_concatenated = int("".join(map(str, losing_team_weakness_counts)))
        else:
            losing_team_concatenated = 0

        # Perform the subtraction of concatenated results
        difference_in_weakness_count = winning_team_concatenated - losing_team_concatenated
        difference_in_weakness_counts.append(difference_in_weakness_count)

        # Extract average rating information
        sum_avg_initial = 0
        sum_avg_final = 0
        num_players = 0

        for line in lines:
            if "initial rating:" in line and "final rating:" in line:
                initial_rating = int(line.split("initial rating:")[1].split(",")[0].strip())
                final_rating = int(line.split("final rating:")[1].strip())
                
                avg_initial_rating = calculate_average(initial_rating, final_rating)
                avg_final_rating = calculate_average(initial_rating, final_rating)
                
                sum_avg_initial += avg_initial_rating
                sum_avg_final += avg_final_rating
                num_players += 1

        # Calculate the overall average rating
        overall_avg_initial = sum_avg_initial / num_players
        overall_avg_final = sum_avg_final / num_players

        # Calculate the final rating estimate and round it up
        final_rating_estimate = calculate_average(overall_avg_initial, overall_avg_final)
        rounded_rating_estimate = math.ceil(final_rating_estimate)
        rating_estimates.append(rounded_rating_estimate)

        # Determine the rating bracket
        if 1000 <= rounded_rating_estimate <= 1200:
            bracket = "1000-1200"
        elif 1201 <= rounded_rating_estimate <= 1400:
            bracket = "1201-1400"
        elif 1401 <= rounded_rating_estimate <= 1600:
            bracket = "1401-1600"
        elif 1601 <= rounded_rating_estimate <= 1800:
            bracket = "1601-1800"
        elif 1801 <= rounded_rating_estimate <= 2000:
            bracket = "1801-2000"
        else:
            continue

        # Update the counters for each bracket based on weakness result
        if difference_in_weakness_count > 0:
            bracket_counts[bracket]["positive"] += 1
        elif difference_in_weakness_count < 0:
            bracket_counts[bracket]["negative"] += 1

# Print the counts for each rating bracket
for bracket, counts in bracket_counts.items():
    print(f"Rating Bracket: {bracket}")
    print("Frequency of Differences in Concatenated Weakness Counts (Winner - Loser) greater than 0:", counts["positive"])
    print("Frequency of Differences in Concatenated Weakness Counts (Winner - Loser) less than 0:", counts["negative"])
    print()

# Create a DataFrame for the data
import pandas as pd
data = pd.DataFrame({'Rating Estimate': rating_estimates, 'Difference in Weakness Counts (Winner - Loser)': difference_in_weakness_counts})

# Create the scatter plot using Plotly
fig = go.Figure()

# Add the scatter trace
fig.add_trace(go.Scatter(
    x=data['Rating Estimate'],
    y=data['Difference in Weakness Counts (Winner - Loser)'],
    mode='markers',
    marker=dict(size=8)
))

# Update the layout to enable scroll zooming
fig.update_layout(
    title='Scatter Plot of Rating Estimates vs. Differences in Concatenated Weakness Counts (Winner - Loser)',
    xaxis_title='Rating Estimate',
    yaxis_title='Difference in Concatenated Weakness Counts (Winner - Loser)',
    hovermode='closest'
)

# Show the interactive plot with scroll zoom enabled
config = {'scrollZoom': True}
fig.show(config=config)


# Code for graphing the differences in concatenated resist counts 
import os
import math
import plotly.graph_objects as go

# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize an empty list to store rating estimates and type resist subtraction results
rating_estimates = []
type_resist_subtraction_results = []

# Function to calculate average rating
def calculate_average(initial, final):
    return (initial + final) / 2

# Iterate over the file names
for file_name in os.listdir(directory):
    if file_name.startswith("stat_summary_gen9ou-") and file_name.endswith(".txt"):
        # Extract the unique number from the file name
        file_number = file_name.split("-")[1].split(".")[0]
        
        # Construct the full file path
        file_path = os.path.join(directory, file_name)

        # Initialize variables to store the average rating sums
        sum_avg_initial = 0
        sum_avg_final = 0
        num_players = 0

        # Read the contents of the single text file
        with open(file_path, "r") as file:
            lines = file.readlines()
            current_player = None
            player_ratings = {}
            for line in lines:
                if "initial rating:" in line and "final rating:" in line:
                    player = line.split("'s")[0]
                    initial_rating = int(line.split("initial rating:")[1].split(",")[0].strip())
                    final_rating = int(line.split("final rating:")[1].strip())
                    
                    avg_initial_rating = calculate_average(initial_rating, final_rating)
                    avg_final_rating = calculate_average(initial_rating, final_rating)
                    
                    sum_avg_initial += avg_initial_rating
                    sum_avg_final += avg_final_rating
                    num_players += 1

        # Calculate the overall average rating
        overall_avg_initial = sum_avg_initial / num_players
        overall_avg_final = sum_avg_final / num_players

        # Calculate the final rating estimate and round it up
        final_rating_estimate = calculate_average(overall_avg_initial, overall_avg_final)
        rounded_rating_estimate = math.ceil(final_rating_estimate)
        
        # Append the rounded rating estimate to the list
        rating_estimates.append(rounded_rating_estimate)

        # Initialize empty lists for resisting counts
        winning_team_resisting_counts = []
        losing_team_resisting_counts = []

        # Loop through the lines and extract resisting counts
        for i, line in enumerate(lines):
            if "Winning Team Resisting Counts (List):" in line:
                winning_team_resisting_counts = list(map(int, lines[i + 1].strip('[]\n').split(', ')))
            elif "Losing Team Resisting Counts (List):" in line:
                losing_team_resisting_counts = list(map(int, lines[i + 1].strip('[]\n').split(', ')))
            if winning_team_resisting_counts and losing_team_resisting_counts:
                break

        # Calculate the concatenated resisting counts for winning and losing teams
        winning_team_concatenated = int("".join(map(str, winning_team_resisting_counts)))
        losing_team_concatenated = int("".join(map(str, losing_team_resisting_counts)))
        
        # Calculate the subtraction result
        type_resist_subtraction_result = winning_team_concatenated - losing_team_concatenated
        type_resist_subtraction_results.append(type_resist_subtraction_result)

        # Counters for positive and negative subtraction results
        positive_count = 0
        negative_count = 0

        # Initialize counters for different rating brackets
bracket_counts = {
    "1000-1200": {"positive": 0, "negative": 0},
    "1201-1400": {"positive": 0, "negative": 0},
    "1401-1600": {"positive": 0, "negative": 0},
    "1601-1800": {"positive": 0, "negative": 0},
    "1801-2000": {"positive": 0, "negative": 0}
}

# Iterate over the rating estimates and subtraction results
for rating, result in zip(rating_estimates, type_resist_subtraction_results):
    if rating >= 1000 and rating <= 1200:
        if result > 0:
            bracket_counts["1000-1200"]["positive"] += 1
        elif result < 0:
            bracket_counts["1000-1200"]["negative"] += 1
    elif rating >= 1201 and rating <= 1400:
        if result > 0:
            bracket_counts["1201-1400"]["positive"] += 1
        elif result < 0:
            bracket_counts["1201-1400"]["negative"] += 1
    elif rating >= 1401 and rating <= 1600:
        if result > 0:
            bracket_counts["1401-1600"]["positive"] += 1
        elif result < 0:
            bracket_counts["1401-1600"]["negative"] += 1
    elif rating >= 1601 and rating <= 1800:
        if result > 0:
            bracket_counts["1601-1800"]["positive"] += 1
        elif result < 0:
            bracket_counts["1601-1800"]["negative"] += 1
    elif rating >= 1801 and rating <= 2000:
        if result > 0:
            bracket_counts["1801-2000"]["positive"] += 1
        elif result < 0:
            bracket_counts["1801-2000"]["negative"] += 1

# Print the counts for each rating bracket
for bracket, counts in bracket_counts.items():
    print(f"Rating Bracket: {bracket}")
    print("Frequency of Differences in Concatenated Resist Counts (Winner - Loser) greater than 0:", counts["positive"])
    print("Frequency of Differences in Concatenated Resist Counts (Winner - Loser) less than 0:", counts["negative"])
    print()


# Create a DataFrame for the data
import pandas as pd
data = pd.DataFrame({'Rating Estimate': rating_estimates, 'Type Resist Subtraction Results': type_resist_subtraction_results})

# Create the scatter plot using Plotly
fig = go.Figure()

# Add the scatter trace
fig.add_trace(go.Scatter(
    x=data['Rating Estimate'],
    y=data['Type Resist Subtraction Results'],
    mode='markers',
    marker=dict(size=8)
))

# Update the layout to enable scroll zooming
fig.update_layout(
    title='Scatter Plot of Rating Estimates vs. Differences in Concatenated Resist Counts (Winner - Loser)',
    xaxis_title='Rating Estimate',
    yaxis_title='Difference in Concatenated Resist Counts (Winner - Loser)',
    hovermode='closest'
)

# Show the interactive plot with scroll zoom enabled
config = {'scrollZoom': True}
fig.show(config=config)


