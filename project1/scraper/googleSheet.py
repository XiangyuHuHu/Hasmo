import gspread
from google.oauth2.service_account import Credentials
import logging

# 这里使用你的 JSON 凭据文件路径
GOOGLE_CREDENTIALS_PATH = "O:/Hasmo Intern/Hasmo/project1/webscraper-438102-d39d79165838.json"

def upload_to_google_sheets(data, sheet_name):

    # 验证传入的数据
    if not data or not isinstance(data, dict):
        logging.error("Invalid data format passed to upload_to_google_sheets.")
        return

    required_keys = ['service_offerings', 'case_studies', 'client_testimonials', 'thought_leadership', 'market_insight']

    for key in required_keys:
        if key not in data or data[key] is None:
            logging.error(f"Missing or None data for key: {key}")
            return

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

        worksheet.update('A1', [['Service Offerings']])
        worksheet.update('A2', [[service] for service in data['service_offerings']])

        worksheet.update('B1', [['Case Studies']])
        worksheet.update('B2', [[case] for case in data['case_studies']])

        worksheet.update('C1', [['Client Testimonials']])
        worksheet.update('C2', [[testimonial] for testimonial in data['client_testimonials']])

        worksheet.update('D1', [['Thought Leadership']])
        worksheet.update('D2', [[article] for article in data['thought_leadership']])

        worksheet.update('E1', [['Market Insights']])
        worksheet.update('E2', [[insight] for insight in data['market_insight']])

        logging.info(f"Data uploaded to {sheet_name} sheet successfully!")
    except Exception as e:
        logging.error(f"Failed to upload data to Google Sheets: {e}")
