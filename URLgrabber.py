import requests
import time
from bs4 import BeautifulSoup

# Returns an array of 30 phishing website URLs from the website OpenPhish hosted on their page.
# This provides a live array of discovered phishing websites, but it only provides 30 at a time
def grabLivePhishingURLs():
    URL_feed = "https://openphish.com/"

    response = requests.get(URL_feed)

    if (response.status_code == 200):
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text()
        phishing_urls = [url for url in all_text.split() if url.startswith('http') or url.startswith('www')]

        return phishing_urls
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Returns an array of 500 phishing website URLs from the website OpenPhish hosted on their feed.text page.
# This provides a larger feed of discovered phishing websites with an array size of 500
def grabLongPhishingURLs():
    URL_feed = "https://openphish.com/feed.txt"

    response = requests.get(URL_feed)

    if (response.status_code == 200):
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text()
        phishing_urls = [url for url in all_text.split() if url.startswith('http') or url.startswith('www')]

        return phishing_urls
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    
def readBenignURLs(filename):
    urls = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                url = line.strip()  # Remove leading and trailing whitespaces
                urls.append(url)
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
    except Exception as e:
        print(f"Error: {e}")
    return urls


def main():
    phishing_urls = grabLivePhishingURLs()

    if phishing_urls:
       for url in phishing_urls:
           print(url)
    
    return phishing_urls

if __name__ == "__main__":
    main()