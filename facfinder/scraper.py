import requests
from bs4 import BeautifulSoup
import os
import multiprocessing
from functools import partial

HOME_PAGE = "https://grainger.illinois.edu/about/directory/faculty"
BASE_URL = "https://grainger.illinois.edu"


def scrape_data():
    home_page_data = requests.get(HOME_PAGE)
    soup = BeautifulSoup(home_page_data.text, "html.parser")
    professor_links = soup.find_all(class_="name")
    professors = {}
    for professor in professor_links:
        professors[professor.get_text().strip()] = professor.find('a').get('href')
    return professors


def fetch_faculty_data(profile_link):
    response = requests.get(BASE_URL + profile_link)
    soup = BeautifulSoup(response.text, "html.parser")
    profile = soup.find(class_="directory-profile maxwidth800").get_text()
    return profile


def save_data(professor, profile, lock, path='../data'):
    os.makedirs(path, exist_ok=True)

    # Write individual profile file
    with open(f'{path}/{professor}.txt', 'w', encoding='utf-8') as file:
        file.write(profile)

    # Thread-safe append to professors list
    with lock:
        with open(f'{path}/professors.txt', 'a', encoding='utf-8') as file:
            file.write(professor + '\n')


def process_professor(name, profile_link, lock):
    try:
        profile = fetch_faculty_data(profile_link)
        save_data(name, profile, lock)
    except Exception as e:
        print(f"Error processing {name}: {str(e)}")


def scrape_professors():
    professors = scrape_data()

    # Create manager for cross-process lock
    manager = multiprocessing.Manager()
    lock = manager.Lock()

    # Create process pool
    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        pool.starmap(
            partial(process_professor, lock=lock),
            professors.items()
        )


if __name__ == '__main__':
    scrape_professors()
