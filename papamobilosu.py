import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import atexit
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

class PapamobilOsu():
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--user-data-dir=" + os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "chromiumprofile")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(options=self.options)
        self.url = 'https://osu.ppy.sh/beatmapsets?m=0'
        self.driver.get(self.url)
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.actions = ActionChains(self.driver)

    def getLatestMap(self):
        self.driver.refresh()
        self.link = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[4]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]/a")))
        self.latestmapname = self.link.get_attribute("innerHTML")
        return self.latestmapname


if __name__ == "__main__":
    osuweb = PapamobilOsu()
    latestmap = osuweb.getLatestMap()
    print(latestmap)
