from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
print("Login test case started")
options=webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches',['enable-logging'])
driver = webdriver.Chrome(r'C:\Users\VORTEX\Downloads\chromedriver_win32\chromedriver.exe', options=options)
driver.maximize_window()
driver.get("http://127.0.0.1:8000/login/")
driver.find_element("id", "user_id").send_keys("vortex")
time.sleep(3)
driver.find_element("id", "password1").send_keys("Nfsundercover")
time.sleep(3)
driver.find_element("xpath", "/html/body/div[1]/div[1]/form/input[4]").click()
time.sleep(3)
print("User Logged In")

# ***********Test Case 3 : Guest Enquiry sending from Guest Home Page. ***************
# Navigate to Studenthome and change the password
print("Advocate Home Page ")
driver.get("http://127.0.0.1:8000/advocatehome/")
time.sleep(3)
print("update profile")
driver.find_element("link text", "Profile Settings").click()
time.sleep(3)
driver.find_element("xpath", "/html/body/section/div/div/div/div[3]/center/a/button").click()
time.sleep(3)


driver.find_element("id", "expervalue").send_keys("4")
time.sleep(3)


driver.find_element("xpath", "/html/body/div[2]/div/form/div[3]/button").click()
time.sleep(3)
print("profile updated successfully")