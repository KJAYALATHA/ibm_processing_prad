import os
import platform
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import file_operations
from log_operations import custom_logger

log = custom_logger()
config_path = os.path.join(os.getcwd(), "config.cfg")
download_dir = file_operations.load_config_file(config_path, str('Browser'), "DOWNLOAD_DIR")
headless_flag = file_operations.load_config_file(config_path, str('Browser'), "HEADLESS")


def get_driver(browser):
    """
    method to get the type of browser
    :param browser: options are [chrome | chrome_headless |firefox | firefox_headless | edge]
    :return: driver object
    """
    driver = None
    try:
        if browser.lower() == "chrome":
            driver = get_chrome()
        elif browser.lower() == 'firefox':
            driver = get_firefox()
        elif browser.lower() == "edge":
            driver = get_ie()
    except WebDriverException as wde:
        log.error('No such driver, error: {} while getting driver type specified'.format(wde.msg))
        return None
    return driver


def get_chrome():
    """
    method to get the chrome driver with options and capabilities
    :return: webdriver
    """
    try:
        # below settings are for setting default download path for automatic downloads.
        prefs = {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "download.default_directory": str(download_dir)
        }
        chrome_options = webdriver.ChromeOptions()
        if headless_flag == "True":
            chrome_options.add_argument('headless')
        # start browser in maximize based on OS
        if platform.system().lower() == "windows":
            chrome_options.add_argument('--start-maximized')
            # avoid the pycache file getting generated
            log_path = "NUL"
        else:
            chrome_options.add_argument('--kiosk')
            # avoid the pycache file getting generated
            log_path = "/dev/null"
        chrome_options.add_argument("no-sandbox")
        # to disable chrome notifications
        chrome_options.add_argument("--disable-notifications")
        # disable chrome automatic upgrade
        chrome_options.add_argument("--disable-gpu")
        # enable option to accept ssl certificates
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(service=Service(os.path.join(os.getcwd(), "drivers\\chromedriver.exe")),
                                  options=chrome_options)
        service_log_path=log_path
        desired_capabilities=capabilities
        # stealth(driver,
        #         languages=["en-US", "en"],
        #         vendor="Google Inc.",
        #         platform="Win32",
        #         webgl_vendor="Intel Inc.",
        #         renderer="Intel Iris OpenGL Engine",
        #         fix_hairline=True,
        #         )
        log.info('initiated chrome driver with web driver-manager, options and capabilities')
    except WebDriverException as wde:
        log.error('No such driver, error: {} while getting driver type specified'.format(wde.msg))
        return None
    return driver


def get_firefox():
    """
    method to get firefox driver with options and capabilities
    :return: webdriver
    """
    try:
        options = webdriver.FirefoxOptions()
        if headless_flag == "True":
            options.add_argument('headless')
        # start browser in maximize
        if platform.system().lower() == "windows":
            options.add_argument('--start-maximized')
            # avoid the pycache file getting generated
            log_path = "NUL"
        else:
            options.add_argument('--kiosk')
            # avoid the pycache file getting generated
            log_path = "/dev/null"
        # to disable chrome notifications
        options.add_argument("--disable-notifications")
        # disable chrome automatic upgrade
        options.add_argument("--disable-gpu")
        # enable option to accept ssl certificates
        capabilities = DesiredCapabilities.FIREFOX.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        # initiating firefox driver with web driver-manager, options and capabilities
        # setting the service_log_path to null to disable the geckodriver logs
        driver = webdriver.Firefox(service=Service(os.path.join(os.getcwd(), "drivers\\geckodriver.exe")),
                                   service_log_path=log_path,
                                   options=options,
                                   desired_capabilities=capabilities)
        log.info('initiated firefox driver with web driver-manager, options and capabilities')
    except WebDriverException as wde:
        log.error('No such driver, error: {} while getting driver type specified'.format(wde.msg))
        return None
    return driver


def get_ie():
    """
    method to get the ie driver with options and capabilities
    :return: webdriver
    """
    try:
        # initiating the ie options
        options = webdriver.EdgeOptions()
        if headless_flag == "True":
            options.add_argument('headless')
        # start browser in maximize
        if platform.system().lower() == "windows":
            options.add_argument('--start-maximized')
            # avoid the pycache file getting generated
            log_path = "NUL"
        else:
            options.add_argument('--kiosk')
            # avoid the pycache file getting generated
            log_path = "/dev/null"
        options.add_argument("no-sandbox")
        # to disable chrome notifications
        options.add_argument("--disable-notifications")
        # disable chrome automatic upgrade
        options.add_argument("--disable-gpu")
        # enable option to accept ssl certificates
        capabilities = DesiredCapabilities.EDGE.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        # initiating edge driver with web driver-manager, options and capabilities
        # setting the service_log_path to null to disable the geckodriver logs
        driver = webdriver.Ie(service=Service(os.path.join(os.getcwd(), "drivers\\msedgedriver.exe")),
                              service_log_path=log_path,
                              options=options,
                              desired_capabilities=capabilities)
        log.info('initiated edge driver with web driver-manager, options and capabilities')
    except WebDriverException as wde:
        log.error('No such driver, error: {} while getting driver type specified'.format(wde.msg))
        return None
    return driver


def get_browser(browser, url):
    """
    method to get the browser and return the driver to calling test
    :param browser: type [chrome | headless]
    :param url: url to launch the application
    :return: driver to calling test
    """
    try:
        # By default, all driver binaries are saved to user.home/.wdm folder.
        # You can override this setting and save binaries to project.root/.wdm
        # os.environ['WDM_LOCAL'] = '1'
        # SSL verification can be disabled for downloading webdriver binaries in case when you have troubles
        # with SSL Certificates or SSL Certificate Chain
        # os.environ['WDM_SSL_VERIFY'] = '0'
        while close_all_browsers():
            time.sleep(1)
        web_driver = get_driver(browser)
        time.sleep(3)
        web_driver.get(url)
        return web_driver
    except Exception as ex:
        log.error("Function get_browser failed with error :{}".format(ex))


def close_all_browsers():
    """
    method to kill any open firefox browsers
    :return: none
    """
    try:
        for browser_type in ["chromedriver.exe", "geckodriver.exe", "IEDriverServer.exe", "msedgedriver.exe"]:
            if platform.system().startswith("Win"):
                os.system("taskkill /im {}.exe /f 2>NUL".format(browser_type))
            elif platform.system() in ["Linux", "Darwin"]:
                os.system("pkill {}.exe".format(browser_type))
    except OSError:
        pass
