

import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

print("Login test case started")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
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
driver.find_element("link text", "Messages").click()
time.sleep(3)
driver.find_element("link text", "kishore kumar").click()
time.sleep(3)
print("chatting started")
driver.find_element("id", "messageInput").send_keys("hello there")
time.sleep(3)
driver.find_element("xpath", "/html/body/section/div/div/div[2]/form/div/button").click()
time.sleep(3)
print("chat completed")






# import time
# from msedge.selenium_tools import EdgeOptions, Edge
#
# print("Login test case started")
#
# options = EdgeOptions()
# options.use_chromium = True
# options.add_argument('--no-proxy')  # Bypass the proxy
#
# # Path to the Microsoft Edge WebDriver executable
# driver_path = "C:\\Users\\VORTEX\\Downloads\\edgedriver_win64\\msedgedriver.exe"
#
# # Initialize the webdriver
# driver = Edge(executable_path=driver_path, options=options)
# driver.maximize_window()
# # Rest of your code...
#
# driver.get("http://127.0.0.1:8000/login/")
# driver.find_element("id", "user_id").send_keys("vortex")
# time.sleep(3)
# driver.find_element("id", "password1").send_keys("Nfsundercover")
# time.sleep(3)
# driver.find_element("xpath", "/html/body/div[1]/div[1]/form/input[4]").click()
# time.sleep(3)
# print("User Logged In")

