import glob
import json
import os
import re
import sys
from pathlib import Path
import PyPDF2

from file_operations import get_file_path_from_dir, load_config_file
from log_operations import custom_logger

log = custom_logger()
config_path = os.path.join(os.getcwd(), "config.cfg")
input_location = load_config_file(config_path, str('Input'), "INPUT_FILE_LOCATION")


def get_pdf_data(partial_file_name, page_number):
    """
    method to read the text from PDf file
    :param partial_file_name: partial file name or only extension
    :param page_number: page to be extracted based on page number passed as integer
    :return: pdf extracted content as array of items
    """
    new_lst = []
    try:
        file_name = get_file_path_from_dir(input_location, partial_file_name)
        pdf_reader = PyPDF2.PdfReader(file_name[0])
        pdf_tool_name = str(pdf_reader.metadata.producer)
        # checking if PDF tool is as expected
        if "iText" not in pdf_tool_name:
            sys.exit("PDF Creation tool has been changed from iText to {}".format(pdf_tool_name))
        log.info(pdf_reader.metadata)
        text = pdf_reader.pages[page_number]
        lst = text.extract_text().split("\n")
        # checking of the value is not null and then appending to array
        new_lst = [a.strip() for a in lst if len(a) > 1 and a != '']
        # eliminate any empty strings from the list
        while "" in new_lst:
            new_lst.remove("")
    except Exception as e:
        log.error(f"Failed to read pdf file due to error {e}")
    return new_lst


# print(get_pdf_data("INVOICE_KT532692.pdf", 0))


def get_value_from_pdf(file_name, page_number, value, index=None):
    """
    method to get the PO number from the PDF file
    :param index: if multiple items with same value, then provide index of item e.g. GSTIN
    :param value: string of text mentioned in convention dict to search in the array list
    :param file_name: file extension of the pdf file if more than one file is there, provide full file name
    :param page_number: integer value of page number
    :return: string text if found return error
    """
    arr = get_pdf_data(file_name, page_number)
    # arr = [arr[i] for i, j in enumerate(arr) if arr[i] != '  ']
    if len(arr) == 0:
        log.error("Failed to parse PDF file")
        return False
    # This is to find the text dynamically in the PDF parsed data which is returned as array list
    # starting after the quess address lines which is line 4
    # indices = [i for i, s in enumerate(arr, start=4) if value in s]
    indices = []
    for i in range(4, len(arr)):
        if value in str(arr[i]):
            indices.append(i)
    # Updated convention on 11-Oct-2022 Based on issues reported from Akshay
    convention = {"INVOICE": 0, "GSTIN": 1, "Date(DD/MM/YYYY)": 1, "Customer PAN": 2, "PAN Number": 1,
                  "Bill To": 3,
                  "Ship To": 6, "Place of supply": 0, "HSN": 0, "PO.": 0, "LUT": 0, "IRN": 0,
                  "IGST": 0, "CGST": 0, "Qty": 10, "Amount (Net)": 1, "IGST (18%)": 1, "Total": 0, "Bank Name": 1,
                  "Account No": 1,
                  "IFSC": 1, "Date of filing": 0, "CGST (9%)": 1, "SGST (9%)": 1, "Professional Software": 1}
    # handle the index for duplicate values
    if value in convention:
        if index is None:
            indices = int(indices[0]) + int(convention.get(value))
        elif index == 0:
            indices = int(indices[index]) + int(convention.get(value)) + 1
        else:
            indices = int(indices[index]) + int(convention.get(value))
    return arr[indices]


# print(get_value_from_pdf("pdf", 0, "GSTIN", 1))


def get_invoice_number(file_name, page_number):
    try:
        flag = None
        arr = get_pdf_data(file_name, page_number)
        for i in arr:
            flag = re.findall('[A-Z]{2}[0-9]{6}', i)
            if len(flag) > 0:
                break
        return flag[0]
        # text = get_value_from_pdf(file_name, page_number, "INVOICE")
        # return text.split(":")[1].strip()
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for invoice number".format(ex))


# regex_pan =

def get_quess_gstin(file_name, page_number):
    try:
        flag = None
        arr = get_pdf_data(file_name, page_number)
        for i in arr:
            flag = re.findall(
                '^([0][1-9]|[1-2][0-9]|[3][0-7])([A-Z]{5})([0-9]{4})([A-Z]{1}[1-9A-Z]{1})([Z]{1})([0-9A-Z]{1})+$', i)
            if len(flag) > 0:
                break
        return "".join(flag[0])
        # supplier_gstin = get_value_from_pdf(file_name, page_number, "GSTIN")
        # return supplier_gstin
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for supplier gstin".format(ex))


def get_invoice_date(file_name, page_number):
    try:
        flag = None
        arr = get_pdf_data(file_name, page_number)
        for i in arr:
            flag = re.findall('[0-9]{2}/[0-9]{2}/[0-9]{4}', i)
            if len(flag) > 0:
                break
        return flag[0]
        # text = get_value_from_pdf(file_name, page_number, "Date(DD/MM/YYYY)")
        # return text.split(":")[1].strip()
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for invoice date".format(ex))


def get_customer_gstin(file_name, page_number):
    try:
        gstin_arr = []
        arr = get_pdf_data(file_name, page_number)
        for i in arr:
            flag = re.findall(
                '   ([0][1-9]|[1-2][0-9]|[3][0-7])([A-Z]{5})([0-9]{4})([A-Z]{1}[1-9A-Z]{1})([Z]{1})([0-9A-Z]{1})+$', i)
            if len(flag) > 0:
                gstin_arr.append("".join(flag[0]))
        return gstin_arr[0]
        # text = get_value_from_pdf(file_name, page_number, "GSTIN", 1)
        # return text.split(":")[1].lstrip()
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for customer gstin".format(ex))


def get_customer_pan(file_name, page_number):
    try:
        pan_arr = []
        flag = None
        arr = get_pdf_data(file_name, page_number)
        for i in arr:
            flag = re.findall('Number: [A-Z]{5}[0-9]{4}[A-Z]{1}', i)
            if len(flag) > 0:
                break
        return flag[0].split(":")[1].lstrip()
        # text = get_value_from_pdf(file_name, page_number, "Customer PAN")
        # return text.split(":")[1].lstrip()
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for customer pan".format(ex))


def get_quess_pan(file_name, page_number):
    try:
        flag = None
        arr = get_pdf_data(file_name, page_number)
        for i in arr:
            flag = re.findall('[A-Z]{5}[0-9]{4}[A-Z]{1}', i)
            if len(flag) > 0:
                break
        return flag[0]
        # text = get_value_from_pdf(file_name, page_number, "PAN Number")
        # return text.split(":")[1].lstrip()
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for supplier pan".format(ex))


def get_sez(file_name, page_number):
    try:
        flag = None
        arr = get_pdf_data(file_name, page_number)
        for i in arr:
            flag = re.findall('SEZ', i)
            if len(flag) > 0:
                break
        return flag[0]
        # value = ""
        # text = get_value_from_pdf(file_name, page_number, "Bill To")
        # try:
        #     value = text[text.find("SEZ"):text.find("SEZ") + len("SEZ")]
        # except ValueError:
        #     pass
        # return value
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for sez from Bill To address line".format(ex))


def get_place_of_supply(file_name, page_number):
    try:
        text = get_value_from_pdf(file_name, page_number, "Place of supply")
        return text.split("-")[-1].lstrip()
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for place of supply".format(ex))


def get_hsn_number(file_name, page_number):
    try:
        text = get_value_from_pdf(file_name, page_number, "HSN")
        return re.sub(r'[^0-9$]', '', text.split(":")[1].lstrip())
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for hsn number".format(ex))


def get_lut_number(file_name, page_number):
    try:
        text = get_value_from_pdf(file_name, page_number, "LUT")
        if "/ Date of filing" in text:
            return text.split(":")[1].replace("/ Date of filing", "").strip()
        else:
            return ''
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for lut number".format(ex))


def get_lut_date(file_name, page_number):
    try:
        lut_dt = get_value_from_pdf(file_name, page_number, "LUT")
        if "/ Date of filing" in lut_dt:
            text = get_value_from_pdf(file_name, page_number, "Date of filing")
            return re.findall(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', text.split(":")[2].lstrip())[0]
        else:
            return ''
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for lut date".format(ex))


def get_irn_number(file_name, page_number):
    try:
        text = get_value_from_pdf(file_name, page_number, "IRN")
        return text.split(":")[1].lstrip()
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for irn number".format(ex))


def get_subtotal_amount(file_name, page_number):
    try:
        sub_total = get_value_from_pdf(file_name, page_number, "Amount (Net)")
        return sub_total.split(" ")[0].replace("INR", "")
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for sub-total amount".format(ex))


def get_total_amount(file_name, page_number):
    try:
        total = get_value_from_pdf(file_name, page_number, "Total")
        return total.split(" ")[1]
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for total amount".format(ex))


def get_gst(file_name, page_number):
    try:
        parsed_arr = get_pdf_data(file_name, page_number)
        parsed_arr = [parsed_arr[i] for i, j in enumerate(parsed_arr) if parsed_arr[i] != '  ']
        if 'IGST (18%)' in parsed_arr:
            flag = None
            arr = get_pdf_data(file_name, page_number)
            for i in arr:
                flag = re.findall('IGST (18%)', i)
                if len(flag) > 0:
                    break
            return flag[0].replace("%", "")
            # text = get_value_from_pdf(file_name, page_number, "IGST (18%)")
            # return text.split(" ")[1].replace("%", "")
        else:
            flag = None
            arr = get_pdf_data(file_name, page_number)
            for i in arr:
                flag = re.findall('CGST (9%)', i)
                if len(flag) > 0:
                    break
            return flag[0].replace("%", "")
            # text = get_value_from_pdf(file_name, page_number, "CGST")
            # return text.split(" ")[1].replace("%", "")
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for gst value".format(ex))


def get_tax_amount(file_name, page_number):
    try:
        parsed_arr = get_pdf_data(file_name, page_number)
        parsed_arr = [parsed_arr[i] for i, j in enumerate(parsed_arr) if parsed_arr[i] != '  ']
        if 'IGST (18%)' in parsed_arr:
            tax_amount = get_value_from_pdf(file_name, page_number, "IGST (18%)")
            return tax_amount.replace("INR", "")
        else:
            tax_amount = get_value_from_pdf(file_name, page_number, "CGST (9%)")
            return tax_amount.replace("INR", "")
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for tax amount".format(ex))


def get_po_number(file_name, page_number):
    try:
        text = get_value_from_pdf(file_name, page_number, "PO.")
        return text.split(":")[-1].lstrip()
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for po number".format(ex))


def get_tax_type(file_name, page_number):
    try:
        arr = get_pdf_data(file_name, page_number)
        arr = [arr[i] for i, j in enumerate(arr) if arr[i] != '  ']
        index = [i for i, j in enumerate(arr) if 'IGST (18%)' in arr[i] or 'CGST (9%)' in arr[i]]
        return arr[index[0]].split(" ")[0]
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for tax type".format(ex))


def get_grn_number(file_name, page_number):
    try:
        text = get_value_from_pdf(file_name, page_number, "Professional Software")
        if len(text.split(" ")) >= 4:
            return text.split(" ")[3].lstrip()[:10]
        else:
            return ""
    except Exception as ex:
        log.error("Error {} parsing the merged pdf file for grn from description".format(ex))


def create_json_file(file_name=None, page_number=None):
    dictionary = {"invoice_number": [get_invoice_number(file_name, page_number)],
                  "supplier_gstin": [get_quess_gstin(file_name, page_number)],
                  "invoice_date": [get_invoice_date(file_name, page_number)],
                  "customer_gstin": [get_customer_gstin(file_name, page_number)],
                  "customer_pan": [get_customer_pan(file_name, page_number)],
                  "supplier_pan": [get_quess_pan(file_name, page_number)],
                  "sez": [get_sez(file_name, page_number)],
                  "place_of_supply": [get_place_of_supply(file_name, page_number)],
                  "hsn_number": [get_hsn_number(file_name, page_number)],
                  "lut_number": [get_lut_number(file_name, page_number)],
                  "lut_date": [get_lut_date(file_name, page_number)],
                  "irn_number": [get_irn_number(file_name, page_number)],
                  "sub_total_amount": [get_subtotal_amount(file_name, page_number)],
                  "total_amount": [get_total_amount(file_name, page_number)],
                  "tax_percentage": [get_gst(file_name, page_number)],
                  "tax_amount": [get_tax_amount(file_name, page_number)],
                  "po_number": [get_po_number(file_name, page_number)],
                  "tax_type": [get_tax_type(file_name, page_number)],
                  "grn_number": [get_grn_number(file_name, page_number)]}

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    file_nm = Path(file_name).stem
    with open("{}.json".format(file_nm), "w") as outfile:
        outfile.write(json_object)
    return glob.glob(os.path.join(os.getcwd(), "{}.json".format(file_nm)))


# for file in get_file_path_from_dir(input_location, ".pdf"):
#     create_json_file(Path(file).name, 0)
