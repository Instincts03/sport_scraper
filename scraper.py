from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException
import csv
import os
import json
import time
from pytz import timezone
from datetime import datetime

class Info:
    def scrape_team_names(driver):
        team_names = []

        try:
            teams_list = driver.find_element(By.CLASS_NAME, "teams_name")
            list_items = teams_list.find_elements(By.TAG_NAME, "li")
            for item in list_items:
                anchor_tag = item.find_element(By.TAG_NAME, "a")
                strong_tag = anchor_tag.find_element(By.TAG_NAME, "strong")
                team_name = strong_tag.text.strip()
                team_names.append(team_name)

        except Exception as e:
            print(f"An error occurred: {e}")

        return team_names
    
    
    def matches_links(driver, switch):
        try:
            os.makedirs('temp', exist_ok=True)

            matches_list = driver.find_elements(By.XPATH, "//ul[@class='matches_list']/li/a[@class='clickable']")
            matches_links = [match.get_attribute('href') for match in matches_list]

            if switch == 'completed':
                matches_links = matches_links[::-1]

            if matches_links:
                with open('matches_link.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows([link] for link in matches_links)

            if switch == 'live':
                csv_file = os.path.join('temp', 'live_match_link.csv')
            elif switch == 'completed':
                csv_file = os.path.join('temp', 'completed_match_link.csv')
            else:
                csv_file = os.path.join('temp', 'upcoming_match_link.csv')

            if csv_file and matches_links:
                with open(csv_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows([link] for link in matches_links)
            
        except Exception as e:
            print(f"An error occurred while scraping matches: {e}")
                    
    
    
    #schedule

    def schedule(driver, switch):
        try:
            # Read match links from the CSV file
            with open(f'temp/{switch}_match_link.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                matches_links = [row[0] for row in reader]
        except:
            #print(f"no {switch} matches found")
            return
            

        # Modify links to include '/info/switch'
        modified_links = [link + f'/info/{switch}' for link in matches_links]

        # Iterate through each modified link and open it
        for link in modified_links:
            driver.get(link)
            time.sleep(2)

            # Locate match details using the new HTML structure
            match_details = driver.find_elements(By.CSS_SELECTOR, ".table_row")
            #print(f"Match details found: {len(match_details)}")

            if match_details:
                # Conditional logic for different switches
                i=0
                try:
                    # Extract match information from the second t_col tag in each row
                    t_col = match_details[i].find_elements(By.CSS_SELECTOR, ".t_col")[1].text.strip()

                    # Conditional handling based on the switch
                    if switch in ['completed', 'live']:
                        # Extract match name, date, time, and venue for 'completed' or 'live'
                        match_info = t_col.split(',')
                        match = match_info[0].strip()  # Match name
                        match_number = match_info[1].strip() if len(match_info) > 1 else "N/A"  # Match number (if available)

                        # Extract date, time, and venue based on the switch
                        date_text = match_details[i + 2].find_elements(By.CSS_SELECTOR, ".t_col")[1].text.strip()
                        time_text = match_details[i + 3].find_elements(By.CSS_SELECTOR, ".t_col")[1].text.strip()
                        venue = match_details[i + 5].find_elements(By.CSS_SELECTOR, ".t_col")[1].text.strip()

                    elif switch == 'upcoming':
                        # Extract match name, date, time, and venue for 'upcoming'
                        match_info = t_col.split(',')
                        match = match_info[0].strip()  # Match name
                        match_number = match_info[1].strip() if len(match_info) > 1 else "N/A"  # Match number (if available)

                        # Extract date, time, and venue based on the switch
                        date_text = match_details[i + 2].find_elements(By.CSS_SELECTOR, ".t_col")[1].text.strip()
                        time_text = match_details[i + 3].find_elements(By.CSS_SELECTOR, ".t_col")[1].text.strip()
                        venue = match_details[i + 4].find_elements(By.CSS_SELECTOR, ".t_col")[1].text.strip()

                    # Extract day
                    day = date_text.split(',')[0].strip()

                    # Combine date and time for UTC conversion
                    local_datetime = datetime.strptime(f"{date_text} {time_text}", "%A, %b-%d, %Y %I:%M %p")
                    ist_tz = timezone("Asia/Kolkata")  # IST timezone
                    local_datetime = ist_tz.localize(local_datetime)
                    utc_datetime = local_datetime.astimezone(timezone("UTC"))
                    
                    file_exists = os.path.isfile('schedule.csv')

                    # Append match details to CSV
                    with open('schedule.csv', 'a', newline='') as csvfile:
                        fieldnames = ['Match', 'Match Number', 'Day', 'Date (UTC)', 'Time (UTC)', 'Venue']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        
                        if not file_exists:
                            writer.writeheader()

                        # Write match details
                        writer.writerow({
                            'Match': match,
                            'Match Number': match_number,
                            'Day': day,
                            'Date (UTC)': utc_datetime.strftime("%Y-%m-%d"),
                            'Time (UTC)': utc_datetime.strftime("%H:%M"),
                            'Venue': venue
                        })
                except Exception as e:
                    print(f"Error processing match details at index {i}: {e}")
            else:
                print(f"No match details available in the {switch} section.")
    


            
    
    def scrape_players_for_team(driver, team):
        try:
            player_elements = driver.find_elements(By.XPATH, "//ul[@class='squad_list']/li")
            team_data = []
            for player in player_elements:
                player_name = player.find_element(By.XPATH, ".//strong").text
                designation = player.find_element(By.XPATH, ".//small").text
                team_data.append((player_name, designation))
            return team_data
        except Exception as e:
            print(f"Error scraping team {team}: {e}")
            return []
        
        
        
        
    def extract_ball_by_ball(driver, switch):
        try:
            csv_file = os.path.join('temp', 'live_match_link.csv') if switch == 'live' else os.path.join('temp', 'completed_match_link.csv')
            output_folder = os.path.join('ball_by_ball')

            if not os.path.exists(csv_file):
                print(f"CSV file not found: {csv_file}")
                return

            os.makedirs(output_folder, exist_ok=True)

            with open(csv_file, 'r') as file:
                links = [row[0] for row in csv.reader(file)]

            for idx, link in enumerate(links, start=1):
                url = f"{link}/live-score/live" if switch == 'live' else f"{link}/live-score/completed"
                driver.get(url)
                time.sleep(3)

                match_filename = f"{switch}_match_{idx}.csv"
                match_filepath = os.path.join(output_folder, match_filename)

                # Scroll to load all ball-by-ball details
                last_height = driver.execute_script("return document.body.scrollHeight")
                scroll_attempts = 0

                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)

                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        scroll_attempts += 1
                        if scroll_attempts == 2:
                            break
                        time.sleep(3)
                    else:
                        scroll_attempts = 0
                        last_height = new_height

                # Extract ball-by-ball data
                ball_numbers = driver.find_elements(By.XPATH, "//div[@class='comm_item']//span")
                scores = driver.find_elements(By.XPATH, "//div[@class='comm_item']//strong")
                comments = driver.find_elements(By.XPATH, "//div[@class='comm_item']//p")
                
                players_file = os.path.join('temp', f"match_{idx}_players.json")
                if not os.path.exists(players_file):
                    print(f"Player JSON file not found: {players_file}")
                    continue

                with open(players_file, 'r', encoding='utf-8') as pf:
                    player_data = json.load(pf)

                
                def get_player_id(player_name):
                    """Helper function to find player ID from player_data."""
                    return player_data.get(player_name, 'ID_Not_Available')

                with open(match_filepath, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(['Ball', 'Score', 'Bowler', 'Bowler ID', 'Batsman', 'Batsman ID', 'Dismissal_type'])

                    for ball, score, comment_element in zip(ball_numbers, scores, comments):
                        try:
                            comment_text = comment_element.text.strip()
                            parts = comment_text.split(",")
                            
                            # Extract bowler and batsman
                            bb = parts[0].split('to')
                            bowler = bb[0].strip()
                            batsman = bb[1].strip()

                            # Check for 'out' class in the comment element
                            dismissal = ""
                            if "playerOut" in score.get_attribute("class"):
                                dismissal = parts[3].split("!!")[0].strip()

                            bowler_id = get_player_id(bowler)
                            batsman_id = get_player_id(batsman)

                            # Write the row
                            writer.writerow([ball.text.strip(), score.text.strip(), bowler, bowler_id, batsman, batsman_id, dismissal])
                        except Exception as e:
                            print(f"Error processing ball data: {e}")
        except Exception as e:
            print(f"Error in extracting info for {switch} matches: {e}")


    
    

    def extract_and_save_scoreboards(driver, switch):
        try:
            csv_file = os.path.join('temp', 'live_match_link.csv') if switch == 'live' else os.path.join('temp', 'completed_match_link.csv')
            output_folder = os.path.join('scoreboard')
            os.makedirs(output_folder, exist_ok=True)  

            if not os.path.exists(csv_file):
                print(f"CSV file not found: {csv_file}")
                return

            with open(csv_file, 'r') as file:
                links = [row[0] for row in csv.reader(file)]

            for idx, link in enumerate(links, start=1):
                url = f"{link}/scorecard/live" if switch == 'live' else f"{link}/scorecard/completed"
                driver.get(url)
                time.sleep(5)  

                try:
                    output_file = os.path.join(output_folder, f"match_{idx}_scorecard.csv")

                    batting_headers = ["Name", "Runs", "Balls", "Fours", "Sixes", "SR"]
                    bowling_headers = ["Name", "O", "M", "R", "W", "NB", "WD", "ECO"]

                    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        current_header = None

                        rows = driver.find_elements(By.XPATH, "//div[@class='table_row']")

                        for row in rows:
                            try:
                                name = None
                                stats = []

                                all_children_by_xpath = row.find_elements(By.XPATH, ".//*")
                                for each in all_children_by_xpath:
                                    if "firstcol" in each.get_attribute("class"):
                                        try:
                                            name_element = each.find_element(By.XPATH, ".//p/strong")
                                            name = name_element.text.strip()
                                        except NoSuchElementException:
                                            name = each.text.strip().split("\n")[0]
                                    elif "t_col" in each.get_attribute("class"):
                                        stat = [col.text.strip() for col in each.find_elements(By.TAG_NAME, "p")]
                                        stats.extend(stat)

                                if len(stats) == 5:
                                    if current_header != "batting":
                                        writer.writerow([]) 
                                        writer.writerow(batting_headers)
                                        current_header = "batting"
                                    writer.writerow([name] + stats)
                                elif len(stats) == 7:
                                    if current_header != "bowling":
                                        writer.writerow([])  
                                        writer.writerow(bowling_headers)
                                        current_header = "bowling"
                                    writer.writerow([name] + stats)

                            except NoSuchElementException:
                                continue

                except Exception as e:
                    print(f"Error processing match {idx}: {e}")

        except Exception as e:
            print(f"Error in extract_and_save_scoreboards: {e}")




    def players(driver, switch):
        try:
            csv_file = os.path.join('temp', 'live_match_link.csv') if switch == 'live' else os.path.join('temp', 'completed_match_link.csv')
            output_folder = 'players'
            os.makedirs(output_folder, exist_ok=True)

            if not os.path.exists(csv_file):
                print(f"CSV file not found: {csv_file}")
                return

            with open(csv_file, 'r') as file:
                links = [row[0] for row in csv.reader(file)]

            for idx, link in enumerate(links, start=1):
                url = f"{link}/squad/live" if switch == 'live' else f"{link}/squad/completed"
                driver.get(url)

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".squad_wrap")))

                try:
                    output_file = os.path.join(output_folder, f"match_{idx}_squads.csv")
                    player_dict_file = os.path.join('temp', f"match_{idx}_players.json")

                    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        
                        player_dict = {}

                        team_1 = driver.find_element(By.CSS_SELECTOR, ".head .left strong").text.strip()
                        team_2 = driver.find_element(By.CSS_SELECTOR, ".head .right strong").text.strip()

                        def extract_player_info(elements):
                            players = []
                            for player in elements:
                                try:
                                    name_element = None
                                    try:
                                        name_element = player.find_element(By.TAG_NAME, "p").find_element(By.TAG_NAME, "strong").find_element(By.TAG_NAME, "a")
                                        name = name_element.text.strip()
                                        href = name_element.get_attribute("href")
                                        player_number = href.split("/")[-2]
                                    except Exception:
                                        name = player.find_element(By.TAG_NAME, "p").find_element(By.TAG_NAME, "strong").text.strip()
                                        player_number = "N/A"

                                    span_tags = player.find_element(By.TAG_NAME, "p").find_elements(By.TAG_NAME, "span")
                                    if len(span_tags) >= 2:
                                        designation = span_tags[1].text.strip()
                                    else:
                                        designation = span_tags[0].text.strip() if span_tags else ""

                                    image_element = player.find_element(By.CLASS_NAME, "thumb").find_element(By.TAG_NAME, "img")
                                    image_link = image_element.get_attribute("src")

                                    players.append((name, designation, player_number, image_link))
                                    player_dict[name] = player_number
                                except Exception as e:
                                    print(f"Error extracting player info: {e}")
                            return players

                        playing11_1_elements = driver.find_elements(By.CSS_SELECTOR, ".leftcol li")[:11]
                        playing11_2_elements = driver.find_elements(By.CSS_SELECTOR, ".rightcol li")[:11]
                        bench_1_elements = driver.find_elements(By.CSS_SELECTOR, ".leftcol li")[11:]
                        bench_2_elements = driver.find_elements(By.CSS_SELECTOR, ".rightcol li")[11:]

                        playing11_1 = extract_player_info(playing11_1_elements)
                        playing11_2 = extract_player_info(playing11_2_elements)
                        bench_1 = extract_player_info(bench_1_elements)
                        bench_2 = extract_player_info(bench_2_elements)

                        writer.writerow([f"{team_1} Playing XI"])
                        writer.writerow(["Name", "Designation", "Player Number", "Image Link"])
                        for p1 in playing11_1:
                            writer.writerow(p1)
                        writer.writerow(["---------------------------------"])

                        writer.writerow([f"{team_1} Bench"])
                        writer.writerow(["Name", "Designation", "Player Number", "Image Link"])
                        for b1 in bench_1:
                            writer.writerow(b1)
                        writer.writerow([])
                        writer.writerow(["---------------------------------"])
                        writer.writerow(["---------------------------------"])
                        writer.writerow([])

                        writer.writerow([f"{team_2} Playing XI"])
                        writer.writerow(["Name", "Designation", "Player Number", "Image Link"])
                        for p2 in playing11_2:
                            writer.writerow(p2)
                        writer.writerow(["---------------------------------"])

                        writer.writerow([f"{team_2} Bench"])
                        writer.writerow(["Name", "Designation", "Player Number", "Image Link"])
                        for b2 in bench_2:
                            writer.writerow(b2)
                        writer.writerow(["---------------------------------"])

                    with open(player_dict_file, 'w', encoding='utf-8') as jsonfile:
                        json.dump(player_dict, jsonfile, ensure_ascii=False, indent=4)

                except Exception as e:
                    print(f"Error processing match {idx}: {e}")

        except Exception as e:
            print(f"Error in scrape_teams_and_players: {e}")
