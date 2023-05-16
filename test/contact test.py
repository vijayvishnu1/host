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
driver.find_element("link text", "Contact us").click()
time.sleep(3)

print("Contact us form")
driver.find_element("id", "name").send_keys("vijay")
time.sleep(3)
driver.find_element("id", "email").send_keys("vijayvishnu@gmail.com")
time.sleep(3)
driver.find_element("id", "message").send_keys("want to contact urgently make necessary assignments")
time.sleep(3)

driver.find_element("xpath", "/html/body/section/div/div/form/input[3]").click()
time.sleep(3)
print("Test done")