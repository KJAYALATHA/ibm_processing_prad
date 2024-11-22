import os
import sys
import time

import file_operations as fo
from gif_operations import generate_gif
from log_operations import custom_logger
from mail_operations import send_outlook_email
from portals.infosys_portal_iterations_docker import upload_doc_to_infosys_iter

log = custom_logger()


def infosys_invoicing_integration():
    try:
        start = time.time()
        config_path = os.path.join(os.getcwd(), "config.cfg")
        browser = fo.load_config_file(config_path, str('Browser'), "BROWSER_TYPE")
        screen_capture = fo.load_config_file(config_path, str("Screenshot"), "REQUIRED")
        url = fo.load_config_file(config_path, str('Browser'), "URL")
        # clear screenshots directory
        fo.check_and_delete_dir(os.path.join(os.getcwd(), "screenshots"))
        # create new screenshots dir
        if screen_capture:
            fo.create_folder(os.path.join(os.getcwd(), "screenshots"))
        # begin the infosys upload process from here
        result = upload_doc_to_infosys_iter(str(browser), str(url))
        # generating a gif file
        if screen_capture:
            generate_gif(os.path.join(os.getcwd(), "screenshots"))
        if not result:
            msg = "Failed to complete the Infosys Invoice Upload task"
            print(msg)
            # send_outlook_email(add_sub=msg)
            sys.exit(msg)
        else:
            msg = "Passed Infosys Invoice Upload task successfully"
            print(msg)
            # send_outlook_email(add_sub=msg)
            # now we have initialized the variable
            # end to store the ending time after
            # execution of program
            end = time.time()
            # difference of start and end variables
            # gives the time of execution of the
            # program in between
            print("Execution in seconds for Infosys Invoice upload program was :", round(end - start))
    except Exception as e:
        log.error("Error in function {} due to {}".format(infosys_invoicing_integration.__name__, e))


if __name__ == '__main__':
    infosys_invoicing_integration()
