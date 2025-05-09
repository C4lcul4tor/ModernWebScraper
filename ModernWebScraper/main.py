
from modules.scraper import WebScraper

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.open_page("https://example.com")
    scraper.close_driver()
