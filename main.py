import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import actions, action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import log
from trace import tracefunc
import time
import os
import sys

# sys.setprofile(tracefunc) # set this if you want a custom trace function - not particularly useful but it is interesting to watch

ABSOLUTE = os.path.dirname(
    os.path.abspath(__file__)) + "/chromedriver.exe"  # added as global instead of object constructor


class SeleniumConfig(unittest.TestCase):

    def __init__(self):
        super().__init__()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(ABSOLUTE, options=options)
        self.action = webdriver.common.action_chains.ActionChains(self.driver)
        self.driver.implicitly_wait(5)

    @log.log_error()
    def pre_start(self):
        self.driver.get('http://jupiter.cloud.planittesting.com')
        self.assertIn("Jupiter Toys", self.driver.title)

    @log.log_error()
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
        self.pre_start()
        self.driver.find_element_by_id("nav-contact").click()
        try:
            # WebDriverWait(self.driver, 10).until(
            #    EC.presence_of_element_located((By.LINK_TEXT, "Submit"))
            # )
            self.wait_implicity_for_element(self.driver, 10, By.XPATH,
                                            "/html/body/div[2]/div/form/div/a[@class='btn-contact btn btn-primary']")
        finally:
            # self.driver.find_element_by_link_text("Submit").click()  # click submit
            self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/form/div/a[@class='btn-contact btn btn-primary']").click()
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
        self.sending_form_data(forename, name)
        self.sending_form_data(email, emailaddress)
        self.sending_form_data(message, messageto)
        self.action_movement(self.action, message, 50, 0)  # performs mouse click
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
            self.quit_driver(self.driver)

    @log.log_error()
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
        self.pre_start()
        self.driver.find_element_by_id("nav-contact").click()
        try:
            # WebDriverWait(self.driver, 10).until(
            #    EC.presence_of_element_located((By.LINK_TEXT, "Submit")) # stack overflow says fullx path is better?
            # )
            self.wait_implicity_for_element(self.driver, 10, By.XPATH,
                                            "/html/body/div[2]/div/form/div/a[@class='btn-contact btn btn-primary']")
        finally:
            pass
            # self.driver.find_element_by_link_text("Submit").click() # test case 2 doesn't require to submit before populating
        # if self.driver.find_element_by_class_name("alert.alert-error.ng-scope"):
        #    print("found the submit error")
        forename = self.driver.find_element_by_id("forename")
        email = self.driver.find_element_by_id("email")
        message = self.driver.find_element_by_id("message")
        self.sending_form_data(forename, name)
        self.sending_form_data(email, emailaddress)
        self.sending_form_data(message, messageto)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/form/div/a[@class='btn-contact btn btn-primary']").click()
        # self.driver.find_element_by_link_text("Submit").click()
        try:
            ## this seems to be random from 10 - 30 seconds based on how many times you've posted form data towards the endpoint
            self.wait_implicity_for_element(self.driver, 30, By.CLASS_NAME,
                                            "alert.alert-success")
        except NoSuchElementException as error:
            print(error)
        finally:
            if self.driver.find_element_by_class_name("alert.alert-success"):
                print("success")
            self.show_body_elem(self.driver, "/html/body/div[2]/div/div/strong[@class='ng-binding']")
            self.quit_driver(self.driver)

    @log.log_error()
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
        action = self.action
        self.pre_start()
        self.driver.find_element_by_id("nav-contact").click()
        try:
            # WebDriverWait(self.driver, 10).until(
            #    EC.presence_of_element_located((By.LINK_TEXT, "Submit"))
            # )
            self.wait_implicity_for_element(self.driver, 10, By.XPATH,
                                            "/html/body/div[2]/div/form/div/a[@class='btn-contact btn btn-primary']")
        finally:
            pass
            # self.driver.find_element_by_link_text("Submit").click() # test case 3 is not testing for a submit post
        # to clear the errors
        forename = self.driver.find_element_by_id("forename")
        email = self.driver.find_element_by_id("email")
        message = self.driver.find_element_by_id("message")
        telephone = self.driver.find_element_by_id("telephone")
        # populating mandatory fields
        self.sending_form_data(forename, name)
        self.sending_form_data(email, emailaddress)
        self.sending_form_data(message, messageto)
        self.sending_form_data(telephone, messageto) # added this to allow message error to pop up
        self.action_movement(self.action, message, 55, 0)  # performs mouse click
        # self.driver.find_element_by_link_text("Submit").click() # not going to submit to get error validations using above instead
        # checking to see if errors are avaliable
        try:
            if self.driver.find_element_by_id("forename-err") is not None:  # assuming that my input still has errors
                print("forename form error")
            if self.driver.find_element_by_id("email-err") is not None:
                print("email form error")
            if self.driver.find_element_by_id(
                    "message-err") is not None:  # need to reiterate this there's a bug where even if the string is empty, the error validation will not appear unless you click outside the box or submit
                print("message form error")
        except NoSuchElementException as suchElementerrors:
            print("no errors", suchElementerrors)
        finally:
            self.quit_driver(self.driver)

    @log.log_error()
    def jupiter_4(self, cow_click, bunny_click):
        """
        Test case 4:
            1.	From the home page go to shop page
            2.	Click buy button 2 times on “Funny Cow” # added method to add no. in args
            3.	Click buy button 1 time on “Fluffy Bunny”
            4.	Click the cart menu
            5.	Verify the items are in the cart

        :return: None
        """
        self.pre_start()
        self.driver.find_element_by_id("nav-shop").click()
        try:
            self.wait_implicity_for_element(self.driver, 10, By.CLASS_NAME, "products.ng-scope")
        finally:
            pass
        # locating buttons for stuffed animals
        cow = self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/ul/li[6]/div/p/a[@class='btn btn-success']")  # assign button click to variable for 2 clicks
        bunny = self.driver.find_element_by_xpath("/html/body/div[2]/div/ul/li[4]/div/p/a[@class='btn btn-success']")
        self.click_multiple(cow, cow_click)  # assuming someone wants to click more than once
        self.click_multiple(bunny, bunny_click)
        self.driver.find_element_by_id(
            "nav-cart").click()  # can use xpath too /html/body/div[1]/div/div/div/ul[2]/li[4]/a
        try:
            self.wait_implicity_for_element(self.driver, 10, By.XPATH, "/html/body/div[2]/div/p[@class='cart-msg']")
        finally:
            self.show_body_elem(self.driver, "/html/body/div[2]/div/p[@class='cart-msg']")
            self.show_body_elem(self.driver, "/html/body/div[2]/div/form/table/tbody")
            self.quit_driver(self.driver)

    @staticmethod
    def show_body_elem(driver, xpath):
        data = driver.find_element_by_xpath(xpath)
        print(data.text)

    @staticmethod
    def click_multiple(objecttoclick, numberofclicks):
        print("Clicking ", numberofclicks)
        for i in range(numberofclicks):
            objecttoclick.click()

    @staticmethod
    def wait_implicity_for_element(driver, length, bypath, elem):
        print("implcitly waiting", driver, length, bypath, elem)
        try:
            WebDriverWait(driver, length).until(
                EC.presence_of_element_located((bypath, elem))
            )
        except NoSuchElementException as error:
            print(error)

    @staticmethod
    def action_movement(action, message, pixelr, pixell, sleepint=10):
        print("action movement", action, message, pixelr, pixell)
        print("pixels to the right: ", pixelr, "\npixels to the left: ", pixell)
        print("sleeping seconds: ", sleepint)
        action.move_to_element_with_offset(message, pixelr, pixell)  # move 50 pixels to the right
        action.click().perform()  # click to the right
        time.sleep(sleepint)  # making sure that the click actually happens before the try catch happens

    @staticmethod
    def sending_form_data(elem, data):
        print("sending data ", elem, data)
        elem.send_keys(data)

    @staticmethod
    def quit_driver(driver):
        print("Quitting driver")
        driver.quit()


if __name__ == "__main__":
    #SeleniumConfig().jupiter_1("johnpham", "john.pham92@email.com", "heyhey")
    #SeleniumConfig().jupiter_2("johnpham", "john.pham92@email.com", "heyhey")
    SeleniumConfig().jupiter_3("", "john.pham92", "")
    #SeleniumConfig().jupiter_4(5, 10)
