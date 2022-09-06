from lib2to3.pgen2 import driver
import os
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.contenttypes.models import ContentType

from selenium import webdriver
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
from selenium.webdriver.common.by import By
import time


class TestWebsiteAuth(StaticLiveServerTestCase):
    driver = None
    port = 8080

    @classmethod
    def setUpClass(cls):
        ContentType.objects.clear_cache()
        super().setUpClass()
        cls.driver = webdriver.Chrome(executable_path=r"./chromedriver.exe")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.driver.get(cls.live_server_url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user_password = "1234@@##"
        self.user_username = "malak"
        self.user = User.objects.create_user(
            username=self.user_username, password=self.user_password
        )
        self.user.save()

    def tearDown(self):
        self.user.delete()
    @classmethod
    def wait_until(cls, findhow, findwhere):
        WebDriverWait(cls.selenium, 10).until(EC.element_to_be_clickable((findhow,findwhere)))


    def test_auth(self):
        driver = self.driver
        driver.get(self.live_server_url)
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        username.send_keys(self.user_username)
        password.send_keys(self.user_password)
        password.send_keys(Keys.RETURN)
        driver.get(self.live_server_url + "/transaction/transactionForm/")
        driver.find_element(By.ID, "testLogout").click()
        driver.get(self.live_server_url + "/logout/")
        self.assertEqual(driver.current_url, self.live_server_url + "/logout/")
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()

 