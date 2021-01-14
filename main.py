import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import actions, action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


class SeleniumConfig(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.absolute = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(self.absolute, options=options)
        self.action = webdriver.common.action_chains.ActionChains(self.driver)

    def jupiter_1(self, name, emailaddress, messageto):
        self.driver.get('http://jupiter.cloud.planittesting.com')
        self.assertIn("Jupiter Toys", self.driver.title)
        self.driver.find_element_by_id("nav-contact").click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Submit"))
            )
        finally:
            self.driver.find_element_by_link_text("Submit").click()  # click submit
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
            print("Errors on page")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "forename-err")))
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email-err")))
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "message-err")))
        except NoSuchElementException:
            pass
        # to clear the errors
        forename = self.driver.find_element_by_id("forename")
        email = self.driver.find_element_by_id("email")
        message = self.driver.find_element_by_id("message")
        # populating mandatory fields
        forename.send_keys(name)
        email.send_keys(emailaddress)
        message.send_keys(messageto)
        # checking to see if errors are avaliable - could also be an if else statement
        try:
            if self.driver.find_element_by_id("forename-err") is None:
                print("forename success 2")
            else:
                print("forename error 2")
            if self.driver.find_element_by_id("email-err") is None:
                print("email success 2")
            else:
                print("email error 2")
            if self.driver.find_element_by_id("message-err") is None:
                print("message success 2")
            else:
                print("message error 2")
        except NoSuchElementException as error:
            print("second error", error)
        finally:
            time.sleep(5)
            self.driver.quit()

    def jupiter_2(self, name, emailaddress, messageto):
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

        time.sleep(5)  # so we can check final screen
        self.driver.quit()

    def jupiter_3(self, name, emailaddress, messageto):
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
        action.perform()
        time.sleep(10)
        # self.driver.find_element_by_link_text("Submit").click() # not going to submit to get error validations
        # checking to see if errors are avaliable - could also be an if else statement
        try:
            if self.driver.find_element_by_id("forename-err") is not None:
                print("forename form error")
            if self.driver.find_element_by_id("email-err") is not None:
                print("email form error")
            if self.driver.find_element_by_id(
                    "message-err") is not None:  # need to reiterate this there's a bug where even if the string is empty, the error validation will not appear unless you click outside the box
                print("message form error")
        except NoSuchElementException as suchElementerrors:
            print("no errors", suchElementerrors)
        finally:
            pass

        time.sleep(5)
        self.driver.quit()

    def jupiter_4(self):
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
        cow = self.driver.find_element_by_xpath("/html/body/div[2]/div/ul/li[6]/div/p/a[@class='btn btn-success']")
        bunny = self.driver.find_element_by_xpath("/html/body/div[2]/div/ul/li[4]/div/p/a[@class='btn btn-success']")
        cow.click()
        cow.click()
        bunny.click()
        self.driver.find_element_by_id("nav-cart").click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/p[@class='cart-msg']"))
            )
        except NoSuchElementException as error:
            print(error)
        cart_message = self.driver.find_element_by_xpath("/html/body/div[2]/div/p[@class='cart-msg']")
        print(cart_message.text)
        table_body = self.driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody")
        print(table_body.text)
        time.sleep(10)
        self.driver.quit()


if __name__ == "__main__":
    # SeleniumConfig().jupiter_1("johnpham", "john.pham92@email.com", "heyhey")
    # SeleniumConfig().jupiter_2("johnpham", "john.pham92@email.com", "heyhey")
    SeleniumConfig().jupiter_3("", "john.pham92", "")
    # SeleniumConfig().jupiter_4()
