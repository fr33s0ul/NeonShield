import requests
import bs4
from datetime import datetime, timedelta


def search_cves(cves, search_term):
    return [cve for cve in cves if search_term.lower() in cve["description"].lower()]


def fetch_data():
    url = "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml"
    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.content, "xml")
    items = soup.findAll("item")
    cves = []

    for item in items:
        cve = {}
        cve["title"] = item.title.text
        cve["link"] = item.link.text
        cve["description"] = item.description.text
        pubDate_tag = item.find("pubDate")
        if pubDate_tag is not None:
            cve["published_date"] = datetime.strptime(pubDate_tag.text, '%a, %d %b %Y %H:%M:%S %Z')
        else:
            cve["published_date"] = "N/A"  # Assigning a default value if pubDate doesn't exist.
        lastModified_tag = item.find("lastModifiedDate")
        if lastModified_tag is not None:
            cve["last_modified_date"] = datetime.strptime(lastModified_tag.text, '%a, %d %b %Y %H:%M:%S %Z')
        else:
            cve["last_modified_date"] = datetime.now()  # Use current time if lastModified doesn't exist.
        cves.append(cve)
    return cves

def display_vulnerabilities(cves, page, total_pages):
    current_time = datetime.now()
    one_week_ago = current_time - timedelta(days=7)  # Define the threshold for considering a CVE as "New"

    for cve in cves:
        cve_number = cve["title"].split(":")[1].strip() if ":" in cve["title"] else "N/A"
        link = cve["link"]
        description = cve["description"]
        published_date = cve["published_date"]
        last_modified_date = cve["last_modified_date"]

        # Check if the CVE is "New" based on the last modified date
        is_new = last_modified_date > one_week_ago

        print(f"CVE Number: {cve_number}")
        if is_new:
            print("New!")
        print(f"Link: {link}")
        print(f"Description: {description}")
        print(f"Published Date: {published_date}")
        print(f"Last Modified Date: {last_modified_date}")
        print()

    print(f"Page {page} of {total_pages}")


def filter_by_category(cves, category):
    filtered_cves = [cve for cve in cves if category.lower() in cve["description"].lower()]
    return filtered_cves
