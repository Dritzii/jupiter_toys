import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import actions, action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from trace import tracefunc
import time
import os
import sys

# sys.setprofile(tracefunc) # set this if you want a custom trace function - not particularly useful but it is interesting to watch

ABSOLUTE = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver.exe"  # added as global instead of object const


class SeleniumConfig(unittest.TestCase):

    def __init__(self):
        super().__init__()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(ABSOLUTE, options=options)
        self.action = webdriver.common.action_chains.ActionChains(self.driver)
        self.driver.implicitly_wait(5)

    def jupiter_1(self, name, emailaddress, messageto):
        """
        Test case 1:
            1.	From the home page go to contact page
            2.	Click submit button
            3.	Validate errors
            4.	Populate mandatory fields
            5.	Validate errors are gone
        :param name: STRING
        :param emailaddress: STRING
        :param messageto: STRING
        :return: None
        """
        self.driver.get('http://jupiter.cloud.planittesting.com')
        self.assertIn("Jupiter Toys", self.driver.title)
        self.driver.find_element_by_id("nav-contact").click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Submit"))
            )
        finally:
            self.driver.find_element_by_link_text("Submit").click()  # click submit
        self.assertTrue(self.driver.find_element_by_link_text(
            "Submit").is_enabled())
        # validating errors using if statement and catching with try block
        try:
            if self.driver.find_element_by_id("forename-err") is None:
                print("forename success 1")
            else:
                print("forename error 1")
            if self.driver.find_element_by_id("email-err") is None:
                print("email success 1")
            else:
                print("email error 1")
            if self.driver.find_element_by_id("message-err") is None:
                print("message success 1")
            else:
                print("message error 1")
        except NoSuchElementException as firsterror:
            print(firsterror)
        finally:
            pass
        # to clear the errors
        forename = self.driver.find_element_by_id("forename")
        email = self.driver.find_element_by_id("email")
        message = self.driver.find_element_by_id("message")
        # populating mandatory fields
        forename.send_keys(name)
        email.send_keys(emailaddress)
        message.send_keys(messageto)
        action = self.action
        action.move_to_element_with_offset(message, 50, 0)  # move 50 pixels to the right
        action.click()  # click to the right
        action.perform()  # the perform method seems to vary between 10 - 20 seconds
        time.sleep(20)  # making sure that the click actually happens before the try catch happens
        # checking to see if errors are avaliable - could also be an if else statement
        try:
            if self.driver.find_element_by_id("forename-err") is None:
                print("forename success 2")
        except NoSuchElementException as error:
            print("second forname-err not found", error)
        try:
            if self.driver.find_element_by_id("email-err") is None:
                print("email success 2")
        except NoSuchElementException as error:
            print("second email-err", error)
        try:
            if self.driver.find_element_by_id("message-err") is None:
                print("message success 2")
        except NoSuchElementException as error:
            print("second message-err", error)
        finally:
            self.driver.quit()

    def jupiter_2(self, name, emailaddress, messageto):
        """
        Test case 2:
            1.	From the home page go to contact page
            2.	Populate mandatory fields
            3.	Click submit button
            4.	Validate successful submission message
        :param name: STRING
        :param emailaddress: STRING
        :param messageto: STRING
        :return: None
        """
        self.driver.get('http://jupiter.cloud.planittesting.com')
        self.assertIn("Jupiter Toys", self.driver.title)
        self.driver.find_element_by_id("nav-contact").click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Submit"))
            )
        finally:
            pass
            # self.driver.find_element_by_link_text("Submit").click() # test case 2 doesn't require to submit before populating
        # if self.driver.find_element_by_class_name("alert.alert-error.ng-scope"):
        #    print("found the submit error")
        forename = self.driver.find_element_by_id("forename")
        email = self.driver.find_element_by_id("email")
        message = self.driver.find_element_by_id("message")
        forename.send_keys(name)
        email.send_keys(emailaddress)
        message.send_keys(messageto)
        print("sending form data")
        self.driver.find_element_by_link_text("Submit").click()
        try:
            print(
                "waiting for alert success")  ## this seems to be random from 10 - 30 seconds based on how many times you've posted form data towards the endpoint
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-success"))
            )
        except NoSuchElementException as error:
            print(error)
        finally:
            if self.driver.find_element_by_class_name("alert.alert-success"):
                print("success")
            text = self.driver.find_elements_by_class_name(
                "ng-binding")  # .get_attribute("outerHTML") # getting text of alert
            for texts in text:
                print(texts.text)
            self.driver.quit()

    def jupiter_3(self, name, emailaddress, messageto):
        """
        Test case 3:
            1.	From the home page go to contact page
            2.	Populate mandatory fields with invalid data
            3.	Validate errors

        :param name: STRING
        :param emailaddress: STRING
        :param messageto: STRING
        :return: None
        """
        self.driver.get('http://jupiter.cloud.planittesting.com')
        self.assertIn("Jupiter Toys", self.driver.title)
        self.driver.find_element_by_id("nav-contact").click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Submit"))
            )
        finally:
            pass
            # self.driver.find_element_by_link_text("Submit").click() # test case 3 is not testing for a submit post
        # to clear the errors
        forename = self.driver.find_element_by_id("forename")
        email = self.driver.find_element_by_id("email")
        message = self.driver.find_element_by_id("message")
        # populating mandatory fields
        forename.send_keys(name)
        email.send_keys(emailaddress)
        message.send_keys(messageto)
        action = self.action
        action.move_to_element_with_offset(message, 50, 0)  # move 50 pixels to the right
        action.click()  # click to the right
        action.perform()  # the perform method seems to vary between 10 - 20 seconds
        time.sleep(20)  # making sure that the click actually happens before the try catch happens
        # self.driver.find_element_by_link_text("Submit").click() # not going to submit to get error validations using above instead
        # checking to see if errors are avaliable
        try:
            if self.driver.find_element_by_id("forename-err") is not None:
                print("forename form error")
            if self.driver.find_element_by_id("email-err") is not None:
                print("email form error")
            if self.driver.find_element_by_id(
                    "message-err") is not None:  # need to reiterate this there's a bug where even if the string is empty, the error validation will not appear unless you click outside the box or submit
                print("message form error")
        except NoSuchElementException as suchElementerrors:
            print("no errors", suchElementerrors)
        finally:
            self.driver.quit()

    def jupiter_4(self):
        """
        Test case 4:
            1.	From the home page go to shop page
            2.	Click buy button 2 times on “Funny Cow”
            3.	Click buy button 1 time on “Fluffy Bunny”
            4.	Click the cart menu
            5.	Verify the items are in the cart

        :return: None
        """
        self.driver.get('http://jupiter.cloud.planittesting.com')
        self.assertIn("Jupiter Toys", self.driver.title)
        self.driver.find_element_by_id("nav-shop").click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "products.ng-scope"))
            )
        except NoSuchElementException as error:
            print(error)
        # locating buttons for stuffed animals
        cow = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/ul/li[6]/div/p/a[@class='btn btn-success']")  # assign button click to variable for 2 clicks
        bunny = self.driver.find_element_by_xpath("/html/body/div[2]/div/ul/li[4]/div/p/a[@class='btn btn-success']")
        cow.click()
        cow.click()
        bunny.click()
        self.driver.find_element_by_id("nav-cart").click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/p[@class='cart-msg']"))
                # waiting for the cart to appear after nav-cart
            )
        except NoSuchElementException as error:
            print(error)
        finally:
            cart_message = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/p[@class='cart-msg']")  # find cart message
            print(cart_message.text)
            table_body = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/form/table/tbody")  # print out cart message
            print(table_body.text)
            self.driver.quit()


if __name__ == "__main__":
    SeleniumConfig().jupiter_1("johnpham", "john.pham92@email.com", "heyhey")
    SeleniumConfig().jupiter_2("johnpham", "john.pham92@email.com", "heyhey")
    SeleniumConfig().jupiter_3("", "john.pham92", "")
    SeleniumConfig().jupiter_4()
