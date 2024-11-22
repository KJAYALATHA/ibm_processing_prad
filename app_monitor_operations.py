import requests

from log_operations import custom_logger

log = custom_logger()


def monitor(url):
    """
    method to check if a web portal is up and accessible
    :param url: url of the web portal
    :return: True else False
    """
    try:
        response = requests.head(url)
    except requests.exceptions.HTTPError:
        return False
    else:
        if response.status_code == 200:
            log.info("Application was reachable")
            return True
        else:
            log.info("Application was not reachable, hence terminating the execution of bot")
            return False
