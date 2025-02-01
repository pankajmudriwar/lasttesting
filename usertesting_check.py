from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from twilio.rest import Client

# Hardcoded credentials
USERTESTING_EMAIL = "mudriwarfalgun@gmail.com"
USERTESTING_PASSWORD = "Pankaj15@"

TWILIO_ACCOUNT_SID = "AC371a5ba7227a379a94ee8b9889e8a118"
TWILIO_AUTH_TOKEN = "1b8df052bade6f2d07ce340f7c61eed9"
TWILIO_PHONE_NUMBER = "+15804074051"
YOUR_PHONE_NUMBER = "+919404135316"
# Set up Selenium with Chromium
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open UserTesting login page
    driver.get("https://www.usertesting.com/login")
    time.sleep(3)  # Wait for the page to load

    # Find login fields and enter credentials
    email_field = driver.find_element("name", "email")
    password_field = driver.find_element("name", "password")
    login_button = driver.find_element("xpath", "//button[@type='submit']")

    email_field.send_keys(USERTESTING_EMAIL)
    password_field.send_keys(USERTESTING_PASSWORD)
    login_button.click()

    time.sleep(5)  # Wait for the page to load after login

    # Check if tests are available
    if "dashboard" in driver.current_url:
        message_body = "✅ UserTesting has available tests!"
    else:
        message_body = "❌ No tests available on UserTesting."

    print(message_body)

    # Send SMS Notification via Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=YOUR_PHONE_NUMBER
    )
    print("SMS Sent:", message.sid)

except Exception as e:
    print("Error:", str(e))

finally:
    driver.quit()
