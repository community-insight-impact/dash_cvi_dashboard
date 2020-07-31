import time
import os
import shutil
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


LOGIN_ID = "ngocdiep892000_PUmagic" #"passarelli.alexandra_PUmagic"
LOGIN_PW = "numnum289" #"Shared05242020"
CHROMEDRIVER_PATH = "/Applications/chromedriver"
LAYER_NAME = "severe_cases_score_data_testing"
LAYER_XPATH = '//*[@id="uniqName_6_0"]/span[1]/span/span[1]/a'
WEB = "https://pumagic.maps.arcgis.com/sharing/rest/oauth2/authorize?client_id=arcgisonline&display=default&response_type=token&state=%7B%22returnUrl%22%3A%22https%3A%2F%2Fpumagic.maps.arcgis.com%2Fhome%2Fcontent.html%3Fview%3Dtable%26sortOrder%3Ddesc%26sortField%3Dmodified%26folder%3Dpassarelli.alexandra_PUmagic%23content%22%2C%22useLandingPage%22%3Afalse%7D&expiration=20160&locale=en-us&redirect_uri=https%3A%2F%2Fpumagic.maps.arcgis.com%2Fhome%2Faccountswitcher-callback.html&force_login=false&hideCancel=true&showSignupOption=true&canHandleCrossOrgSignIn=true&signuptype=esri"


class UpdateBot():
    def __init__(self):
        options = Options()
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome('/Applications/chromedriver')
        self.base_window = self.driver.window_handles[0]

    def login_arcgis(self):
        self.driver.get('https://www.arcgis.com/sharing/rest/oauth2/authorize?client_id=arcgisonline&display=default&response_type=token&state=%7B%22useLandingPage%22%3Atrue%7D&expiration=20160&locale=en-us&redirect_uri=https%3A%2F%2Fwww.arcgis.com%2Fhome%2Faccountswitcher-callback.html&force_login=true&hideCancel=true&showSignupOption=true&canHandleCrossOrgSignIn=true&signuptype=esri')
        #Login with zoom login information
        time.sleep(3)
        email = self.driver.find_element_by_xpath('//*[@id="user_username"]')
        email.send_keys(LOGIN_ID)
        password = self.driver.find_element_by_xpath('//*[@id="user_password"]')
        password.send_keys(LOGIN_PW)
        login_btn = self.driver.find_element_by_xpath('//*[@id="signIn"]')
        login_btn.click()
        time.sleep(8)

    def open_content(self):
    	content = self.driver.find_element_by_xpath('//*[@id="esri-header-menus-link-desktop-0-5"]/span')
    	content.click()

    def update_layer(self):
        time.sleep(4)
    	layer = self.driver.find_element_by_link_text(LAYER_XPATH)
    	layer.click()
    	time.sleep(3)
 		self.driver.find_element_by_link_text("Update Data").click()
 		self.driver.find_element_by_link_text("").click()


bot = UpdateBot()
bot.login_arcgis()
bot.open_content()
