import re
import json
import os
import shutil

# Define the source directory and filtered directory
source_directory = "gen9ou-matchjsons"
filtered_directory = "filteredgen9ou-matchjsons"

# Loop through all JSON files in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith(".json"):
        # Load JSON data from file
        with open(os.path.join(source_directory, filename), "r") as json_file:
            json_data = json.load(json_file)

        # Extract team sizes
        team_size_p1 = int(re.search(r"teamsize\|p1\|(\d+)", json_data['log']).group(1))
        team_size_p2 = int(re.search(r"teamsize\|p2\|(\d+)", json_data['log']).group(1))

        # Extract the winning and losing teams
        result = re.search(r"win\|(.+?)\n\|raw\|(.+?)'s rating:", json_data['log'])
        if result:
            winning_team = result.group(1)
            losing_team = "p1" if winning_team == "p2" else "p2"

            # Initialize variables
            num_turns = 0
            num_faints = 0

            # Process each line in the log
            log_lines = json_data["log"].split("\n")
            for line in log_lines:
                if line.startswith("|turn|"):
                    num_turns += 1
                elif "|faint|{}a:".format(losing_team) in line:
                    num_faints += 1

            # Check conditions for moving the file
            if team_size_p1 == 6 and team_size_p2 == 6 and (num_faints >= 3 or num_turns >= 10):
                # Move the file to the filtered directory
                shutil.move(os.path.join(source_directory, filename), os.path.join(filtered_directory, filename))
                print(f"Moved '{filename}' to the filtered directory.")
            else:
                print(f"Skipped '{filename}' due to conditions not being met.")
