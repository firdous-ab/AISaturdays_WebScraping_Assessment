import os
from bs4 import BeautifulSoup
import requests
import pandas as pd

file_name = "Web_Scraped_Jumia_Reviews.csv"

# for a fresh scrape each run
if os.path.exists(file_name):
    os.remove(file_name)

base_url = "https://www.jumia.com.ng/catalog/productratingsreviews/sku/OR537EA5UCNV3NAFAMZ/?page={}"

# to automatically loop through each jumia review page
for page in range(1, 57):  
    print(f"Scraping page {page}...")

    html_text = requests.get(base_url.format(page), timeout=10).text
    soup = BeautifulSoup(html_text, 'lxml')
    review_container = soup.find_all('article', class_='-pvs -hr _bet')
    review_list = []

    # if not review_container:
    #     print(f"No reviews found on page {page}. Stopping...")
    #     break  # stop if no more reviews are found

    for reviews in review_container:
        review_topic = reviews.find('h3', class_='-m -fs16 -pvs').text.strip()
        review_body = reviews.find('p', class_='-pvs').text.strip()
        review_rating = reviews.find('div', class_='stars _m _al -mvs').text.split()[0]
        review_date = reviews.find('span', class_='-prs').text.strip()
        name = reviews.find('span', class_='').text.strip().split()
        if len(name) <= 2:
            name.append('')
        customer_name = " ".join(name[-2:])
        review_dictionary = {
            "Customer Name": customer_name,
            "Review Topic": review_topic,
            "Review Body": review_body,
            "Rating (of 5)": review_rating,
            "Review Date": review_date
        }
        review_list.append(review_dictionary)

    df = pd.DataFrame(review_list)

    # Append to CSV
    df.to_csv(file_name, mode='a', index=False, header=not os.path.exists(file_name))

print("All pages scraped successfully!")