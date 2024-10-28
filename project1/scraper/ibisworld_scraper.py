from playwright.sync_api import sync_playwright
import gspread
from google.oauth2.service_account import Credentials
import logging

def fetch_data_with_playwright():

    data = {
        'company_names': ["McKinsey", "BCG", "Deloitte"],
        'market_reports': [],
        'industry_analysis': [],
        'trends': [],
        'bcg_market_reports': [],
        'deloitte_market_reports': []
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()


        url1 = "https://www.ibisworld.com/us/company/mckinsey-company/8751/"
        page.goto(url1)
        description_section1 = page.inner_text("div#contentPlaceHolder_Body_litCompanyDescription")
        if description_section1:
            print(f"抓取到 McKinsey 的 Market Research 描述: {description_section1}")
            data['market_reports'].append(description_section1)
        else:
            print("未找到 McKinsey 的 Market Research 描述信息！")

        url2 = "https://www.ibisworld.com/united-states/market-research-reports/energy-utility-consulting-services-industry/#IndustryStatisticsAndTrends"
        page.goto(url2)
        try:
            page.wait_for_selector("div#headerIndustrySummary", timeout=10000)
            industry_analysis_section = page.inner_text("div#headerIndustrySummary")
            if industry_analysis_section:
                print(f"抓取到 McKinsey 的 Industry Analysis 描述: {industry_analysis_section}")
                data['industry_analysis'].append(industry_analysis_section)
            else:
                print("未找到 McKinsey 的 Industry Analysis 描述信息！")
        except Exception as e:
            print(f"抓取 McKinsey 的 Industry Analysis 失败: {e}")

        trends_section = page.inner_text("ul.disc.market-size-trends")
        if trends_section:
            print(f"抓取到 McKinsey 的 Trends 描述: {trends_section}")
            data['trends'].append(trends_section)
        else:
            print("未找到 McKinsey 的 Trends 描述信息！")

        url3 = "https://www.ibisworld.com/au/company/boston-consulting-group-pty-ltd/7408/"
        page.goto(url3)
        description_section3 = page.inner_text("div#litCompanyIntroduction")
        if description_section3:
            print(f"抓取到 BCG 的 Market Research 描述: {description_section3}")
            data['bcg_market_reports'].append(description_section3)
        else:
            print("未找到 BCG 的 Market Research 描述信息！")

        url6 = "https://www.ibisworld.com/united-states/market-research-reports/audit-services-industry/#IndustryStatisticsAndTrends"
        page.goto(url6)

        try:
            page.wait_for_selector("div#headerIndustrySummary", timeout=10000)
            audit_industry_analysis = page.inner_text("div#headerIndustrySummary")
            if audit_industry_analysis:
                print(f"抓取到 Audit Services 的 Industry Analysis 描述: {audit_industry_analysis}")
                data['industry_analysis'].append(audit_industry_analysis)  # 覆盖 Deloitte 的数据
            else:
                print("未找到 Audit Services 的 Industry Analysis 描述信息！")
        except Exception as e:
            print(f"抓取 Audit Services 的 Industry Analysis 失败: {e}")

        # 抓取 Audit Services 的 Trends
        audit_trends_section = page.inner_text("ul.disc.market-size-trends")
        if audit_trends_section:
            print(f"抓取到 Audit Services 的 Trends 描述: {audit_trends_section}")
            data['trends'].append(audit_trends_section)  # 覆盖 Deloitte 的数据
        else:
            print("未找到 Audit Services 的 Trends 描述信息！")



        url5 = "https://www.ibisworld.com/us/company/deloitte-touche-tohmatsu/351861/"
        page.goto(url5)
        description_section5 = page.inner_text("div#contentPlaceHolder_Body_litCompanyDescription")
        if description_section5:
            print(f"抓取到 Deloitte 的 Market Research 描述: {description_section5}")
            data['deloitte_market_reports'].append(description_section5)
        else:
            print("未找到 Deloitte 的 Market Research 描述信息！")

        browser.close()

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

        worksheet.update('A1', [["Company Name"]])  # 第一列标题改为 "Company Name"
        worksheet.update('B1', [["Market research reports"]])
        worksheet.update('C1', [["Industry analysis"]])
        worksheet.update('D1', [["Trends"]])

        worksheet.update('A2', [[name] for name in data['company_names']])  # 公司名称写入 A 列

        worksheet.update('B2', [[report] for report in data['market_reports']])
        worksheet.update('C2', [[analysis] for analysis in data['industry_analysis']])
        worksheet.update('D2', [[trend] for trend in data['trends']])
        worksheet.update('B3', [[report] for report in data['bcg_market_reports']])
        worksheet.update('B4', [[report] for report in data['deloitte_market_reports']])
        worksheet.update('C4', [[data['industry_analysis'][-1]]])  # Audit Services 的 Industry Analysis 存入 C4
        worksheet.update('D4', [[data['trends'][-1]]])  # Audit Services 的 Trends 存入 D4
        worksheet.update('C3', [[""]])  # 清空 C3
        worksheet.update('D3', [[""]])

        worksheet.format('A1:Z1000', {'wrapStrategy': 'WRAP'})  # 将 A1:Z1000 范围内的单元格设置为自动换行

        logging.info(f"Data uploaded to {sheet_name} sheet successfully!")
    except Exception as e:
        logging.error(f"Failed to upload data to Google Sheets: {e}")
        print(f"上传到 Google Sheets 失败: {e}")
        # 输出 Google Sheets API 响应
        if hasattr(e, 'response'):
            print(e.response.content)

data = fetch_data_with_playwright()
upload_to_google_sheets(data, "IBISWorld Reports")
