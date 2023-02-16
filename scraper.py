import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    with open('links.txt', 'r') as f:
        url_list = f.read().split('\n')

    all_data = []

    for idx, url in enumerate(url_list):
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")

        with open(f'pumping/{idx}.txt', 'w') as pumping_f:
            pumping_f.write(str(soup))

        with open('index.txt', 'a') as f:
            f.write(f'{idx} {url}\n')



