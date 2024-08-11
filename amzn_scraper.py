import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 5})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup):
    review_containers = soup.find_all('div', {'data-hook': 'review'})
    with open("amazon_reviews.txt", 'a', encoding='utf-8') as f:
        for review in review_containers:
            review_text= review.find('span', {'data-hook': 'review-body'}).text.strip()
            review_rating =  float(review.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip())
            print(review_rating)
            print(review_text)
            f.write(f'Rating: {review_rating}\n')
            f.write(f'Review: {review_text}\n\n')
            

def get_recent_reviews(soup):
    review_containers = soup.find_all('div', {'data-hook': 'review'})
    with open("amazon_recent_reviews.txt", 'a', encoding='utf-8') as f:
        for review in review_containers:
            review_text= review.find('span', {'data-hook': 'review-body'}).text.strip()
            review_rating =  float(review.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip())
            print(review_rating)
            print(review_text)
            f.write(f'Rating: {review_rating}\n')
            f.write(f'Review: {review_text}\n\n')


link="https://www.amazon.com/Mighty-Patch-Hydrocolloid-Absorbing-count/product-reviews/B074PVTPBW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
link.replace("&reviewerType=all_reviews","")
link2=link
x=1
with open("amazon_reviews.txt", 'w', encoding='utf-8') as f:
    f.write("Reviews: \n")
while x<3:
    soup = get_soup(link + f"&reviewerType=all_reviews&pageNumber={x}")
    print(f'Getting page: {x}')
    get_reviews(soup)
    x=x+1

y=1

with open("amazon_recent_reviews.txt", 'w', encoding='utf-8') as f:
    f.write("Reviews: \n")
while y<3:
    soup = get_soup(link2 + f"&reviewerType=all_reviews&sortBy=recent&pageNumber={y}")
    print(f'Getting page: {x}')
    get_recent_reviews(soup)
    y+=1
