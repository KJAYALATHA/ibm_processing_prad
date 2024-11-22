import os
import sys
import time

import PySimpleGUI as sg
import file_operations as fo
from gif_operations import generate_gif
from mail_operations import send_outlook_email
from portals.infosys_portal_iterations import upload_doc_to_infosys_iter


def run_bot():
    # Use a breakpoint in the code line below to debug your script.
    # Press ⌘F8 to toggle the breakpoint.
    sg.theme('SystemDefault')

    # ------------MENU DEFINITION----------------------
    menu_def = [['Help', ['About', 'Readme'], ]]
    try:
        # -------------LAYOUT--------------------------
        layout = [
            [sg.Menu(menu_def, tearoff=True)],
            [sg.Text(
                'Click "Infosys Invoice Upload" button to begin the Infosys Invoice Upload Process:'),
                sg.Text(size=(40, 1), key='-OUTPUT-')],
            [sg.Button('Begin Infosys Invoice Upload'), sg.Button('Exit')]
        ]

        # -------------WINDOW TITLE--------------------
        window = sg.Window("Infosys Upload Invoice Bot", layout, default_element_size=(40, 1),
                           grab_anywhere=False)
        event, values = window.read()
        if event in (None, sg.WIN_CLOSED, 'Exit', 'Quit', 'Cancel'):
            pass
        elif event == 'About':
            sg.popup('This tool was developed by PRADEEP RAJU SIBBAL, contact email id: ',
                     'PRADEEP.RAJU1979@GMAIL.COM',
                     'This Tool is owned by TERRIER SECURITY SERVICES Business Unit, contact: ',
                     'ANJANA.KOVOOR@QUESSCORP.COM')
        elif event == 'Readme':
            sg.popup('This tool was developed to perform the Infosys Invoice Upload process',
                     'To begin with first user of the bot must enter the outlook password',
                     'so that user can be notified if the task is completed or any error',
                     'occurred during the process of upload ')
        # we initialize the variable start to store the starting time of execution of program
        start = time.time()
        if event == 'Begin Infosys Invoice Upload':
            config_path = os.path.join(os.getcwd(), "config.cfg")
            browser = fo.load_config_file(config_path, str('Browser'), "BROWSER_TYPE")
            screen_capture = fo.load_config_file(config_path, str("Screenshot"), "REQUIRED")
            url = fo.load_config_file(config_path, str('Browser'), "URL")
            # clear screenshots directory
            fo.check_and_delete_dir(os.path.join(os.getcwd(), "screenshots"))
            # create new screenshots dir
            if screen_capture == True:
                fo.create_folder(os.path.join(os.getcwd(), "screenshots"))
            # begin the infosys upload process from here
            result = upload_doc_to_infosys_iter(str(browser), str(url))
            # generating a gif file
            if screen_capture == True:
                generate_gif(os.path.join(os.getcwd(), "screenshots"))
            if not result:
                msg = "Failed to complete the Infosys Invoice Upload task"
                print(msg)
                send_outlook_email(add_sub=msg)
                sys.exit(msg)
            else:
                msg = "Passed Infosys Invoice Upload task successfully"
                print(msg)
                send_outlook_email(add_sub=msg)
                # now we have initialized the variable
                # end to store the ending time after
                # execution of program
                end = time.time()
                # difference of start and end variables
                # gives the time of execution of the
                # program in between
                print("Execution in seconds for Infosys Invoice upload program was :", round(end - start))
                window.close()
    except Exception as e:
        print("Error {0} launching the user interface for bot".format(e))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_bot()
