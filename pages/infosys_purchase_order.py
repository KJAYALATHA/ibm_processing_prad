from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium_operations import SeleniumHelperPage


class InfosysPurchaseOrderPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    _supplier_create_invoice = (By.XPATH, "//td[3]/div/button/span")
    _supplier_standard_invoice = (By.LINK_TEXT, "Standard Invoice")
    _supplier_done_button = (By.XPATH, "//button[contains(.,'Done')]")

    # ----------------------PAGE OBJECTS-------------------------------------

    def navigate_to_standard_invoice(self):
        """
        method to navigate to standard invoice
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_create_invoice)
            # check if create invoice button was displayed
            self.is_element_visible(self._supplier_create_invoice)
            # click on the create invoice button
            self.click(*self._supplier_create_invoice)
            self.wait_for_element(self._supplier_standard_invoice)
            # check if standard invoice option link was displayed
            self.is_element_visible(self._supplier_standard_invoice)
            # click standard invoice option link
            self.click(*self._supplier_standard_invoice)
            self.wait_for_page_load()
            # time.sleep(5)
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when navigating to standard invoice page on infosys arbia web portal".format(e))
            return False

    def complete_invoice_creation(self):
        """
        method to click on done button and complete the invoice creation process
        :return:
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_done_button)
            # check if done button was displayed
            self.is_element_visible(self._supplier_done_button)
            # click on the done button
            self.click(*self._supplier_done_button)
            self.wait_for_page_load()
            self.driver.refresh()
            self.wait_for_page_load()
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when completing the invoice complete on infosys arbia web portal".format(e))
            return False
