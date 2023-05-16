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


print("Advocate Home Page ")
driver.get("http://127.0.0.1:8000/advocatehome/")
time.sleep(3)
driver.find_element("link text", "Schedule").click()
time.sleep(3)
driver.find_element("link text", "Add Schedule").click()
time.sleep(3)
print("Schedule adding started")
driver.find_element("id", "date").send_keys("11-05-2023")
time.sleep(3)
driver.find_element("id", "start_time").send_keys("01:03")
time.sleep(3)
driver.find_element("id", "end_time").send_keys("02:05")
time.sleep(3)
driver.find_element("id", "description").send_keys("meeting with client")
time.sleep(3)
driver.find_element("xpath", "/html/body/section/div/div/div/div/div/div[2]/form/button").click()
time.sleep(3)
print("schedule added")
print("Test successfully completed")

# print("Login test case started")
# print("User Logged In")
# print("Advocate Home Page ")
# print("Schedule adding started")
# print("schedule added")
# print("Test successfully completed")