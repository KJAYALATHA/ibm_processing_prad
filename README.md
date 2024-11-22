# Infosys Invoice Processing Bot

This project is using open source tools like python, selenium, pypdf2 and other python libraries to build a Invoice
upload robot referred as BOT

'-----------------------------To Install Ghostscript-------------------------------'

For macOS, open terminal and run command
'brew install ghostscript tcl-tk'

For Ubuntu, open terminal and run command
'apt install ghostscript python3-tk'

For Windows & Linux, check this link https://www.ghostscript.com/releases/gsdnld.html

For installing Ghostscript on Windows machine  https://ghostscript.com/doc/current/Install.htm

'----------------------------To Install Python-------------------------------------'

For installing Python , check this link  https://www.python.org/downloads/

'----------------------------To install pipenv environment---------------------'

For installing pipenv

1. go to the directory where python is installed
2. navigate to script directory under python folder
3. open command prompt in the script directory
4. run command 'pip install pipenv', this would take few minutes to complete

'----------------------------To Download drivers--------------------------------'

1. Chrome driver , check this link https://chromedriver.chromium.org/downloads
2. Edge driver , check this link https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
3. Firefox driver, check this link https://github.com/mozilla/geckodriver/releases
4. IE driver 32-bit , check
   this https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.0.0/IEDriverServer_Win32_4.0.0.zip
5. IE driver 64-bit , check this
   link https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.0.0/IEDriverServer_x64_4.0.0.zip

'--------------------------How to use the Infosys bot---------------------------'

1. download the Infosys bot zip file
2. extract the exe to a local machine by creating a directory e.g. C:\Infosys Process
3. create or ensure a subdirectory 'resources' under the Infosys Process directory
4. create or ensure a subdirectory 'drivers' with chromedriver.exe under the Infosys Process directory
5. place the digitally signed and merged pdf file in resources subdirectory
6. extract config.cfg file to same location where exe is placed
7. update the config.cfg file as necessary
8. double-click the exe
9. 'Infosys Invoice Bot Automation' pop-up window will open up asking user to enter the outlook password. This is needed
   for notification to user on bot
   progress
10. enter the outlook password and click on 'Begin Infosys Invoice Upload' button
11. see if logs folder was automatically created in the same directory where exe is placed
12. .log file will be generated under 'logs' folder which keeps getting updated as the execution progresses
13. pop-up will close automatically after the execution is completed and an email will be sent for both success and
    failed conditions

'------------------Note: If bot fails to open the browser that means the browser must have been upgraded automatically,
so please visit the driver links mentioned above to download
the latest driver for browser type and place in drivers folder ------------------------'