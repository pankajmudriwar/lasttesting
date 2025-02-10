from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import re
from twilio.rest import Client

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
# chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)


def send_sms():
    # Send SMS Notification via Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)



    message = client.messages.create(
        body="ha test available hai",
        from_=TWILIO_PHONE_NUMBER,
        to=YOUR_PHONE_NUMBER
    )
    print("SMS Sent:", message.sid)

def send_call():
    TWILIO_ACCOUNT_SID = "AC371a5ba7227a379a94ee8b9889e8a118"
    TWILIO_AUTH_TOKEN = "52dfdd8430d84278c032769c0756b3a9"
    TWILIO_PHONE_NUMBER = "+15804074051"
    YOUR_PHONE_NUMBER = "+919404135316"
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to=YOUR_PHONE_NUMBER,
    from_=TWILIO_PHONE_NUMBER,)

try:
    # Open UserTesting login page
    driver.get("https://auth.usertesting.com/")

    time.sleep(3)  # Wait for the page to load

    # Find login fields and enter credentials
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

# Wait for the email field to appear (max 10 seconds)
    email_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "idp-discovery-username"))
    )
    email_field.send_keys(USERTESTING_EMAIL)
    
    next_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "idp-discovery-submit"))
    )
    
    
    next_field.click()
      
    signin_page="https://auth.usertesting.com/signin"

    password_field = WebDriverWait(driver, 10).until(
        
    EC.presence_of_element_located((By.ID, "okta-signin-password"))
    )

    password_field.send_keys(USERTESTING_PASSWORD)

    signin_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "okta-signin-submit"))
    )
    signin_field.click()
    
    # signin id=okta-signin-submit
    # passwordid=okta-signin-password

    # text= We're looking for available tests... 

    search_text = "Check back anytime for new tests, or we'll notify you."
      # Print the full page source
    elements = WebDriverWait(driver, 1000).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".available-tests-list__empty-state.mh-auto.l-block"))
    )
    # elements = driver.find_elements(By.CSS_SELECTOR, ".available-tests-list__empty-state.mh-auto.l-block")
    print(elements)
    if elements:
        print("test is not available")
    else:
        print("test is available")
        send_call()



    
    
    time.sleep(50)

except Exception as e:
    print("Error:", str(e))

finally:
    driver.quit()
