import os.path
import win32com.client
import file_operations
from log_operations import custom_logger

log = custom_logger()
err_msg = 'No such driver, error: {} while getting driver type specified'
app_type = "Outlook.Application"
name_space = "MAPI"


def send_outlook_email(file_to_attach=None, add_sub=None):
    """
    method to send an outlook365 email for notification
    :param add_sub: additional subject line if user wishes to share status
    :param file_to_attach: full file path to attach
    :return: None if success, else error
    """
    config_path = os.path.join(os.getcwd(), "config.cfg")
    to_email = file_operations.load_config_file(config_path, str('Email'), "TO_EMAIL")
    subject = file_operations.load_config_file(config_path, str('Email'), "SUBJECT")
    try:
        html = """
                <html>
                    <head></head>
                        <body>
                            <h1>Hi """ + to_email + """ !</h1>
                                <p>
                                    This is an Automatic email triggered by the
                                    """ + subject + """ robot to notify user on the bot
                                    execution progress / status to you.
                                </p>
                                <p>Kind regards,<br>
                                    <em>Quess Corp </em>
                                </p>
                        </body>
                </html>
                """
        outlook = win32com.client.Dispatch(app_type)
        mail = outlook.CreateItem(0)
        mail.To = to_email
        mail.Subject = subject + add_sub
        # mail.Body = 'Message body'
        mail.HTMLBody = html  # this field is optional
        # To attach a file to the email (optional):
        if file_to_attach is not None:
            attachment = file_to_attach
            mail.Attachments.Add(attachment)
        mail.Send()
    except Exception as e:
        log.exception(err_msg.format(e))
