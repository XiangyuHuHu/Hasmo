from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import gspread
from google.oauth2.service_account import Credentials
import logging
import time


def setup_driver():
    chrome_service = Service(executable_path='O:/chromedriver/chromedriver.exe')  # 修改为你的 chromedriver 路径
    chrome_options = Options()

    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-web-security')

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver


def fetch_reuters_data(url):
    """使用 Selenium 抓取 Reuters 的内容"""
    driver = setup_driver()
    try:
        driver.get(url)
        time.sleep(5)

        # 抓取页面中的段落
        paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid^="paragraph"]')
        if not paragraphs:
            print("未找到内容！")
            return ""

        # 将段落合并为单个字符串
        content_list = [item.text.strip() for item in paragraphs]
        content = ' '.join(content_list)
        print(f"抓取内容: {content}")
        return content
    except Exception as e:
        print(f"抓取数据失败: {e}")
        return ""
    finally:
        driver.quit()


def upload_to_google_sheets(mckinsey_data, bcg_data, deloitte_data, sheet_name):
    GOOGLE_CREDENTIALS_PATH = "O:/Hasmo Intern/Hasmo/project1/webscraper-438102-d39d79165838.json"
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_PATH, scopes=scope)
    client = gspread.authorize(creds)

    try:
        sheet = client.open("Market Research Data")
        try:
            worksheet = sheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=sheet_name, rows="100", cols="20")

        worksheet.update('A1', [["Company Name"]])
        worksheet.update('A2', [["Mckinsey"]])
        worksheet.update('A3', [["BCG"]])
        worksheet.update('A4', [["Deloitte"]])
        worksheet.update('B1', [["Latest News"]])
        worksheet.update('C1', [["Market Reports"]])
        worksheet.update('D1', [["Financial Analysis"]])
        worksheet.update('E1', [["Global Economic Trends"]])

        worksheet.update('B2', [[mckinsey_data.get('McKinsey_latest_news', '')]])
        worksheet.update('C2', [[mckinsey_data.get('McKinsey_market_reports', '')]])
        worksheet.update('D2', [[mckinsey_data.get('McKinsey_financial_analysis', '')]])
        worksheet.update('E2', [[mckinsey_data.get('McKinsey_global_trends', '')]])

        worksheet.update('B3', [[bcg_data.get('BCG_latest_news', '')]])
        worksheet.update('C3', [[bcg_data.get('BCG_market_reports', '')]])
        worksheet.update('D3', [[bcg_data.get('BCG_financial_analysis', '')]])
        worksheet.update('E3', [[bcg_data.get('BCG_global_trends', '')]])

        worksheet.update('B4', [[deloitte_data.get('Deloitte_latest_news', '')]])
        worksheet.update('C4', [[deloitte_data.get('Deloitte_market_reports', '')]])
        worksheet.update('D4', [[deloitte_data.get('Deloitte_financial_analysis', '')]])
        worksheet.update('E4', [[deloitte_data.get('Deloitte_global_trends', '')]])

        worksheet.format('A1:Z1000', {'wrapStrategy': 'WRAP'})

        logging.info(f"Data uploaded to {sheet_name} sheet successfully!")
    except Exception as e:
        logging.error(f"Failed to upload data to Google Sheets: {e}")
        print(f"上传到 Google Sheets 失败: {e}")



def main():
    mckinsey_news = fetch_reuters_data(
        "https://www.reuters.com/technology/artificial-intelligence/portugal-could-boost-productivity-if-third-workforce-trained-ai-study-shows-2024-10-21/")
    mckinsey_reports = fetch_reuters_data(
        "https://www.reuters.com/technology/artificial-intelligence/microsoft-allow-autonomous-ai-agent-development-starting-next-month-2024-10-21/")
    mckinsey_financial = fetch_reuters_data(
        "https://www.reuters.com/business/finance/europes-banks-under-investor-pressure-keep-earnings-growth-alive-2024-10-21/")
    mckinsey_trends = fetch_reuters_data(
        "https://www.reuters.com/business/us-lawmakers-ask-justice-defense-departments-probe-mckinsey-review-contracts-2024-10-18/")


    bcg_news = fetch_reuters_data(
        "https://www.reuters.com/business/finance/singapore-banks-expect-lower-rates-china-stimulus-boost-wealth-business-2024-10-14/")
    bcg_reports = fetch_reuters_data(
        "https://www.reuters.com/markets/bank-valuations-could-rise-by-7-trillion-five-years-study-finds-2024-01-15/")
    bcg_financial = fetch_reuters_data(
        "https://www.reuters.com/business/autos-transportation/hybrid-electric-car-sales-outpace-rest-market-brazil-2030-study-shows-2024-09-27/")
    bcg_trends = fetch_reuters_data(
        "https://www.reuters.com/technology/space/taiwanese-rocket-startup-may-be-early-test-japans-space-hub-plans-2024-07-25/")


    deloitte_news = fetch_reuters_data(
        "https://www.reuters.com/markets/commodities/eu-set-choose-firm-critical-minerals-joint-buying-platform-2024-10-21/")
    deloitte_reports = fetch_reuters_data(
        "https://www.reuters.com/markets/bank-canada-likely-trim-rates-again-boost-economic-growth-2024-09-04/")
    deloitte_financial = fetch_reuters_data(
        "https://www.reuters.com/world/uk/geopolitics-dents-big-uk-businesses-optimism-deloitte-says-2024-10-13/")
    deloitte_trends = fetch_reuters_data(
        "https://www.reuters.com/markets/us/us-holiday-sales-grow-up-35-2024-nrf-forecasts-2024-10-15/")


    mckinsey_data = {
        'McKinsey_latest_news': mckinsey_news,
        'McKinsey_market_reports': mckinsey_reports,
        'McKinsey_financial_analysis': mckinsey_financial,
        'McKinsey_global_trends': mckinsey_trends
    }


    bcg_data = {
        'BCG_latest_news': bcg_news,
        'BCG_market_reports': bcg_reports,
        'BCG_financial_analysis': bcg_financial,
        'BCG_global_trends': bcg_trends
    }


    deloitte_data = {
        'Deloitte_latest_news': deloitte_news,
        'Deloitte_market_reports': deloitte_reports,
        'Deloitte_financial_analysis': deloitte_financial,
        'Deloitte_global_trends': deloitte_trends
    }

    upload_to_google_sheets(mckinsey_data, bcg_data, deloitte_data, sheet_name="Reuters Data")


if __name__ == "__main__":
    main()
