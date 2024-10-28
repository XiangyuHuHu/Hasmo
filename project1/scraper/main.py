from mckinsey_scraper import fetch_mckinsey_data
from bcg_scraper import fetch_bcg_data
from deloitte_scraper import fetch_deloitte_data
from googleSheet import upload_to_google_sheets


def main():
    mckinsey_data = fetch_mckinsey_data()

    bcg_data = fetch_bcg_data()

    deloitte_data = fetch_deloitte_data()

    if mckinsey_data:
        upload_to_google_sheets(mckinsey_data, sheet_name="McKinsey")
    if bcg_data:
        upload_to_google_sheets(bcg_data, sheet_name="BCG")
    if deloitte_data:
        upload_to_google_sheets(deloitte_data, sheet_name="Deloitte")



if __name__ == "__main__":
    main()


