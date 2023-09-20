import os
import plotly.graph_objects as go
import plotly.offline as pyo


# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize dictionaries to store counts of players on the winning and losing teams
winning_counts = {}
losing_counts = {}

# Iterate over the file names
for file_name in os.listdir(directory):
    if file_name.startswith("stat_summary_gen9ou-") and file_name.endswith(".txt"):
        # Construct the full file path
        file_path = os.path.join(directory, file_name)

        # Read the contents of the single text file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Initialize variables to track whether we are in the Winner or Loser sections
        is_winner_section = False
        is_loser_section = False

        # Initialize variables to store move counts for Winner and Loser
        winner_status_moves = 0
        loser_status_moves = 0

        # Read the contents of the single text file
        for line in lines:
            if "p2 (Winner) Move Category Counts:" in line:
                is_winner_section = True
                is_loser_section = False
            elif "p1 (Loser) Move Category Counts:" in line:
                is_winner_section = False
                is_loser_section = True
            elif line.strip() == "":
                is_winner_section = False
                is_loser_section = False
            elif is_winner_section and "Status Moves:" in line:
                winner_status_moves = int(line.split(":")[1].strip())
            elif is_loser_section and "Status Moves:" in line:
                loser_status_moves = int(line.split(":")[1].strip())
        
        # Update the counts in the dictionaries
        if winner_status_moves not in winning_counts:
            winning_counts[winner_status_moves] = 0
        winning_counts[winner_status_moves] += 1
        
        if loser_status_moves not in losing_counts:
            losing_counts[loser_status_moves] = 0
        losing_counts[loser_status_moves] += 1

# Create a bar chart using Plotly
moves = sorted(set(list(winning_counts.keys()) + list(losing_counts.keys())))

fig = go.Figure()

fig.add_trace(go.Bar(
    x=moves,
    y=[winning_counts.get(move, 0) for move in moves],
    name='Winning Team'
))

fig.add_trace(go.Bar(
    x=moves,
    y=[losing_counts.get(move, 0) for move in moves],
    name='Losing Team'
))

fig.update_layout(
    xaxis_title='Number of Status Moves',
    yaxis_title='Number of Players',
    title='Number of Players vs. Number of Status Moves',
    xaxis=dict(tickvals=moves, ticktext=moves),  # Set custom tick values and labels
)

# Enable scroll zoom
config = {'scrollZoom': True}

# Save the figure as an HTML file
html_file_name = "status_moves_chart.html"
pyo.plot(fig, filename=html_file_name, auto_open=False, config=config)

# Display the HTML file path
print(f"Chart saved as: {html_file_name}")


import os
import plotly.graph_objects as go

# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize dictionaries to store counts of players on the winning and losing teams
winning_counts = {}
losing_counts = {}

# Iterate over the file names
for file_name in os.listdir(directory):
    if file_name.startswith("stat_summary_gen9ou-") and file_name.endswith(".txt"):
        # Construct the full file path
        file_path = os.path.join(directory, file_name)

        # Read the contents of the single text file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Initialize variables to track whether we are in the Winner or Loser sections
        is_winner_section = False
        is_loser_section = False

        # Initialize variables to store move counts for Winner and Loser
        winner_runswitch_moves = 0
        loser_runswitch_moves = 0

        # Read the contents of the single text file
        for line in lines:
            if "p2 (Winner) Move Category Counts:" in line:
                is_winner_section = True
                is_loser_section = False
            elif "p1 (Loser) Move Category Counts:" in line:
                is_winner_section = False
                is_loser_section = True
            elif line.strip() == "":
                is_winner_section = False
                is_loser_section = False
            elif is_winner_section and "Runswitch Moves:" in line:
                winner_runswitch_moves = int(line.split(":")[1].strip())
            elif is_loser_section and "Runswitch Moves:" in line:
                loser_runswitch_moves = int(line.split(":")[1].strip())
        
        # Update the counts in the dictionaries
        if winner_runswitch_moves not in winning_counts:
            winning_counts[winner_runswitch_moves] = 0
        winning_counts[winner_runswitch_moves] += 1
        
        if loser_runswitch_moves not in losing_counts:
            losing_counts[loser_runswitch_moves] = 0
        losing_counts[loser_runswitch_moves] += 1

# Create a bar chart using Plotly
moves = sorted(set(list(winning_counts.keys()) + list(losing_counts.keys())))

fig = go.Figure()

fig.add_trace(go.Bar(
    x=moves,
    y=[winning_counts.get(move, 0) for move in moves],
    name='Winning Team'
))

fig.add_trace(go.Bar(
    x=moves,
    y=[losing_counts.get(move, 0) for move in moves],
    name='Losing Team'
))

fig.update_layout(
    xaxis_title='Number of Runswitch Moves',
    yaxis_title='Number of Players',
    title='Number of Players vs. Number of Runswitch Moves',
    xaxis=dict(tickvals=moves, ticktext=moves),  # Set custom tick values and labels
)

# Enable scroll zoom
config = {'scrollZoom': True}

# Save the figure as an HTML file
html_file_name = "runswitch_moves_chart.html"
pyo.plot(fig, filename=html_file_name, auto_open=False, config=config)

# Display the HTML file path
print(f"Chart saved as: {html_file_name}")

import os
import plotly.graph_objects as go

# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize dictionaries to store counts of players on the winning and losing teams
winning_counts = {}
losing_counts = {}

# Iterate over the file names
for file_name in os.listdir(directory):
    if file_name.startswith("stat_summary_gen9ou-") and file_name.endswith(".txt"):
        # Construct the full file path
        file_path = os.path.join(directory, file_name)

        # Read the contents of the single text file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Initialize variables to track whether we are in the Winner or Loser sections
        is_winner_section = False
        is_loser_section = False

        # Initialize variables to store move counts for Winner and Loser
        winner_priority_moves = 0
        loser_priority_moves = 0

        # Read the contents of the single text file
        for line in lines:
            if "p2 (Winner) Move Category Counts:" in line:
                is_winner_section = True
                is_loser_section = False
            elif "p1 (Loser) Move Category Counts:" in line:
                is_winner_section = False
                is_loser_section = True
            elif line.strip() == "":
                is_winner_section = False
                is_loser_section = False
            elif is_winner_section and "Priority Moves:" in line:
                winner_priority_moves = int(line.split(":")[1].strip())
            elif is_loser_section and "Priority Moves:" in line:
                loser_priority_moves = int(line.split(":")[1].strip())
        
        # Update the counts in the dictionaries
        if winner_priority_moves not in winning_counts:
            winning_counts[winner_priority_moves] = 0
        winning_counts[winner_priority_moves] += 1
        
        if loser_priority_moves not in losing_counts:
            losing_counts[loser_priority_moves] = 0
        losing_counts[loser_priority_moves] += 1

# Create a side-by-side bar chart using Plotly
moves = sorted(set(list(winning_counts.keys()) + list(losing_counts.keys())))

fig = go.Figure()

fig.add_trace(go.Bar(
    x=moves,
    y=[winning_counts.get(move, 0) for move in moves],
    name='Winning Team'
))

fig.add_trace(go.Bar(
    x=moves,
    y=[losing_counts.get(move, 0) for move in moves],
    name='Losing Team'
))

fig.update_layout(
    xaxis_title='Number of Priority Moves',
    yaxis_title='Number of Players',
    title='Number of Players vs. Number of Priority Moves',
    xaxis=dict(tickvals=moves, ticktext=moves),  # Set custom tick values and labels
)

# Enable scroll zoom
config = {'scrollZoom': True}

# Save the figure as an HTML file
html_file_name = "priority_moves_chart.html"
pyo.plot(fig, filename=html_file_name, auto_open=False, config=config)

# Display the HTML file path
print(f"Chart saved as: {html_file_name}")


import os
import plotly.graph_objects as go

# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize dictionaries to store counts for each move category
winning_counts = {}
losing_counts = {}

# Iterate over the file names
for file_name in os.listdir(directory):
    if file_name.startswith("stat_summary_gen9ou-") and file_name.endswith(".txt"):
        # Construct the full file path
        file_path = os.path.join(directory, file_name)

        # Read the contents of the single text file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Initialize variables to store move counts for Winner and Loser
        winner_entry_hazard_clear_moves = 0
        loser_entry_hazard_clear_moves = 0

        # Initialize flags to track whether we are in the Winner or Loser sections
        is_winner_section = False
        is_loser_section = False

        # Read the contents of the single text file
        for line in lines:
            if "p2 (Winner) Move Category Counts:" in line:
                is_winner_section = True
                is_loser_section = False
            elif "p1 (Loser) Move Category Counts:" in line:
                is_winner_section = False
                is_loser_section = True
            elif line.strip() == "":
                is_winner_section = False
                is_loser_section = False
            elif is_winner_section and "Entry Hazard Clear Moves:" in line:
                winner_entry_hazard_clear_moves = int(line.split(":")[1].strip())
            elif is_loser_section and "Entry Hazard Clear Moves:" in line:
                loser_entry_hazard_clear_moves = int(line.split(":")[1].strip())
        
        # Update the counts dictionaries based on the move counts
        if winner_entry_hazard_clear_moves in winning_counts:
            winning_counts[winner_entry_hazard_clear_moves] += 1
        else:
            winning_counts[winner_entry_hazard_clear_moves] = 1
        
        if loser_entry_hazard_clear_moves in losing_counts:
            losing_counts[loser_entry_hazard_clear_moves] += 1
        else:
            losing_counts[loser_entry_hazard_clear_moves] = 1

# Create lists to store unique move counts and corresponding counts for each team
moves = list(set(winning_counts.keys()) | set(losing_counts.keys()))

winning_team_counts = [winning_counts.get(move, 0) for move in moves]
losing_team_counts = [losing_counts.get(move, 0) for move in moves]

# Create the side-by-side bar graph using Plotly
fig = go.Figure()

fig.add_trace(go.Bar(
    x=moves,
    y=winning_team_counts,
    name="Winning Team",
    offsetgroup=0,  # Ensure bars are aligned side by side
))

fig.add_trace(go.Bar(
    x=moves,
    y=losing_team_counts,
    name="Losing Team",
    offsetgroup=1,  # Ensure bars are aligned side by side
))

fig.update_layout(
    xaxis_title="Number of Entry Hazard Clear Moves",
    yaxis_title="Number of Players",
    title="Number of Players vs. Number of Entry Hazard Clear Moves",
    barmode="group",  # Display bars in a grouped manner (side by side)
)

# Enable scroll zoom
config = {'scrollZoom': True}

# Save the figure as an HTML file
html_file_name = "entry_hazard_clear_moves_chart.html"
pyo.plot(fig, filename=html_file_name, auto_open=False, config=config)

# Display the HTML file path
print(f"Chart saved as: {html_file_name}")

import os
import plotly.graph_objects as go

# Directory containing the text files
directory = "gen9ou-stat_summary"

# Initialize dictionaries to store counts for each move category
winning_counts = {}
losing_counts = {}

# Iterate over the file names
for file_name in os.listdir(directory):
    if file_name.startswith("stat_summary_gen9ou-") and file_name.endswith(".txt"):
        # Construct the full file path
        file_path = os.path.join(directory, file_name)

        # Read the contents of the single text file
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Initialize variables to store move counts for Winner and Loser
        winner_entry_hazard_moves = 0
        loser_entry_hazard_moves = 0

        # Initialize flags to track whether we are in the Winner or Loser sections
        is_winner_section = False
        is_loser_section = False

        # Read the contents of the single text file
        for line in lines:
            if "p2 (Winner) Move Category Counts:" in line:
                is_winner_section = True
                is_loser_section = False
            elif "p1 (Loser) Move Category Counts:" in line:
                is_winner_section = False
                is_loser_section = True
            elif line.strip() == "":
                is_winner_section = False
                is_loser_section = False
            elif is_winner_section and "Entry Hazard Moves:" in line:
                winner_entry_hazard_moves = int(line.split(":")[1].strip())
            elif is_loser_section and "Entry Hazard Moves:" in line:
                loser_entry_hazard_moves = int(line.split(":")[1].strip())
        
        # Update the counts dictionaries based on the move counts
        if winner_entry_hazard_moves in winning_counts:
            winning_counts[winner_entry_hazard_moves] += 1
        else:
            winning_counts[winner_entry_hazard_moves] = 1
        
        if loser_entry_hazard_moves in losing_counts:
            losing_counts[loser_entry_hazard_moves] += 1
        else:
            losing_counts[loser_entry_hazard_moves] = 1

# Create lists to store unique move counts and corresponding counts for each team
moves = list(set(winning_counts.keys()) | set(losing_counts.keys()))

winning_team_counts = [winning_counts.get(move, 0) for move in moves]
losing_team_counts = [losing_counts.get(move, 0) for move in moves]

# Create the side-by-side bar graph using Plotly
fig = go.Figure()

fig.add_trace(go.Bar(
    x=moves,
    y=winning_team_counts,
    name="Winning Team",
    offsetgroup=0,  # Ensure bars are aligned side by side
))

fig.add_trace(go.Bar(
    x=moves,
    y=losing_team_counts,
    name="Losing Team",
    offsetgroup=1,  # Ensure bars are aligned side by side
))

fig.update_layout(
    xaxis_title="Number of Entry Hazard Moves",
    yaxis_title="Number of Players",
    title="Number of Players vs. Number of Entry Hazard Moves",
    barmode="group",  # Display bars in a grouped manner (side by side)
)

# Enable scroll zoom
config = {'scrollZoom': True}

# Save the figure as an HTML file
html_file_name = "entry_hazard_moves_chart.html"
pyo.plot(fig, filename=html_file_name, auto_open=False, config=config)

# Display the HTML file path
print(f"Chart saved as: {html_file_name}")
