from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from flask_testing import LiveServerTestCase
import time
from server import app, competitions, clubs
import server

# user_email = 'john@simplylift.co'

# class Tests(object):
#     # def open_chrome(self):
#     #     self.driver = webdriver.Chrome('tests/functionnal_tests/chromedriver')
#     # def __init__(self):
#     #     try:
#     #         self.app = server.app
#     #         self.driver = webdriver.Chrome('tests/functionnal_tests/chromedriver')
#     #     except Exception as e:
#     #         print('ERRRRR ::::::::', e)

#     def test_login(self):
#         self.app = server.app
#         self.service = Service('./chromedriver')
#         self.driver = webdriver.Chrome(
#             executable_path='./chrome',
#             service=self.service)
#         self.driver.get(self.get_server_url('/'))
#         time.sleep(30)
#         self.driver.close()
