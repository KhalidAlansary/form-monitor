# Form Monitor

This Python script monitors a specific Microsoft Forms page and sends an email notification when the form is opened.

## Features

- Monitors a specific Microsoft Forms page continuously.
- Sends an email notification when the form is opened.
- Uses Selenium WebDriver to interact with the webpage.
- Uses smtplib to send email notifications.

## Requirements

- Python 3.6+
- Selenium WebDriver
- ChromeDriver

## Environment Variables

The script uses the following environment variables:

- `SENDER_EMAIL`: The email address that will be used to send the notifications.
- `EMAIL_PASS`: The password for the sender's email account.
- `RECIPIENT_EMAIL`: The email address that will receive the notifications.
- `CC_EMAIL`: The email address that will be CC'd on the notifications.

## Usage

1. Set the environment variables `SENDER_EMAIL`, `EMAIL_PASS`, `RECIPIENT_EMAIL`, and `CC_EMAIL`.
2. Run the script with Python 3.6 or higher.

```bash
python3 form_monitor.py
```

The script will continuously monitor the specified Microsoft Forms page and send an email notification when the form is opened.
