import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium_operations import SeleniumHelperPage


class InfosysInvoiceSubmittedPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    _supplier_submitted_label = (By.CSS_SELECTOR, "h2")
    _supplier_exit_link = (By.LINK_TEXT, "Exit")

    # ----------------------PAGE OBJECTS-------------------------------------

    def verify_invoice_submitted(self, invoice_number):
        """
        method to verify if the submit confirmation message was displayed for invoice number
        :param invoice_number:
        :return:
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_submitted_label)
            # check if the submitted messaged element was displayed
            self.is_element_visible(self._supplier_submitted_label)
            text = self.get_text(*self._supplier_submitted_label)
            if invoice_number in text:
                self.log.info("Invoice Number {} was submitted successfully".format(invoice_number))
                return True
            else:
                self.log.error("Failed to submit the Invoice Number {} ".format(invoice_number))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when invoice was submitted on infosys arbia web portal".format(e))
            return False

    def exit_invoice_submission(self):
        """
        method to exit the invoice submitted page
        :return:
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_exit_link)
            # check if the exit link was displayed
            self.is_element_visible(self._supplier_exit_link)
            # click on the exit link
            self.click(*self._supplier_exit_link)
            self.wait_for_page_load()
            # time.sleep(10)
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when exiting from invoice submitted page on infosys arbia web portal".format(e))
            return False
