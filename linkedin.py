import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
"""
l = []
o = {}
k = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

# Update the target URL with the desired keyword and location
keyword = ""  # Replace with your desired keyword or hashtag
location = "India"  # Replace with your desired location
target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location={}&geoId=100293800&currentJobId=3415227738&start={}'

for i in range(0, math.ceil(117/25)):
    res = requests.get(target_url.format(keyword, location, i))
    soup = BeautifulSoup(res.text, 'html.parser')
    alljobs_on_this_page = soup.find_all("li")
    print(len(alljobs_on_this_page))
    for x in range(0, len(alljobs_on_this_page)):
        jobid = alljobs_on_this_page[x].find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
        l.append(jobid)

target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

for j in range(0, len(l)):
    resp = requests.get(target_url.format(l[j]))
    soup = BeautifulSoup(resp.text, 'html.parser')

    try:
        o["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        o["company"] = None

    try:
        o["job-title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
    except:
        o["job-title"] = None

    try:
        o["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace(
            "Seniority level", "").strip()
    except:
        o["level"] = None

    hashtags = soup.find_all("a", {"class": "hashtag-link"})
    o["hashtags"] = [tag.text.strip() for tag in hashtags]

    k.append(o)
    o = {}

df = pd.DataFrame(k)
df.to_csv('linkedinjobs.csv', index=False, encoding='utf-8')
print(k)
"""
import requests
from bs4 import BeautifulSoup
import math
import pandas as pd


def scrape_linkedin(keyword, location="India"):
    l = []
    o = {}
    k = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    # Update the target URL with the desired keyword and location
    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location={}&geoId=100293800&currentJobId=3415227738&start={}'

    for i in range(0, math.ceil(117/25)):
        res = requests.get(target_url.format(keyword, location, i))
        soup = BeautifulSoup(res.text, 'html.parser')
        alljobs_on_this_page = soup.find_all("li")
        print(len(alljobs_on_this_page))
        for x in range(0, len(alljobs_on_this_page)):
            jobid = alljobs_on_this_page[x].find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
            l.append(jobid)

    target_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

    for j in range(0, len(l)):
        resp = requests.get(target_url.format(l[j]))
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            o["company"] = soup.find("div", {"class": "top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            o["company"] = None

        try:
            o["job-title"] = soup.find("div", {"class": "top-card-layout__entity-info"}).find("a").text.strip()
        except:
            o["job-title"] = None

        try:
            o["level"] = soup.find("ul", {"class": "description__job-criteria-list"}).find("li").text.replace(
                "Seniority level", "").strip()
        except:
            o["level"] = None

        hashtags = soup.find_all("a", {"class": "hashtag-link"})
        o["hashtags"] = [tag.text.strip() for tag in hashtags]

        k.append(o)
        o = {}

    # Store data in Firebase

    df = pd.DataFrame(k)
    return df.to_dict('records')
