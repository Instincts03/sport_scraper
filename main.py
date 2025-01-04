import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from actions import Game
from scraper import Info
import time
import csv

# series = input("Enter the series ID (numeric only): ").strip()
# if not series.isdigit():
#     print("Error: Series ID must be a numeric value.")
#     exit()

# switch = input("Enter the switch ('live' or 'completed'): ").strip().lower()
# if switch not in ["live", "completed"]:
#     print("Error: Switch must be either 'live' or 'completed'.")
#     exit() 

series = '10850'
switch = 'completed'
BASE_LINK = f"https://www.sportstiger.com/cricket/series/matches/{series}/"

# squad = f"https://www.sportstiger.com/cricket/series/squad/{series}/"



with Game() as bot:
    
    # ###Get the teams playing in the tournament

    # bot.squads(squad)
    # time.sleep(1)
    # teams=Info.scrape_team_names(bot)
    # with open('teams.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows([[team] for team in teams]) 
        
    # print("Teams playing in the tournament are saved in teams.csv file")



    # ### Squad for each team

    # input_csv = 'teams.csv'
    # output_csv = 'teams_players.csv'
    # bot.squads(squad)

    # with open(input_csv, 'r') as csvfile:
    #     reader = csv.reader(csvfile)
    #     team_names = [row[0] for row in reader]

    # with open(output_csv, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['Team Name', 'Player Name', 'Designation']) 

    #     first_team = team_names[0]
    #     team_data = Info.scrape_players_for_team(bot, first_team)
    #     for player_name, designation in team_data:
    #         writer.writerow([first_team, player_name, designation])

    #     for team in team_names[1:]:
    #         bot.click_team(team)
    #         team_data = Info.scrape_players_for_team(bot, team)
    #         for player_name, designation in team_data:
    #             writer.writerow([team, player_name, designation])
    
    # print("Players for each team are saved in teams_players.csv file")


        
    # ###Get links of the matches
    # bot.land_first_page(BASE_LINK)
    # time.sleep(2)

    # bot.click_result_button()
    # time.sleep(2)
    # Info.matches_links(bot, switch='completed')

    # bot.click_live_button()
    # time.sleep(2)
    # Info.matches_links(bot,switch='live')

    # bot.click_upcoming_button()
    # time.sleep(2)
    # Info.matches_links(bot,switch='upcoming')
    
    # print("Schedule of the matches are saved in schedule.csv file")
    
    
    
    # ### Get schedule of the matches
    
    # Info.schedule(bot, switch='completed')
    # Info.schedule(bot,switch='live')
    # Info.schedule(bot,switch='upcoming')



    # ### Ball-by-Ball info
    #Info.extract_ball_by_ball(bot,switch)
    
    # print("Ball-by-Ball info is saved in ball_by_ball.csv file")



    # ### Scoreboard
    #Info.extract_and_save_scoreboards(bot)
    
    # print("Scoreboard is saved in scoreboard.csv file")

    # ### Playing 11 and benched players
    #Info.players(bot,switch)
    
    # print("Playing 11 and benched players are saved in playing_11.csv file")
    
    
    

    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # '''To remove the stake 10 sec ad(6-9)'''
    # try:
    #     # Wait for the ad container to appear
    #     ad_container = WebDriverWait(bot, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'fullads_banner')]"))
    #     )
    #     print("Ad container located.")

    #     # Wait for the close button to become clickable
    #     try:
    #         close_button = WebDriverWait(ad_container, 10).until(
    #             EC.element_to_be_clickable((By.XPATH, ".//span[contains(@class, 'close_pop')]"))
    #         )
            
            
    #         print("Ad closed successfully.")
    #     except Exception as e:
    #         print("Close button not found after 10 seconds. Proceeding...")
    
    # except Exception as e:
    #     print(f"Ad container not found: {e}")
        
    # bot.click_result_button()
    # print('completed')
    # input("Press Enter to exit...")
    
    
