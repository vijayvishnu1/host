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
driver.find_element("link text", "Client").click()
time.sleep(3)
print("view client")
driver.find_element("xpath", "/html/body/section/div/div/div/div[1]/a").click()
time.sleep(3)
print("view details")
driver.find_element("xpath", "/html/body/section/div/div/div/div[2]/div/div[2]/ul/li[7]/a/button").click()
time.sleep(3)
print("download pdf")
print("Test done")
