from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium_operations import SeleniumHelperPage


class InfosysHomePage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    _supplier_create = (By.ID, "create-btn")
    _supplier_create_po = (By.CSS_SELECTOR, "#createPOInvoice span")
    _supplier_edit_filter_arrow = (
    By.CSS_SELECTOR, "i.sap-icon.filter-arrow-icon.icon-navigation-down-arrow.blue-arrow-down")
    _supplier_search_filter_expand = (By.ID, "edit-filter")
    _suppler_exact_number_radio = (By.CSS_SELECTOR, "input[name='exact']")
    _supplier_po_number_text = (By.XPATH, "//div/div/fd-tokenizer/div/div/input")
    _supplier_po_clear_button = (By.CSS_SELECTOR, 'span.fd-token__close')
    _supplier_search_button = (By.ID, "filter-apply-button")
    _supplier_results_count = (By.CSS_SELECTOR, ".tile-count")

    # ----------------------PAGE OBJECTS-------------------------------------

    def navigate_to_create_po_invoice(self):
        """
        method to navigate to create po invoice from home page
        :return: true if navigated successfully, else false
        """
        try:
            self.wait_for_element(self._supplier_create)
            # check if create button was displayed on home page
            self.is_element_visible(self._supplier_create)
            # click on create button on home page
            self.click(*self._supplier_create)
            # check if PO Invoice option was displayed under Create
            self.is_element_visible(self._supplier_create_po)
            # click on the PO Invoice option
            self.click(*self._supplier_create_po)
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_search_filter_expand)
            # time.sleep(2)
            # check if search filter expand button was displayed
            if self.find_element(self._supplier_search_filter_expand):
                return True
            else:
                return False
        except Exception as e:
            self.log.error("Error {} occurred when navigating to Create PO Invoice infosys arbia web portal".format(e))
            return False

    def expand_search_filter(self):
        """
        method to expand the search filter
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_search_filter_expand)
            try:
                if self.driver.find_element(*self._supplier_edit_filter_arrow).is_displayed():
                    return True
            except NoSuchElementException:
                # expand search filter
                self.click(*self._supplier_search_filter_expand)
                self.wait_for_page_load()
                return True
        except Exception as e:
            self.log.error("Error {} occurred when expanding the search filter on infosys arbia web portal".format(e))
            return False

    def search_by_po_number(self, po_number):
        """
        method to search by PO number on the PO Invoice Page
        :param po_number:
        :return: true is results found , else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._suppler_exact_number_radio)
            action = ActionChains(self.driver)
            # check if exact number radio button was displayed
            self.is_element_visible(self._suppler_exact_number_radio)
            # click on the exact number radio button
            # self.click(*self._suppler_exact_number_radio)
            action.move_to_element(self.driver.find_element(*self._suppler_exact_number_radio))
            action.click(self.driver.find_element(*self._suppler_exact_number_radio)).perform()
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_po_number_text)
            # check if po number text field was displayed
            self.is_element_visible(self._supplier_po_number_text)
            # click, clear and enter PO number in the PO number text field
            self.click(*self._supplier_po_number_text)
            # unable to clear text due to new changes in the application - 12/Oct/2022
            # self.clear_text(*self._supplier_po_number_text)
            for _ in range(2):
                self.driver.find_element(*self._supplier_po_number_text).send_keys(Keys.CONTROL, 'a')
                self.driver.find_element(*self._supplier_po_number_text).send_keys(Keys.BACKSPACE)
            # if self.driver.find_element(*self._supplier_po_clear_button).is_displayed():
            #     self.driver.find_element(*self._supplier_po_clear_button).click()
            self.set_text(po_number, *self._supplier_po_number_text)
            # check if search button was displayed
            self.is_element_visible(self._supplier_search_button)
            # click on the search button
            self.click(*self._supplier_search_button)
            self.wait_for_page_load()
            # refresh is needed as the page loaded is delayed - added on 11/Oct/2022
            self.driver.refresh()
            self.wait_for_page_load()
            # time.sleep(2)
            self.wait_for_element(self._supplier_results_count)
            # check if results count element was displayed
            self.is_element_visible(self._supplier_results_count)
            # get text of the count element
            count_text = self.driver.find_element(*self._supplier_results_count).text
            count = ''.join([n for n in count_text if n.isdigit()])
            self.log.info("{} number of records found via search results".format(count))
            if int(count) != 0:
                return True
            else:
                return False
        except Exception as e:
            self.log.error("Error {} occurred when search for PO on infosys arbia web portal".format(e))
            return False
