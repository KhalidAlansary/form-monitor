"""
Form Monitor:
This script monitors a Microsoft Forms page and sends an email notification
when the form is opened.
"""
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# URL to monitor
URL_TO_MONITOR = ('https://forms.office.com/Pages/ResponsePage.aspx'
                  '?id=TuBZmc5rLk2FGNNr8QsSUsqTWhNHmXJOjEUQMZDmTr1U'
                  'NE1UNUxOWk1ZU1lJTVk1VVdXSFVFNklWUi4u')

# String to check if the form is closed
FORM_CLOSED_TEXT = 'This form is closed.'

# Email addresses and password
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')
CC_EMAIL = os.environ.get('CC_EMAIL')

def send_email(subject, body):
    """
    Send an email notification.
    """
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Cc'] = CC_EMAIL
    msg['Subject'] = subject
    msg['X-Priority'] = '1'  # High priority
    msg['Importance'] = 'High'
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as connection:
        connection.login(SENDER_EMAIL, EMAIL_PASSWORD)
        connection.sendmail(SENDER_EMAIL, [RECIPIENT_EMAIL, CC_EMAIL], msg.as_string())


webdriver_service = Service('/usr/bin/chromedriver')
webdriver_options = Options()
webdriver_options.add_argument('--headless')  # Ensure GUI is off
webdriver_options.add_argument('--no-sandbox')
webdriver_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=webdriver_service, options=webdriver_options)

# Continuously monitor the webpage
prev_status_is_closed = None

while True:
    driver.get(URL_TO_MONITOR)

    # Wait for the page to fully load or until the text 'This form is closed.'
    # is present (which means the page has fully loaded)
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), FORM_CLOSED_TEXT))

    response = driver.page_source

    is_closed = FORM_CLOSED_TEXT in driver.page_source

    # If the content has changed, send an email
    if is_closed != prev_status_is_closed:
        if is_closed:
            print('Form Closed')
            send_email('Urgent: Form Closed', 'The form has been closed.')
        else:
            print('Form Opened')
            send_email('Urgent: Form Opened', 'The form has been opened.')

    prev_status_is_closed = is_closed

    # Remove all cookies to prevent the browser from serving cached pages
    driver.delete_all_cookies()

    # Wait for 30 seconds before checking again
    time.sleep(30)
