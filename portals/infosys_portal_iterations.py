import glob
import os
import sys
from pathlib import Path
import pandas as pd
import file_operations as fo
from app_monitor_operations import monitor
from browser_operations import get_browser, close_all_browsers
from log_operations import custom_logger
from mail_operations import send_outlook_email
from pages.infosys_purchase_order import InfosysPurchaseOrderPage
from pages.infosys_create_invoice import InfosysCreateInvoicePage
from pages.infosys_home import InfosysHomePage
from pages.infosys_login import InfosysLoginPage
from pages.infosys_receipts import InfosysReceiptsPage
from pages.infosys_review import InfosysReviewPage
from pages.infosys_search_results import InfosysSearchResultsPage
from pages.infosys_submitted import InfosysInvoiceSubmittedPage
from pdf_operations import create_json_file

log = custom_logger()


def upload_doc_to_infosys_iter(browser, url):
    global driver, result, file, screenshot, po_number
    try:
        # reading configurations
        config_path = os.path.join(os.getcwd(), "config.cfg")
        screenshot = fo.load_config_file(config_path, str('Screenshot'), "REQUIRED")
        infosys_user_id = fo.load_config_file(config_path, str('App_Credentials'), "INFOSYS_PORTAL_LOGIN_ID")
        infosys_passwd = fo.load_config_file(config_path, str('App_Credentials'), "INFOSYS_PORTAL_PWD")
        input_location = fo.load_config_file(config_path, str('Input'), "INPUT_FILE_LOCATION")

        # check the app status before stating the upload process
        if monitor(url):
            # ------------------Launching driver and browser with application url--------------------------------
            driver = get_browser(browser, url)
            login = InfosysLoginPage(driver)
            home = InfosysHomePage(driver)
            search = InfosysSearchResultsPage(driver)
            purchase_order = InfosysPurchaseOrderPage(driver)
            create_invoice = InfosysCreateInvoicePage(driver)
            review_invoice = InfosysReviewPage(driver)
            submitted = InfosysInvoiceSubmittedPage(driver)
            receipts = InfosysReceiptsPage(driver)
            # Login to infosys portal
            result = login.login_to_arbia(infosys_user_id, infosys_passwd)
            if not result:
                msg = "Failed to login to Infosys Arbia web portal"
                send_outlook_email(add_sub=msg)
                result = False
            # navigate to create po invoice
            result &= home.navigate_to_create_po_invoice()
            if not result:
                msg = "Failed to navigate to create PO invoice on Infosys Arbia web portal"
                send_outlook_email(add_sub=msg)
                result = False

            # --------------------validating if we have required data from combined pdf, before proceeding-----------
            location = os.path.join(os.getcwd(), input_location, "*.pdf*")
            files_lst = glob.glob(location)
            if len(files_lst) == 0:
                sys.exit("No files available in the input folder location : {} , hence terminating run"
                         .format(os.path.join(os.getcwd(), input_location)))
            # ---------getting the inputs from PDF file before proceeding with infosys process----------------------
            for file in files_lst:
                # check file size is less than 100 MB before proceeding and skip the iteration -- Fix done with regex
                size = fo.file_size(file)
                if int(size) == 0:
                    msg = "Merged PDF file {} size is 0KB, hence terminating the iteration".format(
                        Path(file).name)
                    log.error(msg)
                    send_outlook_email(file, msg)
                    continue
                file_name = Path(file).name
                # generate json file from the parsed PDF
                file_path = create_json_file(file_name, 0)
                data = pd.read_json(file_path[0])
                df = pd.DataFrame(data)
                if len(str(df['po_number'][0])) > 0:
                    # expand search filter
                    result &= home.expand_search_filter()
                    if not result:
                        msg = "Failed to expand search filter on Infosys Arbia web portal"
                        send_outlook_email(add_sub=msg)
                        result = False
                    # search by po number
                    result &= home.search_by_po_number(df['po_number'][0])
                    if not result:
                        msg = "Failed to find search results for PO {}".format(df['po_number'][0])
                        send_outlook_email(file, msg)
                        result = False
                    # select order number from search results
                    result &= search.select_order_number()
                    if not result:
                        msg = "Failed to find order number without obsoleted status in the table for PO {}".format(
                            po_number)
                        send_outlook_email(file, msg)
                        result = False
                    # navigate to standard invoice
                    result &= purchase_order.navigate_to_standard_invoice()
                    if not result:
                        msg = "Failed to navigate to standard invoice page in the infosys web portal"
                        send_outlook_email(file, msg)
                        result = False
                    # check for GRN receipts
                    result &= receipts.select_grn_number(str(df['grn_number'][0]))
                    if not result:
                        msg = "Failed to select grn number on receipts page in the infosys web portal"
                        send_outlook_email(file, msg)
                        result = False
                    # create standard invoice
                    result &= create_invoice.enter_invoice_details(df['invoice_number'][0], df['invoice_date'][0])
                    if not result:
                        msg = "Failed to enter invoice details on create invoice page in the infosys web portal"
                        send_outlook_email(file, msg)
                        result = False
                    # enter India specific information
                    result &= create_invoice.enter_india_specific_info(df['place_of_supply'][0], df['sez'][0],
                                                                       df['lut_number'][0], df['lut_date'][0],
                                                                       df['supplier_pan'][0], df['customer_pan'][0],
                                                                       df['supplier_gstin'][0], df['customer_gstin'][0],
                                                                       df['irn_number'][0], file)
                    if not result:
                        msg = "Failed to enter India specific information on create invoice page in the infosys web " \
                              "portal "
                        send_outlook_email(file, msg)
                        result = False
                    # enter line items
                    result &= create_invoice.complete_line_items(df['hsn_number'][0],
                                                                 str(df['tax_percentage'][0]).replace("%", ""),
                                                                 df["sez"][0], df["tax_type"][0])
                    if not result:
                        msg = "Failed to complete line item details on create invoice page in the infosys web portal"
                        send_outlook_email(file, msg)
                        result = False
                    # navigate to final review page
                    result &= create_invoice.navigate_to_review()
                    if not result:
                        msg = "Failed to navigate to final review page in the infosys web portal"
                        send_outlook_email(file, msg)
                        result = False
                    # review before submit
                    result &= review_invoice.review_before_submit(df['invoice_number'][0], df['po_number'][0],
                                                                  df['sub_total_amount'][0], df['tax_amount'][0],
                                                                  df['total_amount'][0], df['supplier_gstin'][0],
                                                                  df['customer_gstin'][0], df['supplier_pan'][0],
                                                                  df['lut_number'][0], df['lut_date'][0],
                                                                  df['customer_pan'][0], df['irn_number'][0],
                                                                  df['customer_pan'][0], df['hsn_number'][0],
                                                                  df['place_of_supply'][0], file_name,
                                                                  df["tax_type"][0])
                    if not result:
                        msg = "Failed to verify the details from merged pdf file on review page in the infosys web " \
                              "portal "
                        send_outlook_email(file, msg)
                        result = False
                    # submit invoice
                    result &= review_invoice.submit_invoice()
                    if not result:
                        msg = "Failed to submit invoice on review page in the infosys web portal"
                        send_outlook_email(file, msg)
                        result = False
                    # submit confirmation message
                    result &= submitted.verify_invoice_submitted(df['invoice_number'][0])
                    if not result:
                        msg = "Failed to see the invoice number {} on submit confirmation page in the infosys " \
                              "web portal".format(df['invoice_number'][0])
                        send_outlook_email(file, msg)
                        result = False
                    # exit invoice submitted page
                    result &= submitted.exit_invoice_submission()
                    if not result:
                        msg = "Failed to exit submit confirmation page in the infosys web portal"
                        send_outlook_email(file, msg)
                        result = False
                    # click on done button to go back to po search screen
                    result &= purchase_order.complete_invoice_creation()
                    if not result:
                        msg = "Failed to click done button on Purchase Order page in the infosys web portal"
                        send_outlook_email(file, msg)
                        result = False
                else:
                    msg = "Required field values in the PDF file was found to be missing"
                    log.error(msg)
                    send_outlook_email(file, msg)
                    result = False
                # remove the json file created
                os.remove(os.path.join(os.getcwd(), file_path[0]))
                # For loop end
        else:
            msg = "Failed with Error Infosys Arbia web portal is not accessible"
            log.error(msg)
            send_outlook_email(file, msg)
            result = False

    except Exception as e:
        msg = "Error {} while uploading the documents to Infosys Arbia web portal".format(e)
        log.error(msg)
        send_outlook_email(file, "Failed to perform the invoice upload on Infosys Arbia web portal")
        result = False
    finally:
        log.info(
            "Uploading documents to Infosys Arbia web portal task finished, check email for success or failure message")
        driver.quit()
        close_all_browsers()
    return result
