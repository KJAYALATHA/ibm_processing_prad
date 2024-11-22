import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium_operations import SeleniumHelperPage


class InfosysLoginPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    _supplier_user_name_text = (By.NAME, "UserName")
    _supplier_password_text = (By.NAME, "Password")
    _supplier_submit_button = (By.CSS_SELECTOR, "input[value='Login']")
    _supplier_error_label = (By.CSS_SELECTOR, "span.sawa-LFE-span")
    _supplier_supplier_link = (By.LINK_TEXT, "Supplier")

    # ----------------------PAGE OBJECTS-------------------------------------
    def login_to_arbia(self, email, pwd):
        """
        method to login into infosys arbia web portal
        :param email: supplier email address
        :param pwd: supplier password
        :return: True if successfully, else False
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_supplier_link)
            # check if Supplier link was displayed
            self.is_element_visible(self._supplier_supplier_link)
            # click Supplier link
            self.click(*self._supplier_supplier_link)
            # check if user name field was displayed
            self.is_element_visible(self._supplier_user_name_text)
            # click and enter user name
            self.click(*self._supplier_user_name_text)
            self.set_text(email, *self._supplier_user_name_text)
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_password_text)
            # check if password field was displayed
            self.is_element_visible(self._supplier_password_text)
            # click, clear and enter password
            self.click(*self._supplier_password_text)
            self.clear_text(*self._supplier_password_text)
            self.set_text(pwd, *self._supplier_password_text, flag=True)
            # check if submit button was displayed
            self.is_element_visible(self._supplier_submit_button)
            # click on submit button
            self.click(*self._supplier_submit_button)
            self.wait_for_page_load()
            # to handle the condition and set the return flag
            try:
                if self.driver.find_element(*self._supplier_error_label):
                    self.log.error("Failed to login into infosys arbia web portal by user id : {}".format(email))
                    return False
            except NoSuchElementException:
                self.log.info("{} : user logged into infosys arbia web portal successfully".format(email))
                return True
        except Exception as e:
            self.log.error("Error {} occurred when logging into infosys arbia web portal".format(e))
            return False
