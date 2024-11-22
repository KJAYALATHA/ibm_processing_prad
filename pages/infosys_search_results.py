from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium_operations import SeleniumHelperPage


class InfosysSearchResultsPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    _supplier_order_rows = (By.CSS_SELECTOR, "table > tbody > tr")

    # ----------------------PAGE OBJECTS-------------------------------------

    def select_order_number(self):
        """
        method to select the order number based on status
        :return: true if successfully selected, else false
        """
        try:
            # get number of rows in the table
            rows = self.driver.find_elements(*self._supplier_order_rows)
            # loop through the table ignoring the header rows
            for row in rows:
                # check if order status is not Obsoleted and revision status = Original
                status = row.find_element(By.CSS_SELECTOR, "td[class$='cdk-column-orderStatus']").text
                if status != "Obsoleted":
                    # and rows[i].find_element(By.CSS_SELECTOR, "td:nth-child(13)").text != "Original"
                    # select the row -- Changed updated 11/Oct/2022 -- Row selection not available
                    # row.find_element(By.CSS_SELECTOR, "td[class$='cdk-column-orderNumber']").click()
                    # get the text of the order number
                    order_number = row.find_element(By.CSS_SELECTOR, "td[class$='cdk-column-orderNumber']").text
                    self.log.info(
                        "Selected Order Number {} on search results page with status as {}".format(order_number,
                                                                                                   status))
                    # click on the order number link
                    row.find_element(By.CSS_SELECTOR, "td[class$='cdk-column-orderNumber']").find_element(By.TAG_NAME,
                                                                                                          'a').click()
                    self.wait_for_page_load()
                    self.log.info("Selected order number : {} with status as {} ".format(order_number, status))
                    return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when selecting order number in the search results page "
                "of infosys arbia web portal".format(e))
            return False
