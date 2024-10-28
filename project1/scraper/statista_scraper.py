import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
import logging

def fetch_statista_data():

    url = "https://www.statista.com/statistics/190343/leading-us-consulting-firms-by-overall-prestige-2011/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    data = {
        'company_names': ["McKinsey & Company"],
        'statistics': []
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        mckinsey_score = soup.find('text', style="font-size:15px;font-weight:bold;color:#454F44;cursor:pointer;")
        if mckinsey_score:
            mckinsey_value = mckinsey_score.get_text(separator=' ').strip()
            print(f"抓取到 McKinsey & Company 的 Statistics 数据: {mckinsey_value}")
            data['statistics'].append(mckinsey_value)
        else:
            print("未找到 McKinsey & Company 的 Statistics 数据信息！")
    else:
        print(f"请求失败，状态码: {response.status_code}")

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
        worksheet.update('D1', [["Statistics"]])


        worksheet.update('A2', [[name] for name in data['company_names']])


        worksheet.update('D2', [[stat] for stat in data['statistics']])
        worksheet.format('A1:Z1000', {'wrapStrategy': 'WRAP'})

        logging.info(f"Data uploaded to {sheet_name} sheet successfully!")
    except Exception as e:
        logging.error(f"Failed to upload data to Google Sheets: {e}")

statista_data = fetch_statista_data()
upload_to_google_sheets(statista_data, "Statista Reports")
