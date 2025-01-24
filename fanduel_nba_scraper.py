import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium_stealth import stealth

# List of user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    #"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
]

# Proxy list (if applicable)
PROXIES = ["IP:PORT1", "IP:PORT2", "IP:PORT3"]
USE_PROXIES = False

# CAPTCHA Solver Configuration (if enabled)
USE_ANTICAPTCHA = False
ANTICAPTCHA_API_KEY = "YOUR_2CAPTCHA_API_KEY"

# Randomized delays
def random_delay(min_sec=1, max_sec=3):
    delay = random.uniform(min_sec, max_sec)
    print(f"Random delay: {delay:.2f} seconds")
    time.sleep(delay)

# Get a random WebDriver (Chrome or Firefox)
def get_random_browser():
    browser_choice = random.choice(["chrome", "firefox"])
    user_agent = random.choice(USER_AGENTS)
    proxy = random.choice(PROXIES) if USE_PROXIES else None

    if browser_choice == "chrome":
        options = ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")  # Optional: Remove if debugging
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        # Apply stealth only for Chrome
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
    else:
        options = FirefoxOptions()
        options.set_preference("general.useragent.override", user_agent)
        options.headless = True  # Optional: Remove if debugging
        if proxy:
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http", proxy.split(":")[0])
            options.set_preference("network.proxy.http_port", int(proxy.split(":")[1]))
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    return driver


# Simulate mouse movement
def simulate_mouse_movement(driver):
    try:
        action = ActionChains(driver)
        for _ in range(random.randint(2, 5)):
            offset_x = random.randint(100, 300)
            offset_y = random.randint(100, 300)
            print(f"Moved mouse to offset: ({offset_x}, {offset_y})")
            action.move_by_offset(offset_x, offset_y).perform()
            random_delay(0.5, 1.5)
    except Exception as e:
        print(f"Error simulating mouse movement: {e}")

# Solve CAPTCHA (if using anti-CAPTCHA services)
def solve_captcha(driver, anticaptcha_api_key, url):
    try:
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        site_key = iframe.get_attribute("data-sitekey")
        response = requests.post(
            "https://2captcha.com/in.php",
            data={"key": anticaptcha_api_key, "method": "userrecaptcha", "googlekey": site_key, "pageurl": url},
        )
        captcha_id = response.text.split('|')[1]
        time.sleep(20)  # Adjust based on solving speed
        solution_response = requests.get(
            f"https://2captcha.com/res.php?key={anticaptcha_api_key}&action=get&id={captcha_id}"
        ).text
        while "CAPCHA_NOT_READY" in solution_response:
            time.sleep(5)
            solution_response = requests.get(
                f"https://2captcha.com/res.php?key={anticaptcha_api_key}&action=get&id={captcha_id}"
            ).text
        solution = solution_response.split('|')[1]
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{solution}";')
        return True
    except Exception as e:
        print("Error solving CAPTCHA:", e)
        return False
# Main execution with CAPTCHA handling
MAX_RETRIES = 3  # Maximum number of retries if CAPTCHA is detected
retry_count = 0  # Counter to track retries

while retry_count < MAX_RETRIES:
    try:
        print(f"Starting scraping attempt {retry_count + 1}/{MAX_RETRIES}...")

        # Get a random browser
        driver = get_random_browser()

        # Randomize the browser window size
        driver.set_window_size(random.randint(800, 1920), random.randint(600, 1080))

        # Open the URL
        url = "https://sportsbook.fanduel.com/"
        driver.get(url)
        random_delay(5, 10)

        # Simulate mouse movements
        simulate_mouse_movement(driver)

        # Check for CAPTCHA
        if "px-captcha" in driver.page_source:
            print("CAPTCHA detected! Restarting scrape...")
            retry_count += 1
            driver.quit()
            continue  # Restart the loop to retry scraping

        # Wait for the page to load
        random_delay(5, 10)

        # Get the page source and save it
        html = driver.page_source
        with open("./scraper-out/output_nba_fanduel.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("HTML content saved to 'output_nba_fanduel.html'")
        break  # Exit the loop if scraping is successful

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        retry_count += 1

    finally:
        if 'driver' in locals():
            driver.quit()

if retry_count >= MAX_RETRIES:
    print("Maximum retries reached. Exiting the script.")
