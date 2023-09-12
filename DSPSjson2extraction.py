import re
import json
import os
import contextlib
import io
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Define the input folder containing the JSON files
input_folder = "filteredgen9ou-matchjsons"

# Create the output folder if it doesn't exist
output_folder = "gen9ou-stat_summary"
os.makedirs(output_folder, exist_ok=True)

# Iterate through all JSON files in the input folder
for input_filename in os.listdir(input_folder):
    if input_filename.endswith(".json"):
        unique_number = re.match(r"gen9ou-(\d+)\.json", input_filename)
        if unique_number:
            unique_number = unique_number.group(1)
            output_filename = f"{output_folder}/stat_summary_gen9ou-{unique_number}.txt"

            # Create a StringIO buffer to capture the output
            output_buffer = io.StringIO()

            # Redirect standard output to the buffer using contextlib
            with contextlib.redirect_stdout(output_buffer):

                def clean_pokemon_name(name):
                    return re.sub(r'[MF]$', '', name).strip().strip(',')

                def convert_to_lowercase(move_list):
                    return [move.lower() for move in move_list]

                # Define the fuzzy match threshold (adjust as needed)
                FUZZY_MATCH_THRESHOLD = 50


                def fuzzy_match_name(name, pokedex_data):
                    title_case_name = name.title()
                    if title_case_name in pokedex_data:
                        return title_case_name

                    matched_name, _ = process.extractOne(name, pokedex_data.keys())
                    if matched_name and fuzz.ratio(name, matched_name) >= FUZZY_MATCH_THRESHOLD:
                        return matched_name.title()  # Convert the matched name to title case

                    return None

                with open(os.path.join(input_folder, input_filename), "r") as json_file:
                    json_data = json.load(json_file)
                # Load pokedex data from the pokedex.json file
                with open("pokedex.json", "r") as pokedex_file:
                    pokedex_data = json.load(pokedex_file)


                # Extract team sizes
                team_size_p1 = int(re.search(r"teamsize\|p1\|(\d+)", json_data['log']).group(1))
                team_size_p2 = int(re.search(r"teamsize\|p2\|(\d+)", json_data['log']).group(1))


                # Extract player names from the beginning of the log
                p1_name = json_data['p1']
                p2_name = json_data['p2']

                # Extract player ratings using regular expressions
                rating_pattern = re.compile(r"'s rating: (\d+) &rarr; <strong>(\d+)")
                ratings_matches = rating_pattern.findall(json_data['log'])

                if len(ratings_matches) == 2:
                    p1_initial_rating, p1_final_rating = map(int, ratings_matches[0])
                    p2_initial_rating, p2_final_rating = map(int, ratings_matches[1])
                else:
                    print("Error: Could not find both players' ratings.")

                # Print player ratings
                print(f"{p1_name}'s initial rating: {p1_initial_rating}, final rating: {p1_final_rating}")
                print(f"{p2_name}'s initial rating: {p2_initial_rating}, final rating: {p2_final_rating}")
                print("\n")

                # Extract the winner's name from the log
                result = re.search(r"win\|(.+?)\n\|raw\|(.+?)'s rating:", json_data['log'])
                if result:
                    winner_name = result.group(1)

                    if winner_name == p1_name:
                        winning_player = "p1"
                        losing_player = "p2"
                    elif winner_name == p2_name:
                        winning_player = "p2"
                        losing_player = "p1"
                    else:
                        print("Error: Winner's name not recognized.")

                    winning_team = winning_player
                    losing_team = losing_player


                    # Extract Pokémon names from the log and clean them up
                    p1_pokemon = re.findall(r"\|poke\|p1\|([^|]+?)\|", json_data['log'])
                    p2_pokemon = re.findall(r"\|poke\|p2\|([^|]+?)\|", json_data['log'])

                    # Clean up Pokémon names
                    p1_pokemon = [clean_pokemon_name(name) for name in p1_pokemon]
                    p2_pokemon = [clean_pokemon_name(name) for name in p2_pokemon]
                    
                    # Correct Pokémon names in the winning team
                    corrected_winning_team_pokemon = []
                    for name in p1_pokemon:
                        cleaned_name = clean_pokemon_name(name)
                        
                        if any(entry["name"] == cleaned_name for entry in pokedex_data.values()):
                            corrected_winning_team_pokemon.append(cleaned_name)
                        else:
                            corrected_name = fuzzy_match_name(cleaned_name, pokedex_data)
                            if corrected_name and corrected_name != cleaned_name:  # Only append if corrected name is different
                                corrected_winning_team_pokemon.append(corrected_name)
                            else:
                                corrected_winning_team_pokemon.append(cleaned_name)

                    # Correct Pokémon names in the losing team
                    corrected_losing_team_pokemon = []
                    for name in p2_pokemon:
                        cleaned_name = clean_pokemon_name(name)
                        
                        if any(entry["name"] == cleaned_name for entry in pokedex_data.values()):
                            corrected_losing_team_pokemon.append(cleaned_name)
                        else:
                            corrected_name = fuzzy_match_name(cleaned_name, pokedex_data)
                            if corrected_name and corrected_name != cleaned_name:  # Only append if corrected name is different
                                corrected_losing_team_pokemon.append(corrected_name)
                            else:
                                corrected_losing_team_pokemon.append(cleaned_name)

                    # Join corrected Pokémon names with commas
                    corrected_winning_pokemon_str = ", ".join(corrected_winning_team_pokemon[:team_size_p1])
                    corrected_losing_pokemon_str = ", ".join(corrected_losing_team_pokemon[:team_size_p2])

                    # Print corrected Pokémon names for the winning and losing teams
                    print("Winning Team:", corrected_winning_pokemon_str if winning_team == "p1" else corrected_losing_pokemon_str)
                    print("Losing Team:", corrected_losing_pokemon_str if winning_team == "p1" else corrected_winning_pokemon_str)
                    print("\n")

                    # Extract and store moves for each player
                    p1_moves = set()
                    p2_moves = set()
                    current_player = None
                    for line in json_data['log'].split('\n'):
                        if '|move|p1' in line:
                            current_player = 'p1'
                            move = line.split('|')[-2]
                            if ':' not in move and move.strip():  # Exclude moves with player names and empty/whitespace-only moves
                                p1_moves.add(move)
                        elif '|move|p2' in line:
                            current_player = 'p2'
                            move = line.split('|')[-2]
                            if ':' not in move and move.strip():  # Exclude moves with player names and empty/whitespace-only moves
                                p2_moves.add(move)
                            
                    # Print moves for each player
                    p1_moves_str = "p1 (Winner) moves: " if winning_team == "p1" else "p1 (Loser) moves: "
                    p2_moves_str = "p2 (Winner) moves: " if winning_team == "p2" else "p2 (Loser) moves: "
                    print(p1_moves_str, ", ".join(p1_moves))
                    print(p2_moves_str, ", ".join(p2_moves))


                # Define move categories as lists
                entry_hazard_moves = ["Stealth Rock", "Spikes", "Toxic Spikes", 
                                    "Sticky Web", "Stone Axe"]  
                entry_hazard_clear_moves = ["Rapid Spin", "Defog", "Mortal Spin", "Tidy Up"]

                priority_moves = ["Accelerock", "Ally Switch", "Aqua Jet", "Baby-Doll Eyes",
                                "Bide", "Bullet Punch", "Ice Shard", "Ion Deluge", "Jet Punch",
                                "Mach Punch", "Powder", "Quick Attack", "Shadow Sneak", "Sucker Punch",
                                "Vacuum Wave", "Water Shuriken", "Ally Switch", "Extremespeed",
                                "Feint", "First Impression", "Follow Me", "Rage Powder", "Quick Guard",
                                "Spotlight", "Wide Guard", "Baneful Bunker", "Detect", "Endure",
                                "King's Shield", "Magic Coat", "Max Guard", "Obstruct", "Protect",
                                "Silk Trap", "Snatch", "Spiky Shield", "Helping Hand"]

                runswitch_moves = ["Volt Switch", "U-turn", "Parting Shot"]

                status_moves = ["Thunder Wave", "Toxic", "Will-O-Wisp", "Spore", "Sleep Powder",
                                "Glare", "Nuzzle", "Stun Spore", "Poison Gas", "Poisonpowder",
                                "Toxic Thread", "Dark Void", "Grasswhistle", "Hypnosis",
                                "Lovely Kiss", "Yawn", "Attract", "Chatter", "Confuse Ray",
                                "Dynamicpunch", "Flatter", "Swagger", "Sweet Kiss",
                                "Supersonic", "Teeter Dance"]

                # Clean moves for each player
                cleaned_p1_moves = [clean_pokemon_name(move.lower()) for move in p1_moves]
                cleaned_p2_moves = [clean_pokemon_name(move.lower()) for move in p2_moves]

                lowercase_entry_hazard_moves = convert_to_lowercase(entry_hazard_moves)
                lowercase_entry_hazard_clear_moves = convert_to_lowercase(entry_hazard_clear_moves)
                lowercase_priority_moves = convert_to_lowercase(priority_moves)
                lowercase_runswitch_moves = convert_to_lowercase(runswitch_moves)
                lowercase_status_moves = convert_to_lowercase(status_moves)

                # Initialize move category counters
                p1_entry_hazard_count = 0
                p2_entry_hazard_count = 0
                p1_entry_hazard_clear_count = 0
                p2_entry_hazard_clear_count = 0
                p1_priority_count = 0
                p2_priority_count = 0
                p1_runswitch_count = 0
                p2_runswitch_count = 0
                p1_status_count = 0
                p2_status_count = 0

                # Iterate through the moves used by each player and count move categories
                for move in cleaned_p1_moves:
                    if move in lowercase_entry_hazard_moves:
                        p1_entry_hazard_count += 1
                    if move in lowercase_entry_hazard_clear_moves:
                        p1_entry_hazard_clear_count += 1
                    if move in lowercase_priority_moves:
                        p1_priority_count += 1
                    if move in lowercase_runswitch_moves:
                        p1_runswitch_count += 1
                    if move in lowercase_status_moves:
                        p1_status_count += 1

                for move in cleaned_p2_moves:
                    if move in lowercase_entry_hazard_moves:
                        p2_entry_hazard_count += 1
                    if move in lowercase_entry_hazard_clear_moves:
                        p2_entry_hazard_clear_count += 1
                    if move in lowercase_priority_moves:
                        p2_priority_count += 1
                    if move in lowercase_runswitch_moves:
                        p2_runswitch_count += 1
                    if move in lowercase_status_moves:
                        p2_status_count += 1


                # Print move category counts for each player
                print("\n")
                if winning_team == "p1":
                    winning_player_indicator = "p1 (Winner)"
                    losing_player_indicator = "p2 (Loser)"
                else:
                    winning_player_indicator = "p2 (Winner)"
                    losing_player_indicator = "p1 (Loser)"

                print(f"{winning_player_indicator} Move Category Counts:")
                print("Entry Hazard Moves:", p1_entry_hazard_count)
                print("Entry Hazard Clear Moves:", p1_entry_hazard_clear_count)
                print("Priority Moves:", p1_priority_count)
                print("Runswitch Moves:", p1_runswitch_count)
                print("Status Moves:", p1_status_count)

                print("\n")

                print(f"{losing_player_indicator} Move Category Counts:")
                print("Entry Hazard Moves:", p2_entry_hazard_count)
                print("Entry Hazard Clear Moves:", p2_entry_hazard_clear_count)
                print("Priority Moves:", p2_priority_count)
                print("Runswitch Moves:", p2_runswitch_count)
                print("Status Moves:", p2_status_count)


                # print("\n")
                # print(cleaned_p1_moves)
                # print(cleaned_p2_moves)

                # print(lowercase_entry_hazard_moves)
                # print(lowercase_entry_hazard_clear_moves)
                # print(lowercase_priority_moves)
                # print(lowercase_runswitch_moves)
                # print(lowercase_status_moves)

                # Load pokedex data from the pokedex.json file
                with open("pokedex.json", "r") as pokedex_file:
                    pokedex_data = json.load(pokedex_file)



                # Function to get a Pokémon's types from the pokedex data
                def get_pokemon_types(pokemon_name):
                    for num, info in pokedex_data.items():
                        if info["name"] == pokemon_name:
                            return info["types"]
                    return []

                # Iterate through the Pokémon on the winning team
                winning_team_pokemon = p1_pokemon if winning_team == "p1" else p2_pokemon
                winning_team_pokemon_types = []
                for pokemon_name in winning_team_pokemon:
                    cleaned_name = clean_pokemon_name(pokemon_name)
                    matching_pokedex_entry = next((entry for entry in pokedex_data.values() if entry["name"] == cleaned_name), None)
                    if matching_pokedex_entry:
                        types = matching_pokedex_entry["types"]
                        winning_team_pokemon_types.append(f"{cleaned_name}: {', '.join(types) if types else 'No type information'}")
                    else:
                        corrected_name = fuzzy_match_name(cleaned_name, pokedex_data)
                        types = get_pokemon_types(corrected_name) if corrected_name else None
                        winning_team_pokemon_types.append(f"{corrected_name if corrected_name else cleaned_name}: {', '.join(types) if types else 'No type information'}")

                # Print Pokémon types for winning team
                print("\nPokémon Types for Winning Team:")
                for entry in winning_team_pokemon_types:
                    print(entry)


                # Iterate through the Pokémon on the losing team
                losing_team_pokemon = p2_pokemon if winning_team == "p1" else p1_pokemon
                losing_team_pokemon_types = []
                for pokemon_name in losing_team_pokemon:
                    cleaned_name = clean_pokemon_name(pokemon_name)
                    matching_pokedex_entry = next((entry for entry in pokedex_data.values() if entry["name"] == cleaned_name), None)
                    if matching_pokedex_entry:
                        types = matching_pokedex_entry["types"]
                        losing_team_pokemon_types.append(f"{cleaned_name}: {', '.join(types) if types else 'No type information'}")
                    else:
                        corrected_name = fuzzy_match_name(cleaned_name, pokedex_data)
                        types = get_pokemon_types(corrected_name) if corrected_name else None
                        losing_team_pokemon_types.append(f"{corrected_name if corrected_name else cleaned_name}: {', '.join(types) if types else 'No type information'}")

                # Print Pokémon types for losing team
                print("\nPokémon Types for Losing Team:")
                for entry in losing_team_pokemon_types:
                    print(entry)



                # Load BattleTypeChart data from typechart.json file
                with open("typechart.json", "r") as typechart_file:
                    typechart_data = json.load(typechart_file)

                def calculate_effectiveness(attacking_type, defending_types):
                    total_effectiveness = 1.0  # Initialize total effectiveness as neutral (1.0)
                    for defending_type in defending_types:
                        defending_type_lower = defending_type.lower()
                        attacking_type_lower = attacking_type.lower()
                        
                        damage_taken_data = typechart_data.get(defending_type_lower, {}).get("damageTaken", {})
                        
                        # Convert attacking_type to title case before using as a key
                        attacking_type_title = attacking_type.title()
                        damage_value = damage_taken_data.get(attacking_type_title, 0)  # Use 0 as default value
                        
                        if damage_value == 1:
                            total_effectiveness *= 2.0  # Double the effectiveness for super effective
                        elif damage_value == 2:
                            total_effectiveness *= 0.5  # Half the effectiveness for resisted
                        
                        # If either type is immune, the total effectiveness becomes 0
                        if damage_value == 3:
                            total_effectiveness = 0.0
                            break
                    
                    return total_effectiveness

                # Create dictionaries to store resisting counts for each team
                winning_team_resisting_counts = {type_name: 0 for type_name in typechart_data}
                losing_team_resisting_counts = {type_name: 0 for type_name in typechart_data}
                winning_team_weakness_counts = {type_name: 0 for type_name in typechart_data}
                losing_team_weakness_counts = {type_name: 0 for type_name in typechart_data}

                # Iterate through each attacking type
                for attacking_type in typechart_data:
                    attacking_type_lower = attacking_type.lower()  # Convert attacking_type to lowercase
                    
                    # Iterate through each Pokémon on the winning team
                    for winning_pokemon in winning_team_pokemon:
                        defending_types = get_pokemon_types(winning_pokemon)
                        effectiveness = calculate_effectiveness(attacking_type_lower, defending_types)
                        if effectiveness <= 0.5:  # Resistance or immunity
                            winning_team_resisting_counts[attacking_type] += 1

                    # Iterate through each Pokémon on the losing team
                    for losing_pokemon in losing_team_pokemon:
                        defending_types = get_pokemon_types(losing_pokemon)
                        effectiveness = calculate_effectiveness(attacking_type_lower, defending_types)
                        if effectiveness <= 0.5:  # Resistance or immunity
                            losing_team_resisting_counts[attacking_type] += 1
                for attacking_type in typechart_data:
                    attacking_type_lower = attacking_type.lower()

                    for winning_pokemon in winning_team_pokemon:
                        defending_types = get_pokemon_types(winning_pokemon)
                        effectiveness = calculate_effectiveness(attacking_type_lower, defending_types)
                        if effectiveness >= 2:  # Weakness
                            winning_team_weakness_counts[attacking_type] += 1

                    for losing_pokemon in losing_team_pokemon:
                        defending_types = get_pokemon_types(losing_pokemon)
                        effectiveness = calculate_effectiveness(attacking_type_lower, defending_types)
                        if effectiveness >= 2:  # Weakness
                            losing_team_weakness_counts[attacking_type] += 1    

                # Print resisting counts for the winning and losing teams in the desired format
                print("\n")

                print("Winning Team Resisting Counts (Dictionary):")
                for type_name, count in winning_team_resisting_counts.items():
                    print(f"{type_name}: {count}")

                print("\nLosing Team Resisting Counts (Dictionary):")
                for type_name, count in losing_team_resisting_counts.items():
                    print(f"{type_name}: {count}")
                print("\nWinning Team Weakness Counts (Dictionary):")
                for type_name, count in winning_team_weakness_counts.items():
                    print(f"{type_name}: {count}")

                print("\nLosing Team Weakness Counts (Dictionary):")
                for type_name, count in losing_team_weakness_counts.items():
                    print(f"{type_name}: {count}")

                # Create and print resisting counts as a list of numbers in ascending order for both teams
                winning_resisting_counts_list = sorted(winning_team_resisting_counts.values())
                losing_resisting_counts_list = sorted(losing_team_resisting_counts.values())
                # Create lists of weakness counts in descending order
                winning_weakness_counts_list = sorted(winning_team_weakness_counts.values(), reverse=True)
                losing_weakness_counts_list = sorted(losing_team_weakness_counts.values(), reverse=True)



                print("\nWinning Team Resisting Counts (List):")
                print(winning_resisting_counts_list)

                print("\nLosing Team Resisting Counts (List):")
                print(losing_resisting_counts_list)

                print("\nWinning Team Weakness Counts (List):")
                print(winning_weakness_counts_list)

                print("\nLosing Team Weakness Counts (List):")
                print(losing_weakness_counts_list)

                # Calculate total stats for winning and losing teams
                winning_team_total_stats = {category: 0 for category in ["hp", "atk", "def", "spa", "spd", "spe"]}
                losing_team_total_stats = {category: 0 for category in ["hp", "atk", "def", "spa", "spd", "spe"]}

                # Define a function to get base stats from pokedex data
                def get_base_stats(pokemon_name, category):
                    for num, info in pokedex_data.items():
                        if info["name"] == pokemon_name:
                            if "baseStats" in info and category in info["baseStats"]:
                                return info["baseStats"][category]
                            else:
                                return 0
                    return 0


                # Iterate through the Pokémon on the winning team
                for pokemon_name in p1_pokemon if winning_team == "p1" else p2_pokemon:
                    for category in winning_team_total_stats:
                        winning_team_total_stats[category] += get_base_stats(pokemon_name, category)

                # Iterate through the Pokémon on the losing team
                for pokemon_name in p2_pokemon if winning_team == "p1" else p1_pokemon:
                    for category in losing_team_total_stats:
                        losing_team_total_stats[category] += get_base_stats(pokemon_name, category)

                # Print total stats for winning and losing teams
                print("\nTotal Stats for Winning Team:")
                for category, value in winning_team_total_stats.items():
                    print(f"{category.capitalize()}: {value}")

                print("\nTotal Stats for Losing Team:")
                for category, value in losing_team_total_stats.items():
                    print(f"{category.capitalize()}: {value}")

            # Get the captured output from the buffer
            captured_output = output_buffer.getvalue()

            # Open the output text file for writing
            with open(output_filename, "w") as output_file:
                output_file.write(captured_output)

            print(f"Summary for {input_filename} written to: {output_filename}")
        else:
            print(f"Error: Input filename {input_filename} doesn't match the expected format.")
