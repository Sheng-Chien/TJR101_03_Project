from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class SeleniumDriver():
    def __init__(self):
        driver_path = Path(__file__).parent/"chromedriver.exe"
        service = Service(driver_path)
        options = Options()
        self.driver = webdriver.Chrome(options=options, service=service)
    
    def gotoURL(self, url):
        self.driver.get(url)

    def waitElement(self, element):
        return True
    
    def getElement(self):
        return self.driver.page_source

    
