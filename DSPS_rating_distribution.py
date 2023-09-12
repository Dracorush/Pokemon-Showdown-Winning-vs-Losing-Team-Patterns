import os
import math
import plotly.graph_objects as go

# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize an empty list to store rating estimates
rating_estimates = []

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

# Create a histogram using Plotly
fig = go.Figure(data=[go.Histogram(x=rating_estimates, nbinsx=30)])
fig.update_layout(
    xaxis_title="Rating Estimate",
    yaxis_title="Frequency",
    title="Distribution of Rating Estimates"
)

# Enable scroll zoom
config = {'scrollZoom': True}
fig.show(config=config)
