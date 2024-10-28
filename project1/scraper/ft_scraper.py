from googleSheet1 import upload_to_google_sheets  # Import from the unified file
import requests
from bs4 import BeautifulSoup


def fetch_ft_data():
    """Scrape FT website for latest news, market reports, financial analysis, and global trends."""

    data_ft = {
        "latest_news": [],
        "market_reports": [],
        "financial_analysis": [],
        "global_trends": []
    }

    # FT Latest News
    news_url = "https://www.ft.com/global-economy"
    news_page = requests.get(news_url)
    if news_page.status_code == 200:
        news_soup = BeautifulSoup(news_page.text, 'html.parser')
        news_section = news_soup.find_all('h3', class_="o-teaser__heading")
        for news in news_section:
            data_ft['latest_news'].append(news.get_text().strip())

    return data_ft


def main():
    ft_data = fetch_ft_data()
    upload_to_google_sheets(ft_data, spreadsheet_name="googleSheet1", sheet_name="FT Data")


if __name__ == "__main__":
    main()
