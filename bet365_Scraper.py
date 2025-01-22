from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import requests

# Optional: Use an Anti-CAPTCHA service (e.g., 2Captcha)
USE_ANTICAPTCHA = False
ANTICAPTCHA_API_KEY = "YOUR_2CAPTCHA_API_KEY"

# Proxy configuration (optional)
USE_PROXY = False
PROXY = "IP:PORT"  # Replace with your proxy address

# URL to scrape
url = "https://www.bet365.com/#/HO/"


# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Enable headless mode (comment out for debugging)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

if USE_PROXY:
    options.add_argument(f'--proxy-server={PROXY}')

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Add stealth settings to avoid detection
stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

def solve_captcha(driver, anticaptcha_api_key, url):
    """Solve CAPTCHA using 2Captcha service."""
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        site_key = iframe.get_attribute("data-sitekey")
        
        # Submit the CAPTCHA solving request
        response = requests.post(
            "https://2captcha.com/in.php",
            data={"key": anticaptcha_api_key, "method": "userrecaptcha", "googlekey": site_key, "pageurl": url},
        )
        captcha_id = response.text.split('|')[1]
        
        # Wait for the solution
        time.sleep(20)  # Adjust based on your 2Captcha account speed
        solution_response = requests.get(
            f"https://2captcha.com/res.php?key={anticaptcha_api_key}&action=get&id={captcha_id}"
        ).text
        
        # Retry until solved
        while "CAPCHA_NOT_READY" in solution_response:
            time.sleep(5)
            solution_response = requests.get(
                f"https://2captcha.com/res.php?key={anticaptcha_api_key}&action=get&id={captcha_id}"
            ).text
        
        solution = solution_response.split('|')[1]
        # Inject the solution into the page
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{solution}";')
        return True
    except Exception as e:
        print("Error solving CAPTCHA:", e)
        return False

try:
    # Open the URL
    driver.get(url)

    # Randomized delay to mimic human behavior
    time.sleep(random.uniform(5, 10))

    # Check for CAPTCHA
    if "px-captcha" in driver.page_source:
        print("CAPTCHA detected! Attempting to solve...")
        if USE_ANTICAPTCHA:
            if not solve_captcha(driver, ANTICAPTCHA_API_KEY, url):
                raise Exception("Failed to solve CAPTCHA")
        else:
            raise Exception("CAPTCHA detected and no anti-CAPTCHA service is configured")

    # Wait for page elements to load
    time.sleep(random.uniform(5, 10))

    # Get the page source (HTML content)
    html = driver.page_source

    # Save the HTML content to a file for inspection
    with open("output_bet365.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML content saved to 'output_bet365.html'")

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the WebDriver
    driver.quit()
