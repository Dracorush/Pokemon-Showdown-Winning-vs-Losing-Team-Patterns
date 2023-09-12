import os
import math
import plotly.graph_objects as go

# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize empty lists to store rating estimates and standard deviation differences
rating_estimates = []
std_dev_differences = []

# Function to calculate average rating
def calculate_average(initial, final):
    return (initial + final) / 2

# Initialize a dictionary to store counts of points above and below 0 for each rating bracket
rating_bracket_counts = {
    "1000-1200": {"above_zero": 0, "below_zero": 0},
    "1201-1400": {"above_zero": 0, "below_zero": 0},
    "1401-1600": {"above_zero": 0, "below_zero": 0},
    "1601-1800": {"above_zero": 0, "below_zero": 0},
    "1801-2000": {"above_zero": 0, "below_zero": 0}
}

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

            # Initialize lists for winning and losing team stats
            winning_team_stats = []
            losing_team_stats = []

            # Flag to indicate whether we are currently parsing total stats
            parsing_winning_stats = False
            parsing_losing_stats = False

            # Loop through the lines and extract total stats for winning and losing teams
            for line in lines:
                if "Total Stats for Winning Team:" in line:
                    parsing_winning_stats = True
                    parsing_losing_stats = False
                    continue
                elif "Total Stats for Losing Team:" in line:
                    parsing_winning_stats = False
                    parsing_losing_stats = True
                    continue

                if parsing_winning_stats:
                    parts = line.strip().split(": ")
                    if len(parts) == 2:
                        stat_name = parts[0]
                        stat_value = parts[1]
                        winning_team_stats.append(float(stat_value))

                if parsing_losing_stats:
                    parts = line.strip().split(": ")
                    if len(parts) == 2:
                        stat_name = parts[0]
                        stat_value = parts[1]
                        losing_team_stats.append(float(stat_value))

            # Calculate the standard deviations for winning and losing teams
            winning_team_std_dev = math.sqrt(sum((x - overall_avg_initial) ** 2 for x in winning_team_stats) / len(winning_team_stats))
            losing_team_std_dev = math.sqrt(sum((x - overall_avg_initial) ** 2 for x in losing_team_stats) / len(losing_team_stats))

            # Calculate the difference in standard deviations (Winning - Losing)
            std_dev_difference = winning_team_std_dev - losing_team_std_dev

            # Append the difference to the list
            std_dev_differences.append(std_dev_difference)

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

            # Update the counts for each rating bracket based on std_dev_difference
            if std_dev_difference > 0:
                rating_bracket_counts[bracket]["above_zero"] += 1
            elif std_dev_difference < 0:
                rating_bracket_counts[bracket]["below_zero"] += 1

# Print counts of points above and below 0 for each rating bracket
for bracket, counts in rating_bracket_counts.items():
    print(f"Rating Bracket: {bracket}")
    print("Frequency of Differences in Standard Deviations of Stats (Winner - Loser) greater than 0:", counts["above_zero"])
    print("Frequency of Differences in Standard Deviations of Stats (Winner - Loser) less than 0:", counts["below_zero"])
    print()

# Create a scatter plot using Plotly
fig = go.Figure(data=[go.Scatter(x=rating_estimates, y=std_dev_differences, mode='markers')])
fig.update_layout(
    xaxis_title="Rating Estimate",
    yaxis_title="Difference in Stat Standard Deviations (Winner - Loser)",
    title="Rating Estimate vs. Difference in Stat Standard Deviations (Winner - Loser)",
)

# Enable scroll zoom
config = {'scrollZoom': True}
fig.show(config=config)
