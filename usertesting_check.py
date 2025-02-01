from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client
import time

# Hardcoded credentials (Replace with your details)
USERNAME = "mudriwarfalgun@gmail.com"
PASSWORD = "Panakj15@"
TWILIO_SID = "AC371a5ba7227a379a94ee8b9889e8a118"
TWILIO_AUTH_TOKEN = "1b8df052bade6f2d07ce340f7c61eed9"
TWILIO_PHONE_NUMBER = "+15804074051"  # Your Twilio phone number
YOUR_PHONE_NUMBER = "+919404135316"   # Your personal phone number

# Function to send SMS
def send_sms(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=YOUR_PHONE_NUMBER
    )
    print("📩 SMS sent successfully!")

# Configure Selenium to use Chrome in headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run without opening a browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Open UserTesting login page
    driver.get("https://www.usertesting.com/login")
    time.sleep(3)

    # Enter email
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(USERNAME)

    # Enter password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)  # Press Enter

    time.sleep(5)  # Wait for login to complete

    # Navigate to the dashboard
    driver.get("https://www.usertesting.com/dashboard")
    time.sleep(3)

    # Check if test slots are available
    try:
        test_element = driver.find_element(By.XPATH, "//div[contains(text(), 'New test available')]")
        print("✅ Test available!")
        send_sms("🚀 New UserTesting test is available! Check your dashboard now.")
    except:
        print("❌ No test available at the moment.")

finally:
    driver.quit()  # Close the browser
