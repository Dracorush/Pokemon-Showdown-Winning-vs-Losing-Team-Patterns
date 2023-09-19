from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import requests
import os

# Set up the Selenium webdriver (replace with appropriate driver executable path)
driver = webdriver.Chrome()

# Specify the URL with the desired format filter (Gen 9 OU)
url = "https://replay.pokemonshowdown.com/search/?format=gen9ou"

# Load the initial URL
driver.get(url)

# Locate and click the "Show More" button
while True:
    try:
        # Wait for the "More" button to be clickable
        more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'More')]"))
        )
        
        # Click the "More" button
        more_button.click()
        
        # Wait for the content to load
        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading")))
    except:
        break  # Break the loop when there are no more battles to load

# Extract the HTML content after loading all battles
html_content = driver.page_source

# Close the Selenium webdriver
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all anchor tags (a) that have the href attribute
anchor_tags = soup.find_all("a", href=True)

# Extract the unique number corresponding to each battle room from the href
battle_numbers = []
for anchor_tag in anchor_tags:
    href = anchor_tag["href"]
    # Assuming the unique number is always the last part of the href
    unique_number = href.split("/")[-1]
    battle_numbers.append(unique_number)

# Specify the directory name
directory_name = "gen9ou-matchjsons"

# Create the directory if it doesn't exist
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

# Print the extracted battle numbers
for number in battle_numbers:
    try:
        url = "https://replay.pokemonshowdown.com/" + number + ".json"
        r = requests.get(url)
        filename = os.path.join(directory_name, number + ".json")
        with open(filename, 'w') as f:
            json.dump(r.json(), f)
    except Exception as e:
        os.remove(filename)
        
        
        # print("Error occurred:", str(e))
        # print(r.status_code)
        # print(number)
        # print("\n")

