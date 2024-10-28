import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import logging

def fetch_market_data():

    url1 = "https://www.marketresearch.com/MarketLine-v3883/McKinsey-Company-Strategy-SWOT-Corporate-35743855/"
    url2 = "https://www.marketresearch.com/Mordor-Intelligence-LLP-v4018/Human-Capital-Advisory-Services-Size-37849199/"
    url3 = "https://www.marketresearch.com/GlobalData-v3648/McKinsey-Strategic-SWOT-Review-38415285/"

    url4 = "https://www.marketresearch.com/GlobalData-v3648/Boston-Consulting-Group-Strategic-SWOT-38024543/"
    url5 = "https://www.marketresearch.com/MarketLine-v3883/Boston-Consulting-Group-Strategy-SWOT-35300094/"
    url6 = "https://www.marketresearch.com/Mordor-Intelligence-LLP-v4018/Consulting-Service-Size-Share-Growth-36998438/"

    url7 = "https://www.marketresearch.com/GlobalData-v3648/Deloitte-Touche-Tohmatsu-Strategic-SWOT-38415353/"
    url8 = "https://www.marketresearch.com/MarketLine-v3883/Deloitte-Touche-Tohmatsu-Limited-Company-36354982/"
    url9 = "https://www.marketresearch.com/Venture-Planning-Group-v3447/Deloitte-Performance-Capabilities-Goals-Strategies-36257903/"
    url10 = "https://www.marketresearch.com/Mordor-Intelligence-LLP-v4018/Consulting-Service-Size-Share-Growth-36998438/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    data = {
        'company_names': ["McKinsey", "BCG", "Deloitte"],
        'market_reports': [],  # McKinsey 的数据
        'trends': [],  # Human Capital 的数据
        'industry_analysis': [],  # McKinsey 的 Industry Analysis
        'bcg_market_reports': [],  # BCG 的 Market Reports
        'bcg_trends': [],  # BCG 的 Trend
        'bcg_industry_analysis': [],  # BCG 的 Industry Analysis
        'deloitte_market_reports': [],  # Deloitte 的 Market Reports
        'deloitte_trends': [],  # Deloitte 的 Trend
        'deloitte_industry_analysis': [],  # Deloitte 的 Industry Analysis
        'deloitte_statistics': []  # Deloitte 的 Statistics
    }

    # 抓取并存储每个 URL 的数据
    urls_and_keys = [
        (url1, 'market_reports'), (url2, 'trends'), (url3, 'industry_analysis'),
        (url4, 'bcg_industry_analysis'), (url5, 'bcg_market_reports'), (url6, 'bcg_trends'),
        (url7, 'deloitte_market_reports'), (url8, 'deloitte_industry_analysis'), (url9, 'deloitte_statistics'), (url10, 'deloitte_trends')
    ]

    for url, key in urls_and_keys:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        description_section = soup.find('div', id='description')
        if description_section:
            description_text = description_section.get_text(separator=' ').strip()
            data[key].append(description_text)
            print(f"抓取到 {key} 的数据: {description_text[:100]}...")
        else:
            print(f"未找到 {key} 的描述信息！")

    return data


def upload_to_google_sheets(data, sheet_name):

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
        worksheet.update('B1', [["Market research reports"]])
        worksheet.update('C1', [["Industry analysis"]])
        worksheet.update('D1', [["Statistics"]])
        worksheet.update('E1', [["Trends"]])

        worksheet.update('A2', [[name] for name in data['company_names']])

        worksheet.update('B2', [[report] for report in data['market_reports']])
        worksheet.update('C2', [[analysis] for analysis in data['industry_analysis']])
        worksheet.update('E2', [[trend] for trend in data['trends']])

        worksheet.update('B3', [[report] for report in data['bcg_market_reports']])
        worksheet.update('C3', [[analysis] for analysis in data['bcg_industry_analysis']])
        worksheet.update('E3', [[trend] for trend in data['bcg_trends']])

        worksheet.update('B4', [[report] for report in data['deloitte_market_reports']])
        worksheet.update('C4', [[analysis] for analysis in data['deloitte_industry_analysis']])
        worksheet.update('D4', [[stat] for stat in data['deloitte_statistics']])
        worksheet.update('E4', [[trend] for trend in data['deloitte_trends']])

        worksheet.format('A1:Z1000', {'wrapStrategy': 'WRAP'})

        logging.info(f"Data uploaded to {sheet_name} sheet successfully!")
    except Exception as e:
        logging.error(f"Failed to upload data to Google Sheets: {e}")


market_data = fetch_market_data()
upload_to_google_sheets(market_data, "Market Research Reports")
