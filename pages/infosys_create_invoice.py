import math
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from date_time_operations import get_formatted_date
from selenium_operations import SeleniumHelperPage


class InfosysCreateInvoicePage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    _supplier_invoice_number_text = (By.XPATH, "//input")
    _supplier_invoice_date = (By.XPATH, "//div/input")
    _supplier_sub_total_label = (By.XPATH, "//td[2]/table/tbody/tr/td[2]/span/nobr")
    _supplier_tax_total_label = (By.XPATH, "//tr[2]/td[2]/span/nobr")
    _supplier_total_label = (By.XPATH, "//td[2]/table/tbody/tr[3]/td[2]/span/nobr")
    # ------------------Additional Fields------------------------------------
    _supplier_customer_vat_label = (By.XPATH, "//tr[18]/td/table/tbody/tr[2]/td[2]/input")
    # ------------------Additional India Specific Information----------------
    _supplier_place_of_supply = (By.XPATH, "//td[2]/table/tbody/tr/td[2]/div/div/span")
    _supplier_place_of_supply_options = (By.CSS_SELECTOR, ".w-dropdown-items")
    _supplier_sez_dropdown = (By.XPATH, "//td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/div/div")
    _supplier_sez_option = (By.XPATH, "//tr[21]/td/table/tbody")
    _supplier_lut_number_text = (By.XPATH, "//tr[21]/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input")
    _supplier_lut_date = (By.XPATH, "//td[2]/nobr/div[2]/div/input")
    _supplier_pan_label = (By.XPATH, "//tr[5]/td/table/tbody/tr/td[2]/input")
    _supplier_customer_pan_number_label = (By.XPATH, "//tr[21]/td/table/tbody/tr[6]/td[2]")
    _supplier_gstin_label = (By.XPATH, "//tr[8]/td[2]/input")
    _supplier_customer_gstin_text = (By.XPATH, "//tr[9]/td[2]/input")
    _supplier_invoice_reference_text = (By.XPATH, "//tr[22]/td/table/tbody/tr[2]/td[2]/input")
    _supplier_add_header_dropdown = (By.XPATH, "//tr[24]/td/table/tbody/tr/td/div/button/span")
    _supplier_add_attachment_link = (By.XPATH, "(//a[contains(text(),'Attachment')])[2]")
    _supplier_choose_file_button = (By.CSS_SELECTOR, ".w-file-upload > input")
    _supplier_add_attachment_button = (By.XPATH, "//tr[2]/td/button/span")
    _supplier_attachment_file_label = (By.XPATH, "//tr[37]/td/table/tbody/tr[2]/td[2]")
    # ------------------------Line Items-------------------------------------
    _supplier_row_checkbox = (By.CSS_SELECTOR, ".tableBodyClass > .w-chk")
    _supplier_hsn_number_label = (By.XPATH, "//tr[2]/td/table/tbody/tr/td[2]/input")
    _supplier_code_text = (By.XPATH, "//td[2]/table/tbody/tr/td[2]/input")
    _supplier_line_item_action_dropdown = (By.XPATH, "//div[2]/table/tbody/tr/td/div/button/span")
    _supplier_line_add_tax_option = (By.XPATH, "(//a[contains(text(),'Tax')])[4]")
    _supplier_tax_category1_dropdown = (
        By.XPATH, "//td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td/a/div/input")
    _supplier_cgst_option = (By.XPATH, "(//a[contains(text(),'Central GST')])[3]")
    _supplier_sgst_option = (By.XPATH, "(//a[contains(text(),'State GST')])[3]")
    _supplier_igst_option = (By.XPATH, "(//a[contains(text(),'Integrated GST')])[3]")
    _supplier_rate1_text = (By.XPATH, "//td[2]/table/tbody/tr[2]/td[2]/input")
    _supplier_tax_amount1_label = (By.XPATH, "//tr[3]/td[2]/input")
    _supplier_tax_category2_dropdown = (By.XPATH, "//tr[5]/td/table/tbody/tr/td[2]/div/table/tbody/tr/td/a/div/input")
    _supplier_rate2_text = (By.XPATH, "//tr[5]/td[2]/table/tbody/tr[2]/td[2]/input")
    _supplier_tax_amount2_label = (By.XPATH, "//tr[5]/td[2]/table/tbody/tr[3]/td[2]/input")
    # -----------Footer Button------------------------------------------------
    _supplier_next_button = (By.XPATH, "//td[2]/div/table/tbody/tr/td[4]/button")

    # ----------------------PAGE OBJECTS-------------------------------------

    def enter_invoice_details(self, invoice_number, invoice_date):
        """
        method to enter the invoice details in the create invoice page
        :param invoice_number: invoice number provided in the merged PDF file
        :param invoice_date: formatted invoice date provided in the merged PDF file
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_invoice_number_text)
            # format invoice date
            invoice_date = get_formatted_date(invoice_date, "%d %b %Y")  # <-- formatted to 23 Mar 2022
            # check invoice number field was displayed and enter invoice number
            self.is_element_visible(self._supplier_invoice_number_text)
            self.clear_text(*self._supplier_invoice_number_text)
            self.set_text(invoice_number, *self._supplier_invoice_number_text)
            # check invoice date field was displayed and enter the date
            self.is_element_visible(self._supplier_invoice_date)
            self.clear_text(*self._supplier_invoice_date)
            self.set_text(invoice_date, *self._supplier_invoice_date)
            self.log.info(
                "{} : invoice number and {} invoice date was successfully entered in infosys arbia web portal successfully".format(
                    invoice_number, invoice_date))
            return True
        except NoSuchElementException as e:
            self.log.error("Error {} occurred when entering invoice details in infosys arbia web portal".format(e))
            return False

    def get_amount_summary(self):
        """
        method to get the sub-total, tax-total and total amount from create invoice page
        :return: sub-total, tax-total, total if successful, else None
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_sub_total_label)
            # check if sub-total value was displayed
            self.is_element_visible(self._supplier_sub_total_label)
            sub_total = self.get_text(*self._supplier_sub_total_label)
            # check if tax amount value was displayed
            self.is_element_visible(self._supplier_tax_total_label)
            tax_total = self.get_text(*self._supplier_tax_total_label)
            # check if tax amount value was displayed
            self.is_element_visible(self._supplier_total_label)
            total = self.get_text(*self._supplier_total_label)
            return sub_total, tax_total, total
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when fetching the amount summary from create invoice page in infosys arbia web portal".format(
                    e))
            return None

    def check_customer_vat_number_and_correct(self, customer_vat):
        """
        method to check customer vat number from create invoice number page and correct to match with pdf file
        :param customer_vat: string customer vat parsed value from pdf file
        :return: customer_vat if successful, else None
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_customer_vat_label)
            # check if customer vat value was displayed
            self.is_element_visible(self._supplier_customer_vat_label)
            displayed_customer_vat = self.get_text(*self._supplier_customer_vat_label)
            if displayed_customer_vat != customer_vat:
                self.set_text(customer_vat, *self._supplier_customer_vat_label)
                self.log.info("Customer vat displayed was corrected from {} to {} to match PDF value".format(
                    displayed_customer_vat, customer_vat))
                return True
            else:
                self.log.info("Customer vat number displayed was matching with PDF value")
                return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when fetching the customer vat number from create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def select_place_of_supply(self, state_name):
        """
        method to select a place of supply based on merged pdf input
        :param state_name: string state name
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_place_of_supply)
            # check if place of supply field was displayed
            self.is_element_visible(self._supplier_place_of_supply)
            # click play of supply
            self.click(*self._supplier_place_of_supply)
            time.sleep(2)
            # click and select the state based on merged PDF place of supply
            items = self.driver.find_elements(*self._supplier_place_of_supply_options)
            state_names = items[3].find_elements(By.CSS_SELECTOR, "div.w-dropdown-item")
            for i, item in enumerate(state_names):
                # there are states with two words separated by space
                if state_name.lower() in state_names[i].text.lower().split("[")[0].strip(" ").replace(" ", ""):
                    state_names[i].click()
                    self.wait_for_page_load()
                    self.log.info("Selected the option {} from the place of supply dropdown".format(state_name))
                    return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when selecting the place of supply from create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def sez_selection(self, sez_option):
        """
        method to select sez if ship to address in merged pdf contains SEZ
        :param sez_option: PDF parsed value from ship to address
        :return: true if SEZ or no SEZ, else false
        """
        try:
            option = None
            # check from merged PDF if the address has SEZ in it
            if sez_option == "SEZ":
                self.wait_for_page_load()
                self.wait_for_element(self._supplier_sez_dropdown)
                # check if the sez tax dropdown was displayed
                self.is_element_visible(self._supplier_sez_dropdown)
                # click on sez dropdown and select 2nd sez option
                self.click(*self._supplier_sez_dropdown)
                # check if the 2nd sez option was displayed
                items = self.driver.find_elements(*self._supplier_place_of_supply_options)
                sez_options = items[2].find_elements(By.CSS_SELECTOR, "div.w-dropdown-item")
                for i, item in enumerate(sez_options):
                    option = sez_options[i].text.lower()
                    if "without payment of integrated tax" in option:
                        sez_options[i].click()
                        self.wait_for_page_load()
                        self.log.info("Selected the option {} from the sez dropdown".format(option))
                        return True
                self.log.info("Selected the option {} from the SEZ dropdown".format(option))
                return True
            else:
                self.log.info("Not SEZ")
                return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when selecting the sez from create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def enter_lut_number_and_date(self, lut_number, lut_date):
        """
        method to enter lut number and lut date as applicable based on the merged PDF input
        :param lut_number: string lut number parsed from merged pdf file
        :param lut_date: string formatted data from the merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_lut_number_text)
            # format invoice date
            lut_date = get_formatted_date(lut_date, "%d %b %Y")  # <-- formatted to 23 Mar 2022
            # check if lut number field was displayed
            self.is_element_visible(self._supplier_lut_number_text)
            # clear any existing values
            self.clear_text(*self._supplier_lut_number_text)
            # enter lut number for merged PDF file
            self.set_text(lut_number, *self._supplier_lut_number_text)
            self.log.info("Entered LUT number {}".format(lut_number))
            result = True
            # check from merged PDF if lut date / date of filing has been provided
            if lut_date is not None:
                # check if LUT date field was displayed
                self.is_element_visible(self._supplier_lut_date)
                # clear any existing date
                self.clear_text(*self._supplier_lut_date)
                # set the date from merged PDF file
                self.set_text(lut_date, *self._supplier_lut_date)
                self.log.info("Entered the LUT date as {}".format(lut_date))
                result &= True
            else:
                self.log.info("No Date of Filing provided in the merged PDF file")
            return result
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when entering lut number and lut date in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def check_and_correct_supplier_pan(self, supplier_pan):
        """displayed_supplier_pan
        method to check and validate the supplier pan
        :param supplier_pan: supplier pan string as parsed from merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_element(self._supplier_pan_label)
            # check if the supplier pan field was displayed
            self.is_element_visible(self._supplier_pan_label)
            # get the value and validate it matches with PDF value
            displayed_supplier_pan = self.get_attribute_value("value", self._supplier_pan_label)
            if displayed_supplier_pan != supplier_pan:
                self.set_text(supplier_pan, *self._supplier_pan_label)
                self.log.info("Supplier pan displayed was corrected from {} to {} to match PDF value".format(
                    displayed_supplier_pan, supplier_pan))
                return True
            else:
                self.log.info("Supplier pan displayed was matching with PDF value")
                return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when correcting supplier pan in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def check_customer_pan(self, customer_pan):
        """
        method to check and validate the customer pan
        :param customer_pan: customer pan string as parsed from merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_element(self._supplier_customer_pan_number_label)
            # check if the customer pan field was displayed
            self.is_element_visible(self._supplier_customer_pan_number_label)
            # get the value and validate it matches with PDF value
            displayed_customer_pan = self.get_text(*self._supplier_customer_pan_number_label)
            if displayed_customer_pan != customer_pan:
                self.log.info("Customer pan displayed was corrected from {} to {} to match PDF value".format(
                    displayed_customer_pan, customer_pan))
                return True
            else:
                self.log.info("Customer pan displayed was matching with PDF value")
                return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when correcting customer pan in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def check_and_correct_supplier_gstin(self, supplier_gstin):
        """
        method to check and validate the supplier gstin
        :param supplier_gstin: supplier gstin string as parsed from merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_element(self._supplier_gstin_label)
            # check if the supplier gstin field was displayed
            self.is_element_visible(self._supplier_gstin_label)
            # get the value and validate it matches with PDF value
            displayed_supplier_gstin = self.get_attribute_value("value", self._supplier_gstin_label)
            if displayed_supplier_gstin != supplier_gstin:
                self.set_text(supplier_gstin, *self._supplier_gstin_label)
                self.log.info("Supplier gstin displayed was corrected from {} to {} to match PDF value".format(
                    displayed_supplier_gstin, supplier_gstin))
                return True
            else:
                self.log.info("Supplier gstin displayed was matching with PDF value")
                return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when correcting supplier gstin in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def enter_customer_gstin(self, customer_gstin):
        """
        method to enter customer gstin
        :param customer_gstin: customer gstin string as parsed from merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_customer_gstin_text)
            # check if the customer pan field was displayed
            self.is_element_visible(self._supplier_customer_gstin_text)
            self.set_text(customer_gstin, *self._supplier_customer_gstin_text)
            self.log.info("Customer gstin entered was {} from PDF value".format(customer_gstin))
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when entering customer gstin in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def enter_invoice_reference_number(self, invoice_number):
        """
        method to enter customer gstin
        :param invoice_number: invoice number string as parsed from merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_element(self._supplier_invoice_reference_text)
            # check if the invoice reference number field was displayed
            self.is_element_visible(self._supplier_invoice_reference_text)
            self.set_text(invoice_number, *self._supplier_invoice_reference_text)
            self.log.info("Invoice number entered was {} from PDF value".format(invoice_number))
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when entering invoice reference number in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def add_attachment(self, full_file_name):
        """
        method to add header and select attachment and add attachment
        :param full_file_name: fully file path with file extension to attach
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_add_header_dropdown)
            # check if add header dropdown was displayed
            self.is_element_visible(self._supplier_add_header_dropdown)
            # click on the add header drop down
            self.click(*self._supplier_add_header_dropdown)
            # check if the attachment option was displayed
            self.is_element_visible(self._supplier_add_attachment_link)
            # click on the attachment link
            self.click(*self._supplier_add_attachment_link)
            self.wait_for_page_load()
            # time.sleep(2)
            # check if the choose file button was displayed
            self.is_element_visible(self._supplier_choose_file_button)
            # Attach File
            element = self.find_element(self._supplier_choose_file_button)
            element.send_keys(full_file_name)
            # check if add attachment button was displayed
            self.is_element_visible(self._supplier_add_attachment_button)
            # click on the add attachment button
            self.click(*self._supplier_add_attachment_button)
            # check if the attachment is completed
            # time.sleep(10)
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_attachment_file_label)
            self.is_element_visible(self._supplier_attachment_file_label)
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when adding attachment in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def check_and_correct_hsn_number(self, hsn_number):
        """
        method to check and validate the hsn number
        :param hsn_number: hsn number string as parsed from merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_hsn_number_label)
            # check if the hsn number field was displayed
            self.is_element_visible(self._supplier_hsn_number_label)
            # get the value and validate it matches with PDF value
            displayed_hsn_number = self.get_text(*self._supplier_hsn_number_label)
            if displayed_hsn_number != hsn_number:
                self.clear_text(*self._supplier_hsn_number_label)
                self.set_text(hsn_number, *self._supplier_hsn_number_label)
                self.log.info("HSN number displayed was corrected from {} to {} to match PDF value".format(
                    displayed_hsn_number, hsn_number))
                return True
            else:
                self.log.info("HSN number displayed was matching with PDF value")
                return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when correcting hsn number in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def enter_domain_code(self, hsn_number):
        """
        method to enter domain code i.e. hsn number
        :param hsn_number: hsn number string as parsed from merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_element(self._supplier_code_text)
            # check if the hsn code number field was displayed
            self.is_element_visible(self._supplier_code_text)
            self.set_text(hsn_number, *self._supplier_code_text)
            self.log.info("HSN number entered was {} from PDF value".format(hsn_number))
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when entering code number in create invoice page in infosys arbia web portal".format(
                    e))
            return False

    def enter_india_specific_info(self, *args):
        """
        method to enter india specific details
        :param args: input arguments from parsed merged pdf file
        :return: true if successful, else false
        """
        try:
            # select place of supply
            result = self.select_place_of_supply(args[0])
            # time.sleep(1)
            # select sez option for tax if sez is true
            result &= self.sez_selection(args[1])
            # enter lut number and date as applicable
            if args[1] == "SEZ":
                result &= self.enter_lut_number_and_date(args[2], args[3])
            # check supplier pan number and correct if necessary
            self.check_and_correct_supplier_pan(args[4])
            # check customer pan and correct if necessary
            self.check_customer_pan(args[5])
            # check supplier gstin and correct if necessary
            self.check_and_correct_supplier_gstin(args[6])
            # time.sleep(3)
            # enter customer gstin from pdf file
            self.enter_customer_gstin(args[7])
            # enter invoice reference number
            self.enter_invoice_reference_number(args[8])
            # add attachment
            self.add_attachment(args[9])
            return result
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when entering India specific values in create invoice page".format(e))
            return False

    def add_tax_lines(self, tax_type):
        """
        method to add tax lines if the tax amount is not zero from the parsed merged pdf file
        :return: true if successful, else false
        """
        try:
            if tax_type != "IGST":
                i = 0
                # since we need to add two tax line items for CGST, SGST
                for _ in range(2):
                    # check if the row checkbox was displayed
                    self.is_element_visible(self._supplier_row_checkbox)
                    # click on the row checkbox
                    self.click(*self._supplier_row_checkbox)
                    # time.sleep(2)
                    self.wait_for_page_load()
                    self.wait_for_element(self._supplier_line_item_action_dropdown)
                    # check if line item field was displayed
                    self.is_element_visible(self._supplier_line_item_action_dropdown)
                    # click line item field and select add tax
                    self.click(*self._supplier_line_item_action_dropdown)
                    self.wait_for_page_load()
                    # time.sleep(1)
                    if i == 1:
                        self.wait_for_element((By.XPATH, "(//a[contains(text(),'Tax')])[7]"))
                        ele = self.driver.find_element(By.XPATH, "(//a[contains(text(),'Tax')])[7]")
                        ele.click()
                    else:
                        self.wait_for_element(self._supplier_line_add_tax_option)
                        # check if the tax option was displayed
                        self.is_element_visible(self._supplier_line_add_tax_option)
                        # click on the tax option
                        self.click(*self._supplier_line_add_tax_option)
                    self.wait_for_page_load()
                    # time.sleep(10)
                    i = i + 1
            elif tax_type == "IGST":
                self.wait_for_page_load()
                self.wait_for_element(self._supplier_row_checkbox)
                # check if the row checkbox was displayed
                self.is_element_visible(self._supplier_row_checkbox)
                # click on the row checkbox
                self.click(*self._supplier_row_checkbox)
                # time.sleep(2)
                self.wait_for_page_load()
                self.wait_for_element(self._supplier_line_item_action_dropdown)
                # check if line item field was displayed
                self.is_element_visible(self._supplier_line_item_action_dropdown)
                # click line item field and select add tax
                self.click(*self._supplier_line_item_action_dropdown)
                # check if the tax option was displayed
                self.is_element_visible(self._supplier_line_add_tax_option)
                # click on the tax option
                self.click(*self._supplier_line_add_tax_option)
                self.wait_for_page_load()
                # time.sleep(10)
            self.log.info("Selected the option 'Add Tax' from the line item actions dropdown")
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when adding tax lines in create invoice page".format(e))
            return False

    def select_sgst_tax(self, tax_percentage):
        """
        method to select the sgst based on ship to and bill to address from the merged PDF file
        :param tax_percentage: tax percentage as parsed from the merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_tax_category1_dropdown)
            self.is_element_visible(self._supplier_tax_category1_dropdown)
            # click the tac category dropdown and select sgst
            self.click(*self._supplier_tax_category1_dropdown)
            time.sleep(1)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#taxcreator0  > div>a")
            # # check if the state gst option is displayed
            # self.is_element_visible(self._supplier_sgst_option)
            # # select the option
            # self.click(*self._supplier_sgst_option)
            for i in range(len(elements)):
                if elements[i].text.strip(" ") == "State GST":
                    elements[i].click()
                    self.wait_for_page_load()
                    break
            # time.sleep(10)
            self.log.info("Selected the option 'SGST' from the tax category dropdown")
            # check if the tax rate % field was displayed
            self.is_element_visible(self._supplier_rate1_text)
            # clear any data displayed
            self.clear_text(*self._supplier_rate1_text)
            # enter % tax rate since ship to and bill to are from same location
            self.set_text(tax_percentage, *self._supplier_rate1_text)
            # time.sleep(2)
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_tax_amount1_label)
            # check if the tax amount was displayed
            self.is_element_visible(self._supplier_tax_amount1_label)
            self.click(*self._supplier_tax_amount1_label)
            self.wait_for_page_load()
            # time.sleep(5)
            # get the amount to check if not null
            displayed_tax_amount = self.driver.find_element(*self._supplier_tax_amount1_label).get_attribute("value")
            if len(displayed_tax_amount) > 0:
                self.log.info("Tax amount was displayed {}".format(displayed_tax_amount))
                return True
            else:
                self.log.info("Tax amount was not displayed")
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when adding SGST tax item in create invoice page".format(e))
            return False

    def select_cgst_tax(self, tax_percentage):
        """
         method to select the cgst based on ship to and bill to address from the merged PDF file
        :param tax_percentage: tax percentage as parsed from the merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_tax_category2_dropdown)
            self.is_element_visible(self._supplier_tax_category2_dropdown)
            # click the tac category dropdown and select sgst
            self.click(*self._supplier_tax_category2_dropdown)
            time.sleep(1)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#taxcreator1  > div>a")
            # check if the central gst option is displayed
            # self.is_element_visible(self._supplier_cgst_option)
            # select the option
            # self.click(*self._supplier_cgst_option)
            for i in range(len(elements)):
                if elements[i].text.strip(" ") == "Central GST":
                    elements[i].click()
                    self.wait_for_page_load()
                    break
            # time.sleep(10)
            self.log.info("Selected the option 'SGST' from the tax category dropdown")
            # check if the tax rate % field was displayed
            self.is_element_visible(self._supplier_rate2_text)
            # clear any data displayed
            self.clear_text(*self._supplier_rate2_text)
            # enter % tax rate since ship to and bill to are from same location
            self.set_text(tax_percentage, *self._supplier_rate2_text)
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_tax_amount2_label)
            # time.sleep(2)
            # check if the tax amount was displayed
            self.is_element_visible(self._supplier_tax_amount2_label)
            self.click(*self._supplier_tax_amount2_label)
            self.wait_for_page_load()
            # time.sleep(5)
            # get the amount to check if not null
            displayed_tax_amount = self.driver.find_element(*self._supplier_tax_amount2_label).get_attribute("value")
            if len(displayed_tax_amount) > 0:
                self.log.info("Tax amount was displayed {}".format(displayed_tax_amount))
                return True
            else:
                self.log.info("Tax amount was not displayed")
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when adding CGST tax item in create invoice page".format(e))
            return False

    def select_igst_tax(self, tax_percentage):
        """
        method to select the igst based on ship to and bill to address from the merged PDF file
        :param tax_percentage: tax percentage as parsed from the merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_tax_category1_dropdown)
            self.is_element_visible(self._supplier_tax_category1_dropdown)
            # click the tac category dropdown and select sgst
            self.click(*self._supplier_tax_category1_dropdown)
            time.sleep(1)
            elements = self.driver.find_elements(By.CSS_SELECTOR, "#taxcreator0  > div>a")
            # check if the integrated gst option is displayed
            # self.is_element_visible(self._supplier_igst_option)
            # select the option
            # self.click(*self._supplier_igst_option)
            for i in range(len(elements)):
                if elements[i].text.strip(" ") == "Integrated GST":
                    elements[i].click()
                    self.wait_for_page_load()
                    break
            # time.sleep(10)
            self.log.info("Selected the option 'Integrated GST' from the tax category dropdown")
            # check if the tax rate % field was displayed
            self.is_element_visible(self._supplier_rate1_text)
            # clear any data displayed
            self.clear_text(*self._supplier_rate1_text)
            # enter % tax rate since ship to and bill to are from same location
            self.set_text(tax_percentage, *self._supplier_rate1_text)
            # time.sleep(2)
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_tax_amount1_label)
            # check if the tax amount was displayed
            self.is_element_visible(self._supplier_tax_amount1_label)
            self.click(*self._supplier_tax_amount1_label)
            self.wait_for_page_load()
            # time.sleep(5)
            # get the amount to check if not null
            displayed_tax_amount = self.driver.find_element(*self._supplier_tax_amount1_label).get_attribute("value")
            if len(displayed_tax_amount) > 0:
                self.log.info("Tax amount was displayed {}".format(displayed_tax_amount))
                return True
            else:
                self.log.info("Tax amount was not displayed")
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when adding IGST tax item in create invoice page".format(e))
            return False

    def complete_line_items(self, *args):
        """
        method to complete the line item details on create invoice page
        :param args: input arguments from parsed merged pdf file
        :return: true if successful, else false
        """
        try:
            # check hsn number and correct as necessary
            self.check_and_correct_hsn_number(args[0])
            # enter domain code
            self.enter_domain_code(args[0])
            # add tax line items only if tax rate is non zero
            tax_value = int(float(args[1]))
            # check if tax % is not 0 and not sez and not IGST
            if tax_value != 0 and args[2] != "SEZ" and args[3] != "IGST":
                # add tax line items as required
                self.add_tax_lines(args[3])
                # add sgst line item
                self.select_sgst_tax(args[1])
                # add cgst line item
                self.select_cgst_tax(args[1])
                self.log.info(
                    "Selected {} option for tax line items".format(args[1]))
                return True
            # check if tax % is not 0 and IGST
            elif tax_value != 0 and args[2] != "SEZ" and args[3] == "IGST":
                # add tax line item
                self.add_tax_lines(args[3])
                # add igst line item
                self.select_igst_tax(args[1])
                self.log.info(
                    "Selected {} option for tax line item".format(args[2]))
                return True
            else:
                self.log.info(
                    "Since it was {} , hence no tax lines items needed".format(args[2]))
                return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when completing line item in create invoice page".format(e))
            return False

    def navigate_to_review(self):
        """
        method to navigate to final review page on infosys web portal
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_next_button)
            # check if the next button was displayed
            self.is_element_visible(self._supplier_next_button)
            # click on the next button
            self.click(*self._supplier_next_button)
            self.wait_for_page_load()
            # time.sleep(5)
            self.log.info(" Successfully navigated to final review page")
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when navigating to final review page in Infosys Web Portal".format(e))
            return False
