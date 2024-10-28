from playwright.sync_api import sync_playwright
import gspread
from google.oauth2.service_account import Credentials
import logging

# 使用 Playwright 抓取 Bloomberg 最新新闻
def fetch_bloomberg_latest_news():

    data = {
        'latest_news': [],
        'market_reports': [],
        'financial_analysis': [],
        'global_trends': []
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "https://www.bloomberg.com/latest"
        page.goto(url)


        page.wait_for_selector('a.LineupContentArchiveFiltered_storyLink', timeout=60000)

        try:

            news_items = page.query_selector_all('a.LineupContentArchiveFiltered_storyLink')

            for item in news_items:
                title = item.inner_text().strip()

                print(f"新闻标题: {title}")

                data['latest_news'].append(title)
                data['market_reports'].append("")  # 示例：没有 Market Reports 的相关内容可以填充空字符串
                data['financial_analysis'].append("")  # 示例：没有 Financial Analysis 的相关内容可以填充空字符串
                data['global_trends'].append("")  # 示例：没有 Global Trends 的相关内容可以填充空字符串

        except Exception as e:
            print(f"抓取新闻数据失败: {e}")

        browser.close()

    return data


def upload_to_google_sheets(data, sheet_name):
    """将提取到的 Bloomberg 最新新闻数据上传到 Google Sheets"""

    GOOGLE_CREDENTIALS_PATH = "O:/Hasmo Intern/Hasmo/project1/webscraper-438102-d39d79165838.json"

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=scope)
    client = gspread.authorize(creds)

    try:

        sheet = client.open("Bloomberg Latest News Data")
        try:
            worksheet = sheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=sheet_name, rows="100", cols="20")


        worksheet.update('A1', [["Latest News"]])
        worksheet.update('B1', [["Market Reports"]])
        worksheet.update('C1', [["Financial Analysis"]])
        worksheet.update('D1', [["Global Economic Trends"]])


        worksheet.update('A2', [[news] for news in data['latest_news']])
        worksheet.update('B2', [[report] for report in data['market_reports']])
        worksheet.update('C2', [[analysis] for analysis in data['financial_analysis']])
        worksheet.update('D2', [[trend] for trend in data['global_trends']])

        logging.info(f"News data uploaded to {sheet_name} sheet successfully!")
    except Exception as e:
        logging.error(f"Failed to upload data to Google Sheets: {e}")
        print(f"上传到 Google Sheets 失败: {e}")
        if hasattr(e, 'response'):
            print(e.response.content)

data = fetch_bloomberg_latest_news()
upload_to_google_sheets(data, "Latest News")
