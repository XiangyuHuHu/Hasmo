import requests
from bs4 import BeautifulSoup


def fetch_mckinsey_data():

    data1 = {
        'service_offerings': [],
        'case_studies': [],
        'client_testimonials': [],
        'thought_leadership': [],
        'market_insight': []
    }

    exclude_list = ["Skip to main content", "Contact", ""]

    service_url1 = "https://www.mckinsey.com/locations/mckinsey-client-capabilities-network/our-work"
    service_page1 = requests.get(service_url1)

    if service_page1.status_code == 200:
        service_soup1 = BeautifulSoup(service_page1.text, 'html.parser')
        service_section1 = service_soup1.find_all('a')

        for service in service_section1:
            text = service.get_text().strip()
            if text and text not in exclude_list:
                data1['service_offerings'].append(text)
    else:
        print(f"Failed to fetch service offerings, status code: {service_page1.status_code}")

    # McKinsey Case Studies
    case_url1 = 'https://www.mckinsey.com/about-us/case-studies'
    case_page1 = requests.get(case_url1)

    if case_page1.status_code == 200:
        case_soup1 = BeautifulSoup(case_page1.text, 'html.parser')
        case_section1 = case_soup1.find_all('h5')
        for case in case_section1:
            data1['case_studies'].append(case.get_text().strip())
    else:
        print(f"Failed to fetch case studies, status code: {case_page1.status_code}")

    # McKinsey Thought Leadership
    leadership_url1 = "https://www.mckinsey.com/featured-insights/leadership"
    leadership_page1 = requests.get(leadership_url1)

    if leadership_page1.status_code == 200:
        leadership_soup1 = BeautifulSoup(leadership_page1.text, 'html.parser')
        leadership_section1 = leadership_soup1.find_all('h5')
        for leadership in leadership_section1:
            data1["thought_leadership"].append(leadership.get_text().strip())
    else:
        print(f"Failed to fetch thought leadership, status code: {leadership_page1.status_code}")

    # McKinsey Client Testimonials
    client_url1 = 'https://www.mckinsey.com/capabilities/growth-marketing-and-sales/how-we-help-clients/impact-stories'
    client_page1 = requests.get(client_url1)

    if client_page1.status_code == 200:
        client_soup1 = BeautifulSoup(client_page1.text, 'html.parser')
        client_section1 = client_soup1.find_all('div', class_="mck-u-links-inline mck-c-generic-item__description")
        for testimony in client_section1:
            data1["client_testimonials"].append(testimony.get_text().strip())
    else:
        print(f"Failed to fetch client testimonials, status code: {client_page1.status_code}")

    # McKinsey Market Insights
    market_url1 = "https://www.mckinsey.com/capabilities/growth-marketing-and-sales/how-we-help-clients/insights-and-analytics"
    market_page1 = requests.get(market_url1)

    if market_page1.status_code == 200:
        market_soup1 = BeautifulSoup(market_page1.text, 'html.parser')
        market_section1 = market_soup1.find_all('p')
        for market in market_section1:
            data1["market_insight"].append(market.get_text().strip())
    else:
        print(f"Failed to fetch market insights, status code: {market_page1.status_code}")

    return data1

