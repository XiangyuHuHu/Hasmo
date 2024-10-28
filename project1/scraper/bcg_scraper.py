import requests
from bs4 import BeautifulSoup


def fetch_bcg_data():
    data2 = {
        "service_offerings": [],
        "case_studies": [],
        "client_testimonials": [],
        "thought_leadership": [],
        "market_insight": []
    }

    # BCG Service Offerings
    service_url2 = "https://www.bcg.com/capabilities"
    service_page2 = requests.get(service_url2)
    if service_page2.status_code == 200:
        service_soup2 = BeautifulSoup(service_page2.text, 'html.parser')
        service_section2 = service_soup2.find_all('p', class_="featured-collection__title")
        for service in service_section2:
            data2['service_offerings'].append(service.get_text().strip())

    # BCG Client Testimonials
    client_url2 = "https://www.bcg.com/capabilities/digital-technology-data/client-success"
    client_page2 = requests.get(client_url2)
    if client_page2.status_code == 200:
        client_soup2 = BeautifulSoup(client_page2.text, 'html.parser')
        client_section2 = client_soup2.find_all('div', class_="article-block__body")
        for testimonies in client_section2:
            data2["client_testimonials"].append(testimonies.get_text().strip())

    # BCG Thought Leadership
    leadership_url2 = "https://www.bcg.com/capabilities/business-transformation/insights"
    leadership_page2 = requests.get(leadership_url2)
    if leadership_page2.status_code == 200:
        leadership_soup2 = BeautifulSoup(leadership_page2.text, 'html.parser')
        leadership_section2 = leadership_soup2.find_all('div', class_='article-block__body')
        for leadership in leadership_section2:
            data2["thought_leadership"].append(leadership.get_text().strip())

    # BCG Market Insights
    market_url2 = "https://www.bcg.com/capabilities/marketing-sales/insights"
    market_page2 = requests.get(market_url2)
    if market_page2.status_code == 200:
        market_soup2 = BeautifulSoup(market_page2.text, 'html.parser')
        market_section2 = market_soup2.find_all('h2', class_='item-title')
        for market in market_section2:
            data2["market_insight"].append(market.get_text().strip())

    return data2
