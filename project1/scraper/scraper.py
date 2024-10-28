import requests
from bs4 import BeautifulSoup
import logging

def fetch_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"Successfully fetched content from {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching {url}: {e}")
        return None

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    data = {
        "service_offerings": [],
        "case_studies": [],
        "client_testimonials": [],
        "thought_leadership": [],
        "market_insights": []
    }

    try:
        for offering in soup.select('.service-title'):
            data['service_offerings'].append(offering.get_text())
    except Exception as e:
        logging.error(f"Error parsing service offerings: {e}")

    try:
        for case in soup.select('.case-study-title'):
            data['case_studies'].append(case.get_text())
    except Exception as e:
        logging.error(f"Error parsing case studies: {e}")

    return data
