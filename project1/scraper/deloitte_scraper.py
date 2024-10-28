import requests
from bs4 import BeautifulSoup


def fetch_deloitte_data():


    data3 = {
        "service_offerings": [],
        "case_studies": [],
        "client_testimonials": [],
        "thought_leadership": [],
        "market_insight": []
    }

    # Deloitte Service Offerings
    service_url3 = "https://www2.deloitte.com/us/en.html"
    service_page3 = requests.get(service_url3)
    if service_page3.status_code == 200:
        service_soup3 = BeautifulSoup(service_page3.text, 'html.parser')
        service_section3 = service_soup3.find_all('li', class_="cmp-pr-nav__menu__item")
        for service in service_section3:
            data3['service_offerings'].append(service.get_text().strip())

    # Deloitte Case Studies
    case_url3 = 'https://www.deloitte.com/an/en/what-we-do/case-studies.html'
    case_page3 = requests.get(case_url3)
    if case_page3.status_code == 200:
        case_soup3 = BeautifulSoup(case_page3.text, 'html.parser')
        case_section3 = case_soup3.find_all('div', class_='cmp-promo__content__desc')
        for cases in case_section3:
            data3['case_studies'].append(cases.get_text().strip())

    # Deloitte Client Testimonials
    client_url3 = "https://www.deloitte.com/global/en/services/risk-advisory/collections/gra-client-stories.html"
    client_page3 = requests.get(client_url3)
    if client_page3.status_code == 200:
        client_soup3 = BeautifulSoup(client_page3.text, 'html.parser')
        client_section3 = client_soup3.find_all('div', class_="cmp-promo__content__desc")
        for testimonies in client_section3:
            data3["client_testimonials"].append(testimonies.get_text().strip())

    # Deloitte Thought Leadership
    leadership_url3 = "https://www2.deloitte.com/ro/en/pages/about-deloitte/articles/deloitte-thought-leadership.html"
    leadership_page3 = requests.get(leadership_url3)
    if leadership_page3.status_code == 200:
        leadership_soup3 = BeautifulSoup(leadership_page3.text, 'html.parser')
        leadership_section3 = leadership_soup3.find_all('a', class_="anchor-new-window")
        for leadership in leadership_section3:
            data3["thought_leadership"].append(leadership.get_text().strip())

    # Deloitte Market Insights
    market_url3 = "https://www2.deloitte.com/us/en/insights.html"
    market_page3 = requests.get(market_url3)
    if market_page3.status_code == 200:
        market_soup3 = BeautifulSoup(market_page3.text, 'html.parser')
        market_section3 = market_soup3.find_all('h3')
        for market in market_section3:
            data3["market_insight"].append(market.get_text().strip())

    return data3
