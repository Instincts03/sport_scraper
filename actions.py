from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import os
import time

class Game(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDrivers"):
        self.driver_path = driver_path
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-cache")
        super(Game, self).__init__(options=options)



    def land_first_page(self,link):
        self.get(link)
        
    
    def squads(self,link):
        self.get(link)
        
    def click_result_button(self):
        result_button = self.find_element(By.XPATH, ".//div[@class='whiteblock match_statustab']//ul/li[a[text()='Result']]//a")
        self.execute_script("arguments[0].click();", result_button)
    
    def click_live_button(self):
        live_button = self.find_element(By.XPATH, ".//div[@class='whiteblock match_statustab']//ul/li[a[text()='Live']]//a")
        self.execute_script("arguments[0].click();", live_button)
        
    def click_upcoming_button(self):
        upcoming_button = self.find_element(By.XPATH, ".//div[@class='whiteblock match_statustab']//ul/li[a[text()='Upcoming']]//a")
        self.execute_script("arguments[0].click();", upcoming_button)
        
    def click_team(driver, team):
        try:
            team_element = driver.find_element(By.XPATH, f"//strong[text()='{team}']")
            driver.execute_script("arguments[0].click();", team_element)
            time.sleep(1)  # Allow time for the page to load
        except Exception as e:
            print(e)
            return


        
        
    # def click_result_button_with_ad(self):
    #     close_button = WebDriverWait(self, 5).until(
    #         EC.element_to_be_clickable((By.XPATH, "//div[@class='footerSticky']//div[@class='closeBTN']//span[@class='close']"))
    #     )

    #     # Click the close button
    #     close_button.click()
    #     print("Ad closed.")
        
    #     stop_seeing_this_ad_button = WebDriverWait(self, 5).until(
    #         EC.element_to_be_clickable((By.XPATH, "//div[@class='adsOverlay']//div[@class='twoBtns']//a[contains(text(), 'Stop seeing this ad')]"))
    #     )

    #     # Click the button
    #     stop_seeing_this_ad_button.click()
    #     print("Clicked 'Stop seeing this ad' button.")
        
    #     result_button = WebDriverWait(self, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, ".//div[@class='whiteblock match_statustab']//ul/li[a[text()='Result']]//a"))
    #     )

    #     # Click the "Result" button
    #     result_button.click()
    #     print("Result button clicked successfully!")