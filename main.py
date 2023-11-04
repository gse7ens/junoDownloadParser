import requests
from bs4 import BeautifulSoup
import csv


HOST = "https://www.junodownload.com/"
url = "https://www.junodownload.com/labels/A+State+Of+Trance+Holland/"
urls = ["https://www.junodownload.com/labels/A+State+Of+Trance+Holland/"]
CSV = "releases.csv"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="row gutters-sm jd-listing-item")
    releases = []
    for item in items:
        releases.append(
            {
                "artist": item.find("div", class_="col juno-artist").get_text(),
                "title": item.find("a", class_="juno-title").get_text(),
                "cat_no": item.find("div", class_="text-sm text-muted mt-3").get_text()
            }
        )
    return releases


def get_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    pages = soup.find_all("a", class_="dropdown-item")
    last_page = pages[-1]
    target_value = int(last_page.text)
    x = 0
    while x < target_value:
        x += 1
        urls.append(url + str(x))
    return target_value

html = get_html(url)
pages = get_urls(html.text)


def save_doc(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["artist", "title", "cat_no"])
        for item in items:
            writer.writerow([item["artist"], item["title"], item["cat_no"]])


releases = []
for url in urls:
    print("Parsing " + url)
    html = get_html(url)
    releases.extend(get_content(html.text))

save_doc(releases, CSV)
