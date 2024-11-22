import os
import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import file_operations
from date_time_operations import get_format_time
from log_operations import custom_logger


class SeleniumHelperPage(object):

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, 30)
        self.log = custom_logger()

    def find_element(self, locator):
        """
        Method to locate the web element
        :param locator: locator - tuple
        :return: web element
        """
        try:
            return self.driver.find_element(*locator)
        except Exception as e:
            self.log.error("Exception {0} while finding element".format(e))
            return None

    def click(self, *locator):
        """
        Method to click on a element
        :param locator: locator - tuple
        :return: result - boolean
        """
        result = False
        try:
            config_path = os.path.join(os.getcwd(), "config.cfg")
            flag = file_operations.load_config_file(config_path, str('Screenshot'), "REQUIRED")
            element = self.element_visible(locator)
            if flag == True:
                self.add_screenshot(self.driver, '{0}_screenshot_{1}'.format(get_format_time(), locator[1]))
            element.click()
            result = True
            self.log.info(
                "Web element {0} : {1} successfully clicked".format(
                    locator[0], locator[1]))
        except NoSuchElementException as ex:
            self.log.error("Failed to click Web element {0} : {1},"
                           " displayed with error {2}".format(locator[0],
                                                              locator[1],
                                                              ex.msg))
        except Exception as e:
            self.log.error("Exception {}".format(e))
        return result

    def click_by_actions(self, *locator):
        """
        Method to click on a element
        :param locator: locator - tuple
        :return: result - boolean
        """
        try:
            config_path = os.path.join(os.getcwd(), "config.cfg")
            flag = file_operations.load_config_file(config_path, str('Screenshot'), "REQUIRED")
            element = self.element_visible(locator)
            # create action chain object
            action = ActionChains(self.driver)
            action.move_to_element(element)
            if flag == True:
                self.add_screenshot(self.driver, '{0}_screenshot_{1}'.format(get_format_time(), locator[1]))
            action.click()
            action.perform()
            self.log.info(
                "Web element {0} : {1} successfully clicked".format(
                    locator[0], locator[1]))
        except NoSuchElementException as ex:
            self.log.error("Failed to click Web element {0} : {1},"
                           " displayed with error {2}".format(locator[0],
                                                              locator[1],
                                                              ex.msg))

    def click_by_js(self, locator):
        """
        wrapper function to click on web element by java script
        :param locator:
        :return:
        """
        try:
            element = self.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except NoSuchElementException as ex:
            self.log.error("Failed to click Web element {} : {}, displayed with error {}"
                           .format(locator[0], locator[1], ex.msg))
            return False

    def wait_for_element(self, locator):
        """
        Method to wait for an element using locator
        :param locator: locator
        :return: element
        """
        try:
            config_path = os.path.join(os.getcwd(), "config.cfg")
            browser_wait = file_operations.load_config_file(config_path, str('Browser'), "MAX_WAIT")
            wait = WebDriverWait(self.driver, browser_wait * 2)
            element = wait.until(ec.visibility_of_element_located(locator))
            return element
        except NoSuchElementException as e:
            self.log.info("Exception - No such element {0}".format(e))
            return None

    def is_element_visible(self, locator):
        """
        Method to verify if element is visible
        :param locator: locator
        :return: boolean
        """
        try:
            config_path = os.path.join(os.getcwd(), "config.cfg")
            element_wait = file_operations.load_config_file(config_path, str('Browser'), "ELEMENT_WAIT")
            WebDriverWait(self.driver, element_wait, poll_frequency=1,
                          ignored_exceptions=[NoSuchElementException]).until(
                ec.visibility_of_element_located(locator))
            return True
        except Exception as e:
            self.log.info("Exception - No such element {0}".format(e))
            return False

    def get_current_url(self):
        return self.driver.current_url

    def get_attribute_value(self, attribute_name, *locator):
        """
         Method to get attribute of a locator
         :param attribute_name: atrib name
         :param locator: element locator
         :return:
         """
        try:
            element = self.find_element(*locator)
            return element.get_attribute(attribute_name)
        except Exception as e:
            self.log.info("Exception - No such element {0}".format(e))
            return None

    def get_attribute_of_element(self, attribute_name, element):
        """
        Method to get attribute of an web element
        :param attribute_name: atrib name
        :param element: web element
        :return:
        """
        try:
            return element.get_attribute(attribute_name)
        except Exception as e:
            self.log.info("Exception - No such element {0}".format(e))
            return None

    def get_text(self, *locator):
        try:
            element = self.element_visible(locator)
            value = element.text
            self.log.info('element text is {0}'.format(value))
            return value
        except NoSuchElementException as ex:
            self.log.error("No such element exception {0} was displayed during"
                           " element {1} : {2} location ".format(ex.msg,
                                                                 locator[0],
                                                                 locator[1]))

            return None

    def clear_text(self, *locator):
        """
        wrapper function to clear text in the type text web element
        :param locator:
        :return: True is text is entered successfully else False
        """
        try:
            element = self.find_element(locator)
            element.clear()
            self.log.info("Cleared text field Web element {} : {}".
                          format(locator[0], locator[1]))
            return True
        except NoSuchElementException as ex:
            self.log.error("Failed to clear value for text web element {} : {},displayed with error message {}".
                           format(locator[0], locator[1], ex.msg))
            return False

    def set_text(self, data, *locator, flag=None):
        """
        wrapper function to enter a text in the type text web element
        :param flag: to send the value of data to log or not
        :param data:
        :param locator:
        :return: True is text is entered successfully else False
        """
        try:
            element = self.find_element(locator)
            element.send_keys(str(data))
            time.sleep(1)
            config_path = os.path.join(os.getcwd(), "config.cfg")
            src_flag = file_operations.load_config_file(config_path, str('Screenshot'), "REQUIRED")
            if src_flag == True:
                self.add_screenshot(self.driver, '{0}_screenshot_{1}'.format(get_format_time(), locator[1]))
            if flag is not None:
                data = "***********"
            self.log.info("Web element {} : {} was located and entered with value : {}".
                          format(locator[0], locator[1], str(data)))
            return True
        except NoSuchElementException as ex:
            self.log.error("Failed to enter value {} for web element {} : {},displayed with error message {}".
                           format(str(data), locator[0], locator[1], ex.msg))
            return False

    def press_enter(self, *locator):
        """
        wrapper function to press keyboard enter key on web element
        :param locator:
        :return: True is text is entered successfully else False
        """
        try:
            element = self.find_element(locator)
            element.send_keys(Keys.ENTER)
            self.log.info("Web element {} : {} was located pressed keyboard enter".
                          format(locator[0], locator[1]))
            return True
        except NoSuchElementException as ex:
            self.log.error("Failed press enter key for web element {} : {},displayed with error message {}".
                           format(locator[0], locator[1], ex.msg))
            return False

    def element_visible(self, locator):
        try:
            config_path = os.path.join(os.getcwd(), "config.cfg")
            browser_wait = file_operations.load_config_file(config_path, str('Browser'), "MAX_WAIT")
            element = WebDriverWait(self.driver, browser_wait).until(
                ec.visibility_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView();",
                                       element)
            self.log.info("Web element {0} : {1} "
                          "was visible".format(locator[0], locator[1]))
            return element
        except StaleElementReferenceException as ser:
            self.log.error("Stale element exception {0} was displayed during"
                           " element {1} : {2} location ".format(ser.msg,
                                                                 locator[0],
                                                                 locator[1]))
        except NoSuchElementException as ex:
            self.log.error("No such element exception {0} was displayed during"
                           "element {1} : {2} location".format(ex.msg,
                                                               locator[0],
                                                               locator[1]))
        except TimeoutException as et:
            self.log.error("Script timed out with message {0} during "
                           "element {1} : {2} location".format(et.msg,
                                                               locator[0],
                                                               locator[1]))

    def js_wait_for_condition(self, js_script, timeout):
        """
        Method for waiting for java script execution
        :param js_script: java script
        :param timeout: max wait time
        :return:  boolean value
        """
        result = False
        try:
            for x in range(1, timeout):
                x = self.driver.execute_script("return " + js_script)
                if x:
                    result = True
                time.sleep(1)
        except Exception as e:
            self.log.error("Exception {} occurred while waiting for JS condition".format(e))
            result = False
        return result

    def wait_for_page_load(self):
        """
         Waiting for the page to load
        :return:
        """
        try:
            self.js_wait_for_condition('document.readyState;', 5)
        except Exception as e:
            self.log.error("Exception {} while waiting for page load".format(e))

    def add_screenshot(self, driver, title):
        """
        method to add screenshot to allure report based on commandline input
        :param driver: web driver instance
        :param title: name of screenshot
        """
        try:
            driver.get_screenshot_as_file(os.path.join(os.getcwd(), "screenshots", "{}.png".format(title)))
            self.log.info('attached screenshot {0}'.format(title))
        except Exception as e:
            self.log.error('Failed to attach screenshot due to exception {0}'.format(e))
