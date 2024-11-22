import math
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from date_time_operations import get_formatted_date
from selenium_operations import SeleniumHelperPage


class InfosysReceiptsPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    _supplier_page_title = (By.CSS_SELECTOR, "table > tbody > tr > td > h2")
    _supplier_receipts_table = (By.CSS_SELECTOR, "table.tableBody tbody")
    _supplier_next_button = (By.XPATH, "//button/span")

    # ----------------------PAGE OBJECTS-------------------------------------

    def select_grn_number(self, grn_number):
        """
        method to select the grn receipt from the description of parsed merged pdf file
        :param grn_number:
        :return: true if successful, else false
        """
        # check if grn number is empty, else proceed selecting grn number
        # check if table was displayed else exit this function with true saying page wasn't applicable for PO
        # check title element was displayed
        try:
            self.wait_for_page_load()
            if not self.driver.find_element(*self._supplier_page_title):
                self.log.info("Receipts page was not applicable for PO number on infosys arbia web portal")
                return True
        except NoSuchElementException:
            self.log.info(
                "Receipts page was not applicable for PO number on infosys arbia web portal")
            return True
        try:
            self.log.info("Receipts page was applicable for PO number on infosys arbia web portal")
            self.wait_for_element(self._supplier_receipts_table)
            self.is_element_visible(self._supplier_receipts_table)
            table = self.driver.find_element(*self._supplier_receipts_table)
            rows = table.find_elements(By.TAG_NAME, "tr")
            flag = False
            for i, row in enumerate(rows):
                columns = rows[i].find_elements(By.TAG_NAME, "td")
                for j, column in enumerate(columns):
                    disp_grn_number = rows[i].find_elements(By.TAG_NAME, "td")[j].text
                    if disp_grn_number == str(grn_number):
                        # select the row
                        rows[i].find_elements(By.TAG_NAME, "td")[j - 1].click()
                        # check if the next button element was displayed
                        self.wait_for_element(self._supplier_next_button)
                        self.click(*self._supplier_next_button)
                        self.wait_for_page_load()
                        flag = True
                        return flag
            if flag:
                self.log.info("Selected the GRN Number : {} ".format(grn_number))
                return True
            else:
                self.log.error("Failed to find the GRN Number : {} in the receipts list ".format(grn_number))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when selecting GRN in Receipts page of infosys arbia web portal".format(e))
            return False
