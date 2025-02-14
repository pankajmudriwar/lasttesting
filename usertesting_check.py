from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from twilio.rest import Client
import tempfile

# Hardcoded credentials
USERTESTING_EMAIL = "mudriwarfalgun@gmail.com"
USERTESTING_PASSWORD = "Pankaj15@"

TWILIO_ACCOUNT_SID = "AC371a5ba7227a379a94ee8b9889e8a118"
TWILIO_AUTH_TOKEN = "52dfdd8430d84278c032769c0756b3a9"
TWILIO_PHONE_NUMBER = "+15804074051"
YOUR_PHONE_NUMBER = "+919404135316"

# Set up Selenium with Chromium
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Use a temporary directory for the Chrome user data to avoid conflicts
temp_dir = tempfile.mkdtemp()
chrome_options.add_argument(f"--user-data-dir={temp_dir}")

# Initialize WebDriver
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

def send_sms():
    """Send an SMS notification via Twilio."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body="A UserTesting test is available!",
            from_=TWILIO_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
        print("SMS Sent:", message.sid)
    except Exception as e:
        print("Error sending SMS:", str(e))

def send_call():
    """Make a voice call via Twilio."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",
            to=YOUR_PHONE_NUMBER,
            from_=TWILIO_PHONE_NUMBER
        )
        print("Call Sent:", call.sid)
    except Exception as e:
        print("Error sending call:", str(e))

try:
    driver.get("https://auth.usertesting.com/")
    print("Opened UserTesting login page.")
    time.sleep(3)

    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "idp-discovery-username"))
    )
    email_field.send_keys(USERTESTING_EMAIL)
    print("Entered email.")

    next_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "idp-discovery-submit"))
    )
    next_field.click()
    print("Clicked 'Next'.")

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "okta-signin-password"))
    )
    password_field.send_keys(USERTESTING_PASSWORD)
    print("Entered password.")

    signin_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "okta-signin-submit"))
    )
    signin_field.click()
    print("Clicked 'Sign In'.")

    search_message = "Check back anytime for new tests, or we'll notify you."
    test_message_selector = ".available-tests-list__empty-state.mh-auto.l-block"

    try:
        element = WebDriverWait(driver, 550).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, test_message_selector))
        )
        print("No tests available:", element.text)
    except:
        print("Tests are available!")
        # send_sms()
        send_call()

    time.sleep(55)

except Exception as e:
    print("Error:", str(e))

finally:
    driver.quit()
    print("WebDriver closed.")

