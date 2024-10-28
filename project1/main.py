
from scraper.mckinsey_scraper import fetch_mckinsey_data
from scraper.bcg_scraper import fetch_bcg_data
from scraper.deloitte_scraper import fetch_deloitte_data
from scraper.googleSheet import upload_to_google_sheets


def main():
    # 抓取 McKinsey 数据
    mckinsey_data = fetch_mckinsey_data()

    # 抓取 BCG 数据
    bcg_data = fetch_bcg_data()

    # 抓取 Deloitte 数据
    deloitte_data = fetch_deloitte_data()



    # 将数据上传到不同的 Google Sheets 工作表
    if mckinsey_data:
        upload_to_google_sheets(mckinsey_data, sheet_name="McKinsey")
    if bcg_data:
        upload_to_google_sheets(bcg_data, sheet_name="BCG")
    if deloitte_data:
        upload_to_google_sheets(deloitte_data, sheet_name="Deloitte")



if __name__ == "__main__":
    main()


