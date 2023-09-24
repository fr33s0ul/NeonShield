from flask import Flask, render_template, request
from utils import fetch_data, search_cves, display_vulnerabilities
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form.get('search')
        cves = fetch_data()
        cves = search_cves(cves, search_term)
    else:
        cves = fetch_data()
    
    # Pagination
    page = int(request.args.get('page', 1))  # Get the current page number from the URL query parameters
    page_size = 10  # Number of CVEs to display per page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    cves_paginated = cves[start_index:end_index]
    total_pages = len(cves) // page_size + 1

    # Mark CVEs as new or not
    current_time = datetime.now()
    two_weeks_ago = current_time - timedelta(weeks=2)  # Define the threshold for considering a CVE as "New"

    for cve in cves_paginated:
        if isinstance(cve["last_modified_date"], datetime):
            is_new = cve["last_modified_date"] > two_weeks_ago
            cve["is_new"] = is_new
        else:
            cve["is_new"] = False

    display_vulnerabilities(cves_paginated, page, total_pages)  # Display vulnerabilities

    start_page = max(1, page - 2)
    end_page = min(start_page + 4, total_pages)

    return render_template('base.html', cves=cves_paginated, page=page, total_pages=total_pages,
                           start_page=start_page, end_page=end_page)

if __name__ == '__main__':
    app.run(debug=True)
