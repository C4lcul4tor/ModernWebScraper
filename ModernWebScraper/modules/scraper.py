
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from modules.utils import load_config
import csv

class WebScraper:
    def __init__(self):
        self.config = load_config()
        self.driver = self.setup_driver()

    def setup_driver(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromeService
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.firefox.options import Options as FirefoxOptions

        browser = self.config["scraper"]["browser"]
        headless = self.config["scraper"]["headless"]
        timeout = self.config["scraper"]["timeout"]

        if browser == "chrome":
            options = ChromeOptions()
            options.headless = headless
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        elif browser == "firefox":
            options = FirefoxOptions()
            options.headless = headless
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        else:
            raise ValueError("Invalid browser specified in config.yaml")

        driver.implicitly_wait(timeout)
        return driver

    def open_page(self, url):
        print(f"Opening URL: {url}")
        self.driver.get(url)

    def extract_products(self):
        wait = WebDriverWait(self.driver, 20)
        products = []
        
        try:
            product_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-card")))
            
            for product in product_elements[:10]:  # Limiting to first 10 products for testing
                try:
                    title = product.find_element(By.CSS_SELECTOR, "h3.product-title").text
                    price = product.find_element(By.CSS_SELECTOR, "span.product-price").text
                    link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

                    products.append({
                        "Title": title,
                        "Price": price,
                        "Link": link
                    })

                except Exception as e:
                    print(f"Error extracting product: {e}")
        
        except Exception as e:
            print(f"Error finding products: {e}")

        return products

    def save_to_csv(self, data):
        file_path = "data/scraped_data.csv"
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Title", "Price", "Link"])
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {file_path}")

    def close_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = WebScraper()
    target_url = scraper.config["scraper"]["target_url"]
    scraper.open_page(target_url)
    time.sleep(5)  # Wait for page to load
    products = scraper.extract_products()
    scraper.save_to_csv(products)
    scraper.close_driver()
