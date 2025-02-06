import requests
from bs4 import BeautifulSoup


HOME_PAGE = "https://grainger.illinois.edu/about/directory/faculty"

NAME_TEMPLATE = """<div class="name"><a href="/about/directory/faculty/abbamont" aria-label="Peter  Abbamonte">Peter  Abbamonte</a></div>"""

def scrape_data():

    home_page_data = requests.get(HOME_PAGE)
    soup = BeautifulSoup(home_page_data.text, "html.parser")
    elements = soup.find_all(class_="my-class")
    links = []

    return