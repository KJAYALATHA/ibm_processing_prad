import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from date_time_operations import get_formatted_date
from general_operations import format_amount
from selenium_operations import SeleniumHelperPage


class InfosysReviewPage(SeleniumHelperPage):
    # ----------------------PAGE OBJECT CONSTRUCTOR-------------------------
    def __init__(self, driver):
        """
        constructor for the class to initiate the page class driver
        :param driver:
        """
        SeleniumHelperPage.__init__(self, driver)
        self.driver = driver

    # ----------------------WEBELEMENT LOCATORS-----------------------------
    _supplier_invoice_number_label = (By.XPATH, "//div/div/table/tbody/tr/td[2]")
    _supplier_po_number_label = (By.XPATH, "//tr[3]/td[2]")
    _supplier_subtotal_amount_label = (By.XPATH, "//td[2]/div")
    _supplier_tax_amount_label = (By.XPATH, "//tr[2]/td[2]/div")
    _supplier_total_amount_label = (By.XPATH, "//tr[3]/td[2]/div")
    _supplier_gstin_label = (By.XPATH, "//span/div[2]")
    _supplier_customer_gstin_label = (By.XPATH, "//div[2]/span/div[2]")
    _supplier_pan_label = (By.XPATH, "//span[8]")
    _supplier_lut_number_label = (By.XPATH, "//span[10]")
    _supplier_customer_pan_number_label = (By.XPATH, "//span[14]")
    _supplier_lut_date_label = (By.XPATH, "//span[16]")
    _supplier_irn_number_label = (By.XPATH, "//span[20]")
    _supplier_customer_vat_id_label = (By.XPATH, "//tr[12]/td/div")  # <-- Check if entire text the value is present
    _supplier_attachment_label = (By.XPATH, "//tr[3]/td/table/tbody/tr[2]/td")
    _supplier_hsn_number_label = (By.XPATH, "//tr[5]/td/div[2]/div[2]")
    _supplier_hsn_code_label = (By.XPATH, "//div[3]/table/tbody/tr/td/table/tbody/tr/td[2]")
    _supplier_submit_button = (By.XPATH, "//td[2]/div/table/tbody/tr/td[3]/button")

    # ----------------------PAGE OBJECTS-------------------------------------

    def verify_invoice_number(self, invoice_number):
        """
        method to verify invoice number on review page
        :param invoice_number: invoice number from the parsed merged pdf file
        :return: true if successful, else false
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_invoice_number_label)
            # check if the invoice label was displayed
            self.is_element_visible(self._supplier_invoice_number_label)
            # get text of invoice number label
            inv_num = self.get_text(*self._supplier_invoice_number_label)
            if inv_num == invoice_number:
                self.log.info("Invoice Number {} was correctly displayed in review page".format(inv_num))
                return True
            else:
                self.log.error("Invoice Number {} was incorrectly displayed in review page".format(inv_num))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the invoice number on review page".format(e))
            return False

    def verify_po_number(self, purchase_order_number):
        """
        method to verify po number on review page
        :param purchase_order_number:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_po_number_label)
            # get text of invoice number label
            po_num = self.get_text(*self._supplier_po_number_label)
            if int(po_num) == purchase_order_number:
                self.log.info("PO Number {} was correctly displayed in review page".format(po_num))
                return True
            else:
                self.log.error("PO Number {} was incorrectly displayed in review page".format(po_num))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the po number on review page".format(e))
            return False

    def verify_subtotal_amount(self, sub_total_amt):
        """
        method to verify the sub-total amount on review page
        :param sub_total_amt:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_subtotal_amount_label)
            # get text of invoice number label
            sub_total = self.get_text(*self._supplier_subtotal_amount_label)
            sub_total = sub_total.replace(" INR", "")
            if float(format_amount(sub_total)) == float(sub_total_amt):
                self.log.info("Sub Total Amount {} was correctly displayed in review page".format(sub_total))
                return True
            else:
                self.log.error("Sub Total Amount {} was incorrectly displayed in review page".format(sub_total))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the sub total amount on review page".format(e))
            return False

    def verify_total_amount(self, total_amt):
        """
        method to verify the total amount on review page
        :param total_amt:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_total_amount_label)
            # get text of invoice number label
            total = self.get_text(*self._supplier_total_amount_label)
            total = total.replace(" INR", "")
            if float(format_amount(total)) == float(total_amt):
                self.log.info("Total Amount {} was correctly displayed in review page".format(total))
                return True
            else:
                self.log.error("Total Amount {} was incorrectly displayed in review page".format(total))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the total amount on review page".format(e))
            return False

    def verify_tax_amount(self, tax_amt, tax_type):
        """
        method to verify the tax amount on review page
        :param tax_type:
        :param tax_amt:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_tax_amount_label)
            # get text of invoice number label
            tax = self.get_text(*self._supplier_tax_amount_label)
            tax = tax.replace(" INR", "")
            # to handle the type of tax
            if tax_type != "CGST":
                if float(format_amount(tax)) == float(tax_amt):
                    self.log.info("Tax Amount {} was correctly displayed in review page".format(tax))
                    return True
                else:
                    self.log.error("Tax Amount {} was incorrectly displayed in review page".format(tax))
                    return False
            else:
                if float(format_amount(tax)) / 2 == float(tax_amt):
                    self.log.info("Tax Amount {} was correctly displayed in review page".format(tax))
                    return True
                else:
                    self.log.error("Tax Amount {} was incorrectly displayed in review page".format(tax))
                    return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the tax amount on review page".format(e))
            return False

    def verify_supplier_gstin_number(self, supplier_gstin_number):
        """
        method to verify the supplier gstin number on review page
        :param supplier_gstin_number:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_gstin_label)
            sup_gstin = self.get_text(*self._supplier_gstin_label)
            if supplier_gstin_number in sup_gstin:
                self.log.info(
                    "Supplier GSTIN  Number {} was correctly displayed in review page".format(supplier_gstin_number))
                return True
            else:
                self.log.error(
                    "Supplier GSTIN Number {} was incorrectly displayed in review page".format(supplier_gstin_number))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the supplier gstin number on review page".format(e))
            return False

    def verify_customer_gstin_number(self, customer_gstin_number):
        """
        method to verify customer gstin number on review page
        :param customer_gstin_number:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_customer_gstin_label)
            cus_gstin = self.get_text(*self._supplier_customer_gstin_label)
            if customer_gstin_number in cus_gstin:
                self.log.info(
                    "Customer GSTIN Number {} was correctly displayed in review page".format(customer_gstin_number))
                return True
            else:
                self.log.error(
                    "Customer GSTIN Number {} was incorrectly displayed in review page".format(customer_gstin_number))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the customer gstin number on review page".format(e))
            return False

    def verify_supplier_pan_number(self, supplier_pan_number):
        """
        method to verify supplier pan number on review page
        :param supplier_pan_number:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_pan_label)
            sup_pan = self.get_text(*self._supplier_pan_label)
            if sup_pan == supplier_pan_number:
                self.log.info("Supplier PAN Number {} was correctly displayed in review page".format(sup_pan))
                return True
            else:
                self.log.error("Supplier PAN Number {} was incorrectly displayed in review page".format(sup_pan))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the supplier pan number on review page".format(e))
            return False

    def verify_customer_pan_number(self, customer_pan_number):
        """
        method to verify customer pan number on review page
        :param customer_pan_number:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_customer_vat_id_label)
            cus_pan = self.get_text(*self._supplier_customer_vat_id_label)
            if customer_pan_number in cus_pan:
                self.log.info("Customer PAN Number {} was correctly displayed in review page".format(cus_pan))
                return True
            else:
                self.log.error("Customer PAN Number {} was incorrectly displayed in review page".format(cus_pan))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the customer pan number on review page".format(e))
            return False

    def verify_lut_number(self, lut_number):
        """
        method to verify lut number on the review page
        :param lut_number:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_lut_number_label)
            lut_num = self.get_text(*self._supplier_lut_number_label)
            if lut_num == lut_number or lut_num == "No":
                self.log.info("LUT Number {} was correctly displayed in review page".format(lut_num))
                return True
            else:
                self.log.error("LUT Number {} was incorrectly displayed in review page".format(lut_num))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the lut number on review page".format(e))
            return False

    def verify_lut_date(self, lut_dt):
        """
        method to verify lut date on review page
        :param lut_dt:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_customer_vat_id_label)
            lut_date = self.get_text(*self._supplier_customer_vat_id_label)
            if get_formatted_date(lut_dt, "%d %b %Y") in lut_date:
                self.log.info(
                    "LUT Date {} was correctly displayed in review page".format(get_formatted_date(lut_dt, "%d %b %Y")))
                return True
            else:
                self.log.error("LUT Date {} was incorrectly displayed in review page".format(
                    get_formatted_date(lut_dt, "%d %b %Y")))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the lut date on review page".format(e))
            return False

    def verify_irn_number(self, irn_num):
        """
        method to verify irn number on review page
        :param irn_num:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_customer_vat_id_label)
            irn = self.get_text(*self._supplier_customer_vat_id_label)
            if irn_num in irn:
                self.log.info("IRN Number {} was correctly displayed in review page".format(irn_num))
                return True
            else:
                self.log.error("IRN Number {} was incorrectly displayed in review page".format(irn_num))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the irn number on review page".format(e))
            return False

    def verify_customer_vat_number(self, cus_vat_num):
        """
        method to verify customer vat number on review page
        :param cus_vat_num:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_customer_vat_id_label)
            cus_vat = self.get_text(*self._supplier_customer_vat_id_label)
            if cus_vat_num in cus_vat:
                self.log.info("Customer VAT Number {} was correctly displayed in review page".format(cus_vat_num))
                return True
            else:
                self.log.error("Customer VAT Number {} was incorrectly displayed in review page".format(cus_vat_num))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the customer vat number on review page".format(e))
            return False

    def verify_place_of_supply(self, place):
        """
        method to verify the place of supply on review page
        :param place:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_customer_vat_id_label)
            cus_vat = self.get_text(*self._supplier_customer_vat_id_label)
            # checking first 4 characters of the state name exists in the text blob
            new_place = place[:4]
            if new_place.lower().title() in cus_vat:
                self.log.info("Place of supply {} was correctly displayed in review page".format(place))
                return True
            else:
                self.log.error("Place of supply {} was incorrectly displayed in review page".format(place))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the place of supply on review page".format(e))
            return False

    def verify_customer_hsn_number(self, cus_hsn_num):
        """
        method to verify hsn number on the review page
        :param cus_hsn_num:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_hsn_number_label)
            cus_hsn = self.get_text(*self._supplier_hsn_number_label)
            if cus_hsn == str(cus_hsn_num):
                self.log.info("Customer HSN Number {} was correctly displayed in review page".format(cus_hsn))
                return True
            else:
                self.log.error("Customer HSN Number {} was incorrectly displayed in review page".format(cus_hsn))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the customer hsn number on review page".format(e))
            return False

    def verify_customer_hsn_code(self, cus_hsn_num):
        """
        method to verify hsn code on review page
        :param cus_hsn_num:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_hsn_code_label)
            cus_hsn = self.get_text(*self._supplier_hsn_code_label)
            if cus_hsn == str(cus_hsn_num):
                self.log.info("Customer HSN Code {} was correctly displayed in review page".format(cus_hsn))
                return True
            else:
                self.log.error("Customer HSN Code {} was incorrectly displayed in review page".format(cus_hsn))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the customer hsn code on review page".format(e))
            return False

    def verify_attachment(self, file_name):
        """
        method to verify the attachment file name on the review page
        :param file_name:
        :return:
        """
        try:
            self.is_element_visible(self._supplier_attachment_label)
            att_name = self.get_text(*self._supplier_attachment_label)
            if att_name == file_name:
                self.log.info("Attachment {} was correctly displayed in review page".format(att_name))
                return True
            else:
                self.log.error("Attachment {} was incorrectly displayed in review page".format(att_name))
                return False
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when comparing the attachment file name on review page".format(e))
            return False

    def review_before_submit(self, *args):
        """
        integrated method to verify all the input values entered in creating invoice using the parsed merged pdf file
        :param args:
        :return:
        """

        result = self.verify_invoice_number(args[0])
        result &= self.verify_po_number(args[1])
        result &= self.verify_subtotal_amount(args[2])
        result &= self.verify_tax_amount(args[3], args[16])
        result &= self.verify_total_amount(args[4])
        result &= self.verify_supplier_gstin_number(args[5])
        result &= self.verify_customer_gstin_number(args[6])
        result &= self.verify_supplier_pan_number(args[7])
        # lut number an date exists only for SEZ
        if args[16] == "SEZ":
            result &= self.verify_lut_number(args[8])
            result &= self.verify_lut_date(args[9])
        result &= self.verify_customer_pan_number(args[10])
        result &= self.verify_irn_number(args[11])
        result &= self.verify_customer_vat_number(args[12])
        result &= self.verify_customer_hsn_number(args[13])
        result &= self.verify_customer_hsn_code(args[13])
        result &= self.verify_place_of_supply(args[14])
        result &= self.verify_attachment(args[15])
        return result

    def submit_invoice(self):
        """
        method to submit invoice
        :return:
        """
        try:
            self.wait_for_page_load()
            self.wait_for_element(self._supplier_submit_button)
            # check if the submit button was displayed
            self.is_element_visible(self._supplier_submit_button)
            # click on the submit button
            self.click(*self._supplier_submit_button)
            self.wait_for_page_load()
            # time.sleep(10)
            return True
        except NoSuchElementException as e:
            self.log.error(
                "Error {} occurred when clicking on submit button on the review page".format(e))
            return False
