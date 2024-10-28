import scrapy
from scrapy.crawler import CrawlerProcess
import gspread
from google.oauth2.service_account import Credentials
import logging



class MarketDataSpider(scrapy.Spider):
    name = "market_data_spider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 2,  # Delay to reduce server load
    }

    # URLs for McKinsey, BCG, and Deloitte articles
    start_urls = [
        # McKinsey URLs
        "https://www.reuters.com/technology/artificial-intelligence/portugal-could-boost-productivity-if-third-workforce-trained-ai-study-shows-2024-10-21/",
        "https://www.reuters.com/technology/artificial-intelligence/microsoft-allow-autonomous-ai-agent-development-starting-next-month-2024-10-21/",
        "https://www.reuters.com/business/finance/europes-banks-under-investor-pressure-keep-earnings-growth-alive-2024-10-21/",
        "https://www.reuters.com/business/us-lawmakers-ask-justice-defense-departments-probe-mckinsey-review-contracts-2024-10-18/",

        # BCG URLs
        "https://www.reuters.com/business/finance/singapore-banks-expect-lower-rates-china-stimulus-boost-wealth-business-2024-10-14/",
        "https://www.reuters.com/markets/bank-valuations-could-rise-by-7-trillion-five-years-study-finds-2024-01-15/",
        "https://www.reuters.com/business/autos-transportation/hybrid-electric-car-sales-outpace-rest-market-brazil-2030-study-shows-2024-09-27/",
        "https://www.reuters.com/technology/space/taiwanese-rocket-startup-may-be-early-test-japans-space-hub-plans-2024-07-25/",

        # Deloitte URLs
        "https://www.reuters.com/markets/commodities/eu-set-choose-firm-critical-minerals-joint-buying-platform-2024-10-21/",
        "https://www.reuters.com/markets/bank-canada-likely-trim-rates-again-boost-economic-growth-2024-09-04/",
        "https://www.reuters.com/world/uk/geopolitics-dents-big-uk-businesses-optimism-deloitte-says-2024-10-13/",
        "https://www.reuters.com/markets/us/us-holiday-sales-grow-up-35-2024-nrf-forecasts-2024-10-15/"
    ]

    def parse(self, response):
        # Determine the company and content type
        company, content_type = self.identify_content_type(response.url)
        paragraphs = response.css('div[data-testid^="paragraph"]::text').getall()
        content = ' '.join(paragraphs).strip()

        # Output data
        if content:
            yield {
                'company': company,
                'content_type': content_type,
                'content': content
            }

    def identify_content_type(self, url):
        if "mckinsey" in url.lower():
            company = "McKinsey"
        elif "bcg" in url.lower():
            company = "BCG"
        elif "deloitte" in url.lower():
            company = "Deloitte"
        else:
            company = "Unknown"

        if "latest" in url.lower():
            content_type = "latest_news"
        elif "market" in url.lower():
            content_type = "market_reports"
        elif "finance" in url.lower():
            content_type = "financial_analysis"
        elif "trends" in url.lower():
            content_type = "global_trends"
        else:
            content_type = "unknown"

        return company, content_type


class GoogleSheetsPipeline:
    def __init__(self):
        # Authenticate with Google Sheets
        creds_path = "O:/Hasmo Intern/Hasmo/project1/webscraper-438102-d39d79165838.json"  # Adjust path to your credentials file
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open("Market Research Data").worksheet("Reuters Data test")

        # Prepare headers
        self.sheet.update('A1',
                          [["Company Name", "Latest News", "Market Reports", "Financial Analysis", "Global Trends"]])
        self.row_map = {"McKinsey": 2, "BCG": 3, "Deloitte": 4}
        self.col_map = {'latest_news': 'B', 'market_reports': 'C', 'financial_analysis': 'D', 'global_trends': 'E'}

    def process_item(self, item):
        # Update Google Sheet based on item content type and company
        row = self.row_map.get(item['company'], None)
        col = self.col_map.get(item['content_type'], None)
        if row and col:
            self.sheet.update(f"{col}{row}", item['content'])
        return item


def run_spider():
    # Set up the Scrapy process
    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            '__main__.GoogleSheetsPipeline': 1,
        }
    })
    process.crawl(MarketDataSpider)
    process.start()


if __name__ == "__main__":
    run_spider()
